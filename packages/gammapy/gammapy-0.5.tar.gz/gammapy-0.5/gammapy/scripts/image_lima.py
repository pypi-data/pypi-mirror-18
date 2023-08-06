# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import click
click.disable_unicode_literals_warning = True

import numpy as np
from astropy.convolution import Tophat2DKernel

from ..detect import compute_lima_image, compute_lima_on_off_image
from ..image import SkyImageList

__all__ = ['image_lima']

log = logging.getLogger(__name__)

@click.command()
@click.argument('infile')
@click.argument('outfile')
@click.option('--theta', multiple=True, type=float, help='On-region correlation radii (deg)')
@click.option('--onoff', is_flag=True, default=False, help='Compute Li&Ma images for'
              'on/off observation.')
@click.option('--residual', is_flag=True, default=False, help='Compute Li&Ma residual'
                                            ' images, requires a model excess extension in the input file.')
@click.option('--overwrite', is_flag=True, default=False, help='Overwrite existing output file?')
def image_lima(infile, outfile, theta, onoff, residual, overwrite):
    """
    Compute Li&Ma significance images for a given set of input images.
    """
    log.info('Reading {0}'.format(infile))
    data = SkyImageList.read(infile)
    if residual:
        data.background += data.model

    for t in theta:
        # Convert theta to pix
        theta_pix = t / data._ref_header['CDELT2']
        kernel = Tophat2DKernel(theta_pix)
        with np.errstate(invalid='ignore', divide='ignore'):
            if not onoff:
                result = compute_lima_image(data.counts, data.background,
                                            kernel, data.exposure)
            else:
                result = compute_lima_on_off_image(data.n_on, data.n_off, data.a_on,
                                                   data.a_off, kernel)
        log.info('Computing derived images')
        if len(theta) > 1:
            outfile_ = outfile.replace('.fits', '_{0:.3f}.fits'.format(t))
        else:
            outfile_ = outfile

        log.info('Writing {0}'.format(outfile_))
        result.write(outfile_, header=data._ref_header, clobber=overwrite)


