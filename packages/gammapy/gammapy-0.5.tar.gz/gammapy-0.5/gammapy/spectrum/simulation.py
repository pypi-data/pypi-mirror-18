# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import astropy.units as u
import logging
from ..utils.random import get_random_state
from .utils import calculate_predicted_counts
from .core import PHACountsSpectrum
from .observation import SpectrumObservation, SpectrumObservationList

__all__ = [
    'SpectrumSimulation'
]

log = logging.getLogger(__name__)

class SpectrumSimulation(object):
    """Simulate `~gammapy.spectrum.SpectrumObservation`.

    Parameters
    ----------
    aeff : `~gammapy.irf.EffectiveAreaTable`
        Effective Area
    edisp : `~gammapy.irf.EnergyDispersion`,
        Energy Dispersion
    source_model : `~gammapy.spectrum.models.SpectralModel`
        Source model
    livetime : `~astropy.units.Quantity`
        Livetime
    e_reco : `~astropy.units.Quantity`, optional
        Desired energy axis of the prediced counts vector By default, the reco
        energy axis of the energy dispersion matrix is used.
    background_model : `~gammapy.spectrum.models.SpectralModel`, optional
        Background model
    alpha : float, optional
        Exposure ratio between source and background
    """
    def __init__(self, aeff, edisp, source_model, livetime,
                 e_reco=None, background_model=None, alpha=None):
        self.aeff = aeff
        self.edisp = edisp
        self.source_model = source_model
        self.livetime = livetime
        self.e_reco = e_reco or edisp.e_reco.data
        self.background_model = background_model
        self.alpha = alpha

        self.on_vector = None
        self.off_vector = None
        self.obs = None
        self.result = SpectrumObservationList()

    @property
    def npred_source(self):
        """Predicted source `~gammapy.spectrum.CountsSpectrum`"""
        npred = calculate_predicted_counts(livetime=self.livetime,
                                           aeff=self.aeff,
                                           edisp=self.edisp,
                                           model=self.source_model)
        return npred

    @property
    def npred_background(self):
        """Predicted background `~gammapy.spectrum.CountsSpectrum`"""
        npred = calculate_predicted_counts(livetime=self.livetime,
                                           aeff=self.aeff,
                                           edisp=self.edisp,
                                           model=self.background_model)
        return npred

    def run(self, seed):
        """Simulate `~gammapy.spectrum.SpectrumObservationList`

        The seeds will be set as observation id. Previously produced results
        will be overwritten.

        Parameters
        ----------
        seed : array of ints
            Random number generator seeds
        """
        self.reset()
        n_obs = len(seed)
        log.info("Simulating {} observations".format(n_obs))
        for counter, current_seed in enumerate(seed):
            progress = ((counter + 1) / n_obs) * 100
            if progress % 10 == 0:
                log.info("Progress : {} %".format(progress))
            self.simulate_obs(seed=current_seed)
            self.obs.obs_id = current_seed
            self.result.append(self.obs)

    def reset(self):
        """Clear all results"""
        self.result = SpectrumObservationList()
        self.obs = None
        self.on_vector = None
        self.off_vector = None

    def simulate_obs(self, seed='random-seed'):
        """Simulate one `~gammapy.spectrum.SpectrumObservation`.

        The result is stored as ``obs`` attribute

        Parameters
        ----------
        seed : {int, 'random-seed', 'global-rng', `~numpy.random.RandomState`}
            see :func:~`gammapy.utils.random.get_random_state`
        """
        rand = get_random_state(seed)
        self.simulate_source_counts(rand)
        if self.background_model is not None:
            self.simulate_background_counts(rand)
        obs = SpectrumObservation(on_vector=self.on_vector,
                                  off_vector=self.off_vector,
                                  aeff=self.aeff,
                                  edisp=self.edisp)
        self.obs = obs

    def simulate_source_counts(self, rand):
        """Simulate source `~gammapy.spectrum.PHACountsSpectrum`

        Source counts are added to the on vector.

        Parameters
        ----------
        rand: `~numpy.random.RandomState`
            random state
        """
        on_counts = rand.poisson(self.npred_source.data)

        counts_kwargs = dict(energy=self.e_reco,
                             livetime=self.livetime,
                             creator=self.__class__.__name__)

        on_vector = PHACountsSpectrum(data=on_counts,
                                      backscal=1,
                                      **counts_kwargs)

        self.on_vector = on_vector

    def simulate_background_counts(self, rand):
        """Simulate background `~gammapy.spectrum.PHACountsSpectrum`

        Background counts are added to the on vector. Furthermore
        background counts divided by alpha are added to the off vector.

        TODO: At the moment the source IRFs are used. Make it possible to pass
        dedicated background IRFs.

        Parameters
        ----------
        rand: `~numpy.random.RandomState`
            random state
        """
        bkg_counts = rand.poisson(self.npred_background.data)
        off_counts = rand.poisson(self.npred_background.data / self.alpha)

        # Add background to on_vector
        self.on_vector.data += bkg_counts

        # Create off vector
        off_vector = PHACountsSpectrum(energy=self.e_reco,
                                       data=off_counts,
                                       livetime=self.livetime,
                                       backscal=1. / self.alpha,
                                       is_bkg=True,
                                       creator=self.__class__.__name__)
        self.off_vector = off_vector
