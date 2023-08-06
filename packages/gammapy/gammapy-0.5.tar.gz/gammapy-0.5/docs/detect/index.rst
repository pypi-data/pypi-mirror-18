.. _detect:

*****************************************
Source detection tools (`gammapy.detect`)
*****************************************

.. currentmodule:: gammapy.detect

Introduction
============

The `gammapy.detect` submodule includes low level functions to compute significance
and test statistics images as well as some high level source detection method
prototypes.

Detailed description of the methods can be found in [Stewart2009]_
and [LiMa1983]_.

Computation of TS images
========================

.. image:: fermi_ts_image.png
    :scale: 100%

Test statistics image computed using `~gammapy.detect.compute_ts_image` for an
example Fermi dataset.

The `gammapy.detect` module includes a high performance `~gammapy.detect.compute_ts_image` function to
compute test statistics (TS) images for gamma-ray survey data. The implementation is based on the method
described in [Stewart2009]_.

Assuming a certain source morphology, which can be defined by any `astropy.convolution.Kernel2D`
instance, the amplitude of the morphology model is fitted at every pixel of the input data using a 
Poisson maximum likelihood procedure. As input data a counts, background and exposure images have to be provided.
Based on the best fit flux amplitude, the change in TS, compared to the null hypothesis is computed
using `~gammapy.stats.cash` statistics.

To optimize the performance of the code, the fitting procedure is simplified by finding roots
of the derivative of the fit statistics with respect to the flux amplitude. This approach is
described in detail in Appendix A of [Stewart2009]_. To further improve the performance,
Pythons's `multiprocessing` facility is used.

In the following the computation of a TS image for prepared Fermi survey data, which is provided in
`gammapy-extra <https://github.com/gammapy/gammapy-extra/tree/master/datasets/fermi_survey>`_, shall be demonstrated:

.. code-block:: python

	from astropy.convolution import Gaussian2DKernel
	from gammapy.image import SkyImageList
	from gammapy.detect import compute_ts_image
	images = SkyImageList.read('$GAMMAPY_EXTRA/datasets/fermi_survey/all.fits.gz')
	kernel = Gaussian2DKernel(5)
	result = compute_ts_image(images['counts'], images['background'],
							  images['exposure'], kernel)

The function returns a `~gammapy.image.SkyImageList` object, that bundles all relevant
data. E.g. the time needed for the TS image computation can be checked by:

.. code-block:: python

	print(result.meta['runtime'])

The TS image itself can be accessed using the ``ts`` attribute of the `~gammapy.image.SkyImageList` object:

.. code-block:: python

	print(result.ts.data.max())

Command line tool
-----------------

Gammapy also provides a command line tool ``gammapy-image-ts`` for TS image computation, which can be run
on the Fermi example dataset by:

.. code-block:: bash

	$ cd $GAMMAPY_EXTRA/datasets/fermi_survey
	$ gammapy-image-ts all.fits.gz ts_image_0.00.fits --scale 0

The command line tool additionally requires a psf json file, where the psf shape
is defined by the parameters of a triple Gaussian model. See also 
`gammapy.irf.multi_gauss_psf_kernel`. By default the command line tool uses
a Gaussian source kernel, where the width in degree can be defined by the 
``--scale`` parameter. Multiple scales can be selected by passing a list to the
``scales`` parameter.  When setting ``--scale 0`` only the psf is used as source
model, which is the preferred setting to detect point sources. When using scales
that are larger than five times the binning of the data, the data is sampled down
and later sampled up again to speed up the performance. See 
`~gammapy.image.downsample_2N` and `~gammapy.image.upsample_2N` for details.   

Furthermore it is possible to compute residual TS images. Using the following options:
 
.. code-block:: bash

	$ gammapy-image-ts all.fits.gz residual_ts_image_0.00.fits --scale 0 --residual --model model.fits.gz

When ``--residual`` is set an excess model must be provided using the ``--model`` option.


Computation of Li&Ma significance images
========================================

The method derived by [LiMa1983]_ is one of the standard methods to determine
detection significances for gamma-ray sources. Using the same prepared Fermi
dataset as above, the corresponding images can be computed using the
`~gammapy.detect.compute_lima_image` function:

.. code-block:: python

    from astropy.convolution import Tophat2DKernel
    from gammapy.image import SkyImageList
    from gammapy.detect import compute_lima_image
    images = SkyImageList.read('$GAMMAPY_EXTRA/datasets/fermi_survey/all.fits.gz')
    kernel = Tophat2DKernel(5)
    result = compute_lima_image(images['counts'].data, images['background'].data, kernel)

The function returns a `~gammapy.image.SkyImageList`, that bundles all resulting
images such as significance, flux and correlated counts and excess images.


Command line tool
-----------------

There is also a corresponding command line tool available. That can be used as
following:

.. code-block:: bash

    $ cd gammapy-extra/datasets/fermi_survey
    $ gammapy-image-lima all.fits.gz lima_image_0.1.fits --theta 0.1
    

The command line tool features an ``--onoff`` option to compute Li & Ma significance
for on-off observations and a ``--residual`` option to compute residual significance
images. For this function the input fits file needs a ``model`` extension, containing
a excess model.


Iterative source detection
==========================

In addition to ``gammapy-image-ts`` there is also command-line tool ``gammapy-detect-iterative``, which runs iterative multi-scale source detection. 
It takes as arguments count, background and exposure FITS images (in separate files, unlike previous tool)
and a list of ``--scales`` and calls ``~gammapy.detect.iterfind.IterativeSourceDetection`` class.

It implements the following algorithm:

1. Compute significance images on multiple scales (disk-correlate)
2. Largest peak on any scale gives a seed position / extension (the scale)
3. Fit a 2D Gauss-model source using the seed parameters
4. Add the source to a list of detected sources and the background model
5. Restart at step 1, but this time with detected sources added to the background model, i.e. significance images will be "residual significance" images.

Usage example:

.. code-block:: bash

	$ cd $GAMMAPY_EXTRA/datasets/source_diffuse_separation/galactic_simulations
	$ gammapy-detect-iterative --counts fermi_counts.fits --background fermi_diffuse.fits --exposure fermi_exposure_gal.fits output_fits output_regions


Reference/API
=============

.. automodapi:: gammapy.detect
    :no-inheritance-diagram:
