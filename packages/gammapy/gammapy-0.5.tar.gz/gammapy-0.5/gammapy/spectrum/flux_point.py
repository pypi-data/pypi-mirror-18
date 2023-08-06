# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Differential and integral flux point computations."""
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from collections import OrderedDict
import numpy as np
from astropy.table import Table
from astropy.units import Quantity, Unit
from gammapy.utils.scripts import make_path

from ..utils.fits import table_from_row_data
from ..utils.energy import Energy, EnergyBounds
from ..spectrum.powerlaw import power_law_flux
from ..spectrum.models import PowerLaw

__all__ = [
    'DifferentialFluxPoints',
    'IntegralFluxPoints',
    'compute_differential_flux_points',
    'FluxPointEstimator',
    'SEDLikelihoodProfile',
]

log = logging.getLogger(__name__)


class DifferentialFluxPoints(Table):
    """Differential flux points table

    Column names: ENERGY, ENERGY_ERR_HI, ENERGY_ERR_LO,
    DIFF_FLUX, DIFF_FLUX_ERR_HI, DIFF_FLUX_ERR_LO
    For a complete documentation see :ref:`gadf:flux-points`, for an usage
    example see :ref:`flux-point-computation`.

    Upper limits are stored as in the Fermi catalogs. I.e. the lower error is set
    to `NaN`, while the upper error represents the 1 sigma upper limit.
    """

    @classmethod
    def from_arrays(cls, energy, diff_flux, energy_err_hi=None,
                    energy_err_lo=None, diff_flux_err_hi=None,
                    diff_flux_err_lo=None):
        """Create `~gammapy.spectrum.DifferentialFluxPoints` from numpy arrays"""
        t = Table()
        energy = Energy(energy)
        diff_flux = Quantity(diff_flux)
        if not diff_flux.unit.is_equivalent('TeV-1 cm-2 s-1'):
            raise ValueError(
                'Flux (unit {}) not a differential flux'.format(diff_flux.unit))

        # Set errors to zero by default
        def_f = np.zeros(len(energy)) * diff_flux.unit
        def_e = np.zeros(len(energy)) * energy.unit
        if energy_err_hi is None:
            energy_err_hi = def_e
        if energy_err_lo is None:
            energy_err_lo = def_e
        if diff_flux_err_hi is None:
            diff_flux_err_hi = def_f
        if diff_flux_err_lo is None:
            diff_flux_err_lo = def_f

        t['ENERGY'] = energy
        t['ENERGY_ERR_HI'] = Quantity(energy_err_hi)
        t['ENERGY_ERR_LO'] = Quantity(energy_err_lo)
        t['DIFF_FLUX'] = diff_flux
        t['DIFF_FLUX_ERR_HI'] = Quantity(diff_flux_err_hi)
        t['DIFF_FLUX_ERR_LO'] = Quantity(diff_flux_err_lo)
        return cls(t)

    def plot(self, ax=None, energy_unit='TeV',
             flux_unit='cm-2 s-1 TeV-1', energy_power=0, **kwargs):
        """Plot flux points

        kwargs are forwarded to :func:`~matplotlib.pyplot.errorbar`

        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`, optional
            Axis
        energy_unit : str, `~astropy.units.Unit`, optional
            Unit of the energy axis
        flux_unit : str, `~astropy.units.Unit`, optional
            Unit of the flux axis
        energy_power : int
            Power of energy to multiply flux axis with

        Returns
        -------
        ax : `~matplotlib.axes.Axes`, optional
            Axis
        """
        import matplotlib.pyplot as plt

        kwargs.setdefault('fmt', 'o')
        ax = plt.gca() if ax is None else ax

        energy = self['ENERGY'].quantity.to(energy_unit)
        energy_hi = self['ENERGY_ERR_HI'].quantity.to(energy_unit)
        energy_lo = self['ENERGY_ERR_LO'].quantity.to(energy_unit)

        flux = self['DIFF_FLUX'].quantity.to(flux_unit)

        # lower flux error is stored with negative sign, account for that
        flux_lo = np.abs(self['DIFF_FLUX_ERR_LO'].quantity.to(flux_unit))
        flux_hi = self['DIFF_FLUX_ERR_HI'].quantity.to(flux_unit)

        eunit = [_ for _ in flux.unit.bases if _.physical_type == 'energy'][0]
        yunit = flux.unit * eunit ** energy_power
        y = (flux * np.power(energy, energy_power)).to(yunit)
        y_hi = (flux_hi * np.power(energy, energy_power)).to(yunit)
        y_lo = (flux_lo * np.power(energy, energy_power)).to(yunit)

        # plot flux points
        is_ul = np.isnan(flux_lo).astype('bool')
        yerr = (y_lo.value[~is_ul], y_hi.value[~is_ul])
        xerr = (energy_lo.value[~is_ul], energy_hi.value[~is_ul])

        kwargs.setdefault('marker', 'None')
        ax.errorbar(energy.value[~is_ul], y.value[~is_ul],
                    yerr=yerr, xerr=xerr, **kwargs)

        # plot upper limit flux points
        xerr = (energy_lo.value[is_ul], energy_hi.value[is_ul])

        ul_kwargs = {'marker': 'v',
                     'label': None}

        kwargs.setdefault('ms', 10)
        kwargs.setdefault('mec', 'None')
        kwargs.update(ul_kwargs)

        # UL are typically shown as 2 * sigma
        ax.errorbar(energy.value[is_ul], 2 * y_hi.value[is_ul], xerr=xerr, **kwargs)

        ax.set_xlabel('Energy [{}]'.format(energy_unit))
        if energy_power > 0:
            ax.set_ylabel('E{0} * Flux [{1}]'.format(energy_power, yunit))
        else:
            ax.set_ylabel('Flux [{}]'.format(yunit))
        ax.set_xscale("log", nonposx='clip')
        ax.set_yscale("log", nonposy='clip')
        return ax


class IntegralFluxPoints(Table):
    """Integral flux points table

    Column names: ENERGY_MIN, ENERGY_MAX, INT_FLUX, INT_FLUX_ERR_HI, INT_FLUX_ERR_LO
    For a complete documentation see :ref:`gadf:flux-points`
    """

    @classmethod
    def from_arrays(cls, ebounds, int_flux, int_flux_err_hi=None,
                    int_flux_err_lo=None):
        """Create `~gammapy.spectrum.IntegralFluxPoints` from numpy arrays"""
        t = Table()
        ebounds = EnergyBounds(ebounds)
        int_flux = Quantity(int_flux)
        if not int_flux.unit.is_equivalent('cm-2 s-1'):
            raise ValueError('Flux (unit {}) not an integrated flux'.format(int_flux.unit))

        # Set errors to zero by default
        def_f = np.zeros(ebounds.nbins) * int_flux.unit
        int_flux_err_hi = def_f if int_flux_err_hi is None else int_flux_err_hi
        int_flux_err_lo = def_f if int_flux_err_lo is None else int_flux_err_lo

        t['ENERGY_MIN'] = ebounds.lower_bounds
        t['ENERGY_MAX'] = ebounds.upper_bounds
        t['INT_FLUX'] = int_flux
        t['INT_FLUX_ERR_HI'] = int_flux_err_hi
        t['INT_FLUX_ERR_LO'] = int_flux_err_lo

        t['INT_FLUX_ERR_HI_%'] = 100 * int_flux_err_hi / int_flux
        t['INT_FLUX_ERR_LO_%'] = 100 * int_flux_err_lo / int_flux
        return cls(t)

    @property
    def ebounds(self):
        """Energy bounds"""
        return EnergyBounds.from_lower_and_upper_bounds(
            self['ENERGY_MIN'], self['ENERGY_MAX'])

    def to_differential_flux_points(self, x_method='lafferty',
                                    y_method='power_law', model=None,
                                    spectral_index=None):
        """Create `~gammapy.spectrum.DifferentialFluxPoints`

        see :func:`~gammapy.spectrum.compute_differential_flux_points`.
        """
        energy_min = self['ENERGY_MIN'].to('TeV').value
        energy_max = self['ENERGY_MAX'].to('TeV').value
        int_flux = self['INT_FLUX'].to('cm-2 s-1').value
        # Use upper error as symmetric value
        int_flux_err_hi = self['INT_FLUX_ERR_HI'].to('cm-2 s-1').value
        int_flux_err_lo = self['INT_FLUX_ERR_LO'].to('cm-2 s-1').value

        val = compute_differential_flux_points(
            x_method=x_method,
            y_method=y_method,
            model=model,
            spectral_index=spectral_index,
            energy_min=energy_min,
            energy_max=energy_max,
            int_flux=int_flux,
            int_flux_err_hi=int_flux_err_hi,
            int_flux_err_lo=int_flux_err_lo,
        )

        energy = val['ENERGY'] * Unit('TeV')
        f = val['DIFF_FLUX'] * Unit('TeV-1 cm-2 s-1')
        f_err_hi = val['DIFF_FLUX_ERR_HI'] * Unit('TeV-1 cm-2 s-1')
        f_err_lo = val['DIFF_FLUX_ERR_LO'] * Unit('TeV-1 cm-2 s-1')

        energy_min = Quantity(self['ENERGY_MIN'])
        energy_max = Quantity(self['ENERGY_MAX'])

        # assume symmetric errors
        return DifferentialFluxPoints.from_arrays(
            energy=energy,
            energy_err_hi=energy_max - energy,
            energy_err_lo=energy - energy_min,
            diff_flux=f,
            diff_flux_err_lo=f_err_lo,
            diff_flux_err_hi=f_err_hi,
        )


def compute_differential_flux_points(x_method='lafferty', y_method='power_law',
                                     table=None, model=None,
                                     spectral_index=None, energy_min=None,
                                     energy_max=None, int_flux=None,
                                     int_flux_err_hi=None, int_flux_err_lo=None):
    """Creates differential flux points table from integral flux points table.

    Parameters
    ----------
    table : `~astropy.table.Table`
        Integral flux data table in energy bins, including columns
        'ENERGY_MIN', 'ENERGY_MAX', 'INT_FLUX', 'INT_FLUX_ERR'
    energy_min : float, array_like
        If table not defined, minimum energy of bin(s) may be input
        directly as either a float or array.
    energy_max : float, array_like
        If table not defined, maximum energy of bin(s) input directly.
    int_flux : float, array_like
        If table not defined, integral flux in bin(s) input directly. If array,
        energy_min, energy_max must be either arrays of the same shape
        (for differing energy bins) or floats (for the same energy bin).
    int_flux_err_hi : float, array_like
        Type must be the same as for int_flux
    int_flux_err_lo : float, array_like
        Type must be the same as for int_flux
    x_method : {'lafferty', 'log_center', 'table'}
        Flux point energy computation method; either Lafferty & Wyatt
        model-based positioning, log bin center positioning
        or user-defined `~astropy.table.Table` positioning
        using column heading ['ENERGY']
    y_method : {'power_law', 'model'}
        Flux computation method assuming PowerLaw or user defined model function
    model : callable
        User-defined model function
    spectral_index : float, array_like
        Spectral index if default power law model is used. Either a float
        or array_like (in which case, energy_min, energy_max and int_flux
        must be floats to avoid ambiguity)

    Returns
    -------
    differential_flux_table : `~astropy.table.Table`
        Input table with appended columns 'ENERGY', 'DIFF_FLUX', 'DIFF_FLUX_ERR'

    Notes
    -----
    For usage, see this tutorial: :ref:`tutorials-flux_point`.
    """
    # Use input values if not initially provided with a table
    # and broadcast quantities to arrays if required
    if table is None:
        spectral_index = np.array(spectral_index).reshape(np.array(spectral_index).size, )
        energy_min = np.array(energy_min).reshape(np.array(energy_min).size, )
        energy_max = np.array(energy_max).reshape(np.array(energy_max).size, )
        int_flux = np.array(int_flux).reshape(np.array(int_flux).size, )
        try:
            # TODO: unresolved reference `int_flux_err`
            # and too broad except clause.
            # This function is spaghetti code ... needs to be refactored!
            int_flux_err = np.array(int_flux_err).reshape(np.array(int_flux_err).size, )
        except:
            pass
        # TODO: Can a better implementation be found here?
        lengths = dict(SPECTRAL_INDEX=len(spectral_index),
                       ENERGY_MIN=len(energy_min),
                       ENERGY_MAX=len(energy_max),
                       FLUX=len(int_flux))
        max_length = np.array(list(lengths.values())).max()
        int_flux = np.array(int_flux) * np.ones(max_length)
        spectral_index = np.array(spectral_index) * np.ones(max_length)
        energy_min = np.array(energy_min) * np.ones(max_length)
        energy_max = np.array(energy_max) * np.ones(max_length)
        try:
            int_flux_err = np.array(int_flux_err) * np.ones(max_length)
        except:
            pass
    # Otherwise use the table provided
    else:
        energy_min = np.asanyarray(table['ENERGY_MIN'])
        energy_max = np.asanyarray(table['ENERGY_MAX'])
        int_flux = np.asanyarray(table['INT_FLUX'])
        try:
            int_flux_err_hi = np.asanyarray(table['INT_FLUX_ERR_HI'])
            int_flux_err_lo = np.asanyarray(table['INT_FLUX_ERR_LO'])
        except:
            pass

    # Compute x point
    if x_method == 'table':
        # This is only called if the provided table includes energies
        energy = np.array(table['ENERGY'])
    elif x_method == 'log_center':
        from scipy.stats import gmean
        energy = np.array(gmean((energy_min, energy_max)))
    elif x_method == 'lafferty':
        if y_method == 'power_law':
            # Uses analytical implementation available for the power law case
            energy = _energy_lafferty_power_law(energy_min, energy_max,
                                                spectral_index)
        else:
            energy = np.array(_x_lafferty(energy_min,
                                          energy_max, model))
    else:
        raise ValueError('Invalid x_method: {0}'.format(x_method))

    # Compute y point
    if y_method == 'power_law':
        g = -1 * np.abs(spectral_index)
        diff_flux = power_law_flux(int_flux, g, energy, energy_min, energy_max)
    elif y_method == 'model':
        diff_flux = _ydiff_excess_equals_expected(int_flux, energy_min,
                                                  energy_max, energy, model)
    else:
        raise ValueError('Invalid y_method: {0}'.format(y_method))

    # Add to table
    table = Table()
    table['ENERGY'] = energy
    table['DIFF_FLUX'] = diff_flux

    # Error processing if required
    try:
        # TODO: more rigorous implementation of error propagation should be implemented
        # I.e. based on MC simulation rather than gaussian error assumption
        err_hi = int_flux_err_hi / int_flux
        diff_flux_err_hi = err_hi * diff_flux
        table['DIFF_FLUX_ERR_HI'] = diff_flux_err_hi

        err_lo = int_flux_err_lo / int_flux
        diff_flux_err_lo = err_lo * diff_flux
        table['DIFF_FLUX_ERR_LO'] = diff_flux_err_lo
    except:
        pass

    table.meta['spectral_index'] = spectral_index
    table.meta['spectral_index_description'] = "Spectral index assumed in the DIFF_FLUX computation"
    return table


def _x_lafferty(xmin, xmax, function):
    """The Lafferty & Wyatt method to compute X.

    Pass in a function and bin bounds x_min and x_max i.e. for energy
    See: Lafferty & Wyatt, Nucl. Instr. and Meth. in Phys. Res. A 355(1995) 541-547
    See: http://nbviewer.ipython.org/gist/cdeil/bdab5f236640ef52f736
    """
    from scipy.optimize import brentq
    from scipy import integrate

    indices = np.arange(len(xmin))

    x_points = []
    for index in indices:
        deltax = xmax[index] - xmin[index]
        I = integrate.quad(function, xmin[index], xmax[index], args=())
        F = (I[0] / deltax)

        def g(x):
            return function(x) - F

        x_point = brentq(g, xmin[index], xmax[index])
        x_points.append(x_point)
    return x_points


def _ydiff_excess_equals_expected(yint, xmin, xmax, x, model):
    """The ExcessEqualsExpected method to compute Y (differential).

    y / yint = y_model / yint_model"""
    yint_model = _integrate(xmin, xmax, model)
    y_model = model(x)
    return y_model * (yint / yint_model)


def _integrate(xmin, xmax, function, segments=1e3):
    """Integrates method function using the trapezium rule between xmin and xmax.
    """
    indices = np.arange(len(xmin))
    y_values = []
    for index in indices:
        x_vals = np.arange(xmin[index], xmax[index], 1.0 / segments)
        y_vals = function(x_vals)
        # Division by number of segments required for correct normalization
        y_values.append(np.trapz(y_vals) / segments)
    return y_values


def _energy_lafferty_power_law(energy_min, energy_max, spectral_index):
    """Analytical case for determining lafferty x-position for power law case.
    """
    # Cannot call into gammapy.powerlaw as implementation is different
    # due to different reference energies
    term0 = 1. - spectral_index
    term1 = energy_max - energy_min
    term2 = 1. / term0
    flux_lw = term2 / term1 * (energy_max ** term0 - energy_min ** term0)
    return np.exp(-np.log(flux_lw) / np.abs(spectral_index))


class FluxPointEstimator(object):
    """
    Flux point estimator.

    Parameters
    ----------
    obs : `~gammapy.spectrum.SpectrumObservation`
        Spectrum observation
    groups : `~gammapy.spectrum.SpectrumEnergyGroups`
        Energy groups (usually output of `~gammapy.spectrum.SpectrumEnergyGroupsMaker`)
    model : `~gammapy.spectrum.models.SpectralModel`
        Global model (usually output of `~gammapy.spectrum.SpectrumFit`)
    """

    def __init__(self, obs, groups, model):
        self.obs = obs
        self.groups = groups
        self.model = model

        self.flux_points = None

    def __str__(self):
        s = 'FluxPointEstimator:\n'
        s += str(self.obs) + '\n'
        s += str(self.groups) + '\n'
        s += str(self.model) + '\n'
        return s

    def compute_points(self):
        meta = OrderedDict(
            method='TODO',
        )
        rows = []
        for group in self.groups:
            if group.bin_type != 'normal':
                log.debug('Skipping energy group:\n{}'.format(group))
                continue

            row = self.compute_flux_point(group)
            rows.append(row)

        self.flux_points = table_from_row_data(rows=rows, meta=meta)

    def compute_flux_point(self, energy_group):
        log.debug('Computing flux point for energy group:\n{}'.format(energy_group))
        model = self.compute_approx_model(
            global_model=self.model,
            energy_range=energy_group.energy_range,
        )

        energy_ref = self.compute_energy_ref(energy_group)

        return self.fit_point(
            model=model, energy_group=energy_group, energy_ref=energy_ref,
        )

    def compute_energy_ref(self, energy_group):
        return energy_group.energy_range.log_center

    @staticmethod
    def compute_approx_model(global_model, energy_range):
        """
        Compute approximate model, to be used in the energy bin.
        """
        # binning = EnergyBounds(binning)
        # low_bins = binning.lower_bounds
        # high_bins = binning.upper_bounds
        #
        # from sherpa.models import PowLaw1D
        #
        # if isinstance(model, models.PowerLaw):
        #     temp = model.to_sherpa()
        #     temp.gamma.freeze()
        #     sherpa_models = [temp] * binning.nbins
        # else:
        #     sherpa_models = [None] * binning.nbins
        #
        # for low, high, sherpa_model in zip(low_bins, high_bins, sherpa_models):
        #     log.info('Computing flux points in bin [{}, {}]'.format(low, high))
        #
        #     # Make PowerLaw approximation for higher order models
        #     if sherpa_model is None:
        #         flux_low = model(low)
        #         flux_high = model(high)
        #         index = powerlaw.power_law_g_from_points(e1=low, e2=high,
        #                                                  f1=flux_low,
        #                                                  f2=flux_high)
        #
        #         log.debug('Approximated power law index: {}'.format(index))
        #         sherpa_model = PowLaw1D('powlaw1d.default')
        #         sherpa_model.gamma = index
        #         sherpa_model.gamma.freeze()
        #         sherpa_model.ref = model.parameters.reference.to('keV')
        #         sherpa_model.ampl = 1e-20
        #return PowerLaw(
        #    index=Quantity(2, ''),
        #    amplitude=Quantity(1, 'm-2 s-1 TeV-1'),
        #    reference=Quantity(1, 'TeV'),
        #)
        return global_model

    def fit_point(self, model, energy_group, energy_ref):
        from gammapy.spectrum import SpectrumFit

        sherpa_model = model.to_sherpa()
        sherpa_model.gamma.freeze()
        fit = SpectrumFit(self.obs, sherpa_model)

        erange = energy_group.energy_range
        # TODO: Notice channels contained in energy_group
        fit.fit_range = erange.min, 0.9999 * erange.max

        log.debug(
            'Calling Sherpa fit for flux point '
            ' in energy range:\n{}'.format(fit)
        )

        fit.fit()

        res = fit.global_result

        energy_err_hi = energy_group.energy_range.max - energy_ref
        energy_err_lo = energy_ref - energy_group.energy_range.min
        diff_flux = res.model(energy_ref).to('m-2 s-1 TeV-1')
        err = res.model_with_uncertainties(energy_ref.to('TeV').value)
        diff_flux_err = err.s * Unit('m-2 s-1 TeV-1')

        return OrderedDict(
            energy=energy_ref,
            energy_err_hi=energy_err_hi,
            energy_err_lo=energy_err_lo,
            diff_flux=diff_flux,
            diff_flux_err_hi=diff_flux_err,
            diff_flux_err_lo=diff_flux_err,
        )


class SEDLikelihoodProfile(object):
    """SED likelihood profile.

    See :ref:`gadf:likelihood_sed`.

    TODO: merge this class with the classes in ``fermipy/castro.py``,
    which are much more advanced / feature complete.
    This is just a temp solution because we don't have time for that.
    """

    def __init__(self, table):
        self.table = table

    @classmethod
    def read(cls, filename, **kwargs):
        filename = make_path(filename)
        table = Table.read(str(filename), **kwargs)
        return cls(table=table)

    def __str__(self):
        s = self.__class__.__name__ + '\n'
        s += str(self.table)
        return s

    def plot(self, ax=None):
        import matplotlib.pyplot as plt
        if ax is None:
            ax = plt.gca()

        # TODO
