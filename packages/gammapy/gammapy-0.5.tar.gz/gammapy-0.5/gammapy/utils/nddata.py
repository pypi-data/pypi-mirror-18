# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import absolute_import, division, print_function, unicode_literals
import itertools
import numpy as np
import abc
import copy
from ..extern.bunch import Bunch
from astropy.units import Quantity
from astropy.table import Table, Column
from astropy.io import fits
from astropy.extern import six
from .array import array_stats_str
from .scripts import make_path
from .fits import table_to_fits_table, fits_table_to_table

__all__ = [
    'NDDataArray',
    'DataAxis',
    'BinnedDataAxis',
]

# Note: test for this class are implemented in
# gammapy/irf/tests/test_effective_area2.py.

six.add_metaclass(abc.ABCMeta)
class NDDataArray(object):
    """ND Data Array Base class

    This is an abstract base class for n-dimensional data arrays. It handles
    interpolation and I/O. See :ref:`use-nddata`.
    """
    axis_names = ()
    """Axis names. This specifies the axis order"""

    interp_kwargs = dict(bounds_error=False)
    """Interpolation kwargs used to initialize the
    `scipy.interpolate.RegularGridInterpolator`.  The interpolation behaviour
    of an individual axis ('log', 'linear') can be passed to the axis on
    initialization."""

    def __init__(self, **kwargs):

        # TODO : Dynamically generate function signature
        # https://github.com/astropy/astropy/blob/ffc0a89b2c42fd440eb19bcb2f93db90cab3c98b/astropy/utils/codegen.py#L30
        data = kwargs.pop('data', None)

        # Extract meta dict
        meta = kwargs.pop('meta', None)
        if meta is not None:
            self.meta = Bunch(meta)

        # Set axes
        self._axes = list()
        for axis_name in self.axis_names:
            value = kwargs.pop(axis_name, None)
            if value is None:
                raise ValueError('No input for axis "{}"'.format(axis_name))
            elif isinstance(value, DataAxis):
                value = value.data
            elif not isinstance(value, Quantity):
                raise ValueError('No unit for axis "{}"'.format(axis_name))
            # This is needed to transform the class level axis attribute to an
            # instance level attribute
            template_axis = getattr(self, axis_name)
            axis = copy.deepcopy(template_axis)
            axis.data = value
            setattr(self, axis_name, axis)
            self._axes.append(axis)

        # Set remaining kwargs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

        if data is not None:
            self.data = data
        self._regular_grid_interp = None

    @property
    def axes(self):
        """Array holding the axes in correct order"""
        return self._axes

    @property
    def data(self):
        """Array holding the n-dimensional data"""
        return self._data

    @data.setter
    def data(self, data):
        """Set data

        Some sanitiy checks are performed to avoid an invalid array. Also, the
        interpolator is set to None to avoid unwanted behaviour.

        Parameters
        ----------
        data : `~astropy.units.Quantity`, array-like
            Data array
        """
        data = Quantity(data)
        dimension = len(data.shape)
        if dimension != self.dim:
            raise ValueError('Overall dimensions to not match. '
                             'Data: {}, Hist: {}'.format(dimension, self.dim))

        for dim in np.arange(self.dim):
            axis = self.axes[dim]
            if axis.nbins != data.shape[dim]:
                msg = 'Data shape does not match in dimension {d}\n'
                msg += 'Axis {n} : {sa}, Data {sd}'
                raise ValueError(msg.format(d=dim, n=self.axis_names[dim],
                                            sa=axis.nbins, sd=data.shape[dim]))
        self._regular_grid_interp = None
        self._data = data

    @property
    def dim(self):
        """Dimension (number of axes)"""
        return len(self.axes)

    def to_table(self):
        raise NotImplementedError('This must be implemented by subclasses')

    def to_hdulist(self):
        """Convert to HDUList

        Default: One extension containing the output of ``to_table``

        Returns
        -------
        hdulist : `~astropy.io.fits.HDUList`
            HDU list
        """
        hdu = table_to_fits_table(self.to_table())
        prim_hdu = fits.PrimaryHDU()
        return fits.HDUList([prim_hdu, hdu])

    def write(self, *args, **kwargs):
        """Write to disk

        Calling astropy I/O interface
        see http://docs.astropy.org/en/stable/io/unified.html
        """
        temp = list(args)
        temp[0] = str(make_path(args[0]))
        self.to_hdulist().writeto(*temp, **kwargs)

    @classmethod
    def from_table(cls, table):
        raise NotImplementedError('This must be implemented by subclasses')

    @classmethod
    def from_hdulist(cls, hdulist):
        """Read from disk

        Default: Read first extension as BinTableHDU
        """
        table = fits_table_to_table(hdulist[1])
        return cls.from_table(table)

    @classmethod
    def read(cls, *args, **kwargs):
        """Read from disk

        Calling astropy I/O interface
        see http://docs.astropy.org/en/stable/io/unified.html
        """
        # Support Path input
        temp = list(args)
        temp[0] = str(make_path(args[0]))
        hdulist  = fits.open(*temp, **kwargs)
        return cls.from_hdulist(hdulist)

    def __str__(self):
        """String representation"""
        ss = '{} summary info\n'.format(type(self).__name__)
        for axis, axname in zip(self.axes, self.axis_names):
            ss += array_stats_str(axis.data, axname)
        ss += array_stats_str(self.data, 'Data')
        return ss

    def evaluate(self, method=None, **kwargs):
        """Evaluate NDData Array

        This function provides a uniform interface to several interpolators.
        The evaluation nodes are given as ``kwargs``.

        Currently available:
        `~scipy.interpolate.RegularGridInterpolator`, methods: linear, nearest

        Parameters
        ----------
        method : str {'linear', 'nearest'}, optional
            Interpolation method
        kwargs : dict
            Keys are the axis names, Values the evaluation points

        Returns
        -------
        array : `~astropy.units.Quantity`
            Interpolated values, axis order is the same as for the NDData array
        """

        values = list()
        for axname, axis in zip(self.axis_names, self.axes):
            # Extract values for each axis, default: nodes
            temp = kwargs.pop(axname, axis.nodes)
            # Transform to correct unit
            temp = temp.to(axis.unit).value
            # Transform to match interpolation behaviour of axis
            values.append(np.atleast_1d(axis._interp_values(temp)))

        if method is None:
            return self._eval_regular_grid_interp(
                values) * self.data.unit
        elif method == 'linear':
            return self._eval_regular_grid_interp(
                values, method='linear') * self.data.unit
        elif method == 'nearest':
            return self._eval_regular_grid_interp(
                values, method='nearest') * self.data.unit
        else:
            raise ValueError('Interpolator {} not available'.format(method))

    def _eval_regular_grid_interp(self, values, **kwargs):
        """Evaluate linear interpolator

        Input: list of values to evaluate, in correct units and correct order.
        """
        if self._regular_grid_interp is None:
            self._add_regular_grid_interp()

        # This is necessary since np.append does not support the 1D case
        if self.dim > 1:
            shapes = np.append(*[np.shape(_) for _ in values])
        else:
            shapes = values[0].shape
        # Flatten in order to support 2D array input
        values = [_.flatten() for _ in values]
        points = list(itertools.product(*values))
        res = self._regular_grid_interp(points, **kwargs)
        res = np.reshape(res, shapes).squeeze()

        return res

    def _add_regular_grid_interp(self, interp_kwargs=None):
        """Add `~scipy.interpolate.RegularGridInterpolator`

        http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.RegularGridInterpolator.html

        Parameters
        ----------
        interp_kwargs : dict, optional
            Interpolation kwargs
        """
        from scipy.interpolate import RegularGridInterpolator

        if interp_kwargs is None:
            interp_kwargs = self.interp_kwargs
        points = [a._interp_nodes() for a in self.axes]
        values = self.data.value

        # If values contains nan, only setup interpolator in valid range
        if np.isnan(values).any():
            if self.dim > 1:
                raise NotImplementedError('Data grid contains nan. This is not'
                                          'supported for arrays dimension > 1')
            else:
                mask = np.isfinite(values)
                points = [points[0][mask]]
                values = values[mask]

        self._regular_grid_interp = RegularGridInterpolator(points, values,
                                                            **interp_kwargs)


class DataAxis(object):
    """Data axis to be used with NDDataArray

    Axis values are interpreted as nodes.
    """
    def __init__(self, data=None, interpolation_mode='linear'):
        self.data = data
        self._interpolation_mode = interpolation_mode

    @property
    def unit(self):
        """Axis unit"""
        return self.data.unit

    @classmethod
    def logspace(cls, vmin, vmax, nbins, unit=None):
        """Create axis with equally log-spaced nodes

        if no unit is given, it will be taken from vmax

        Parameters
        ----------
        vmin : `~astropy.units.Quantity`, float
            Lowest value
        vmax : `~astropy.units.Quantity`, float
            Highest value
        bins : int
            Number of bins
        unit : `~astropy.units.UnitBase`, str
            Unit
        """

        if unit is not None:
            vmin = Quantity(vmin, unit)
            vmax = Quantity(vmax, unit)
        else:
            vmin = Quantity(vmin)
            vmax = Quantity(vmax)
            unit = vmax.unit
            vmin = vmin.to(unit)

        x_min, x_max = np.log10([vmin.value, vmax.value])
        vals = np.logspace(x_min, x_max, nbins)

        return cls(vals * unit, interpolation_mode='log')

    def find_node(self, val):
        """Find next node

        Parameters
        ----------
        val : `~astropy.units.Quantity`
            Lookup value
        """
        val = Quantity(val)

        if not val.unit.is_equivalent(self.unit):
            raise ValueError('Units {} and {} do not match'.format(
                val.unit, self.unit))

        val = val.to(self.data.unit)
        val = np.atleast_1d(val)
        x1 = np.array([val] * self.nbins).transpose()
        x2 = np.array([self.nodes] * len(val))
        temp = np.abs(x1 - x2)
        idx = np.argmin(temp, axis=1)
        return idx

    @property
    def nbins(self):
        """Number of bins"""
        return self.data.size

    @property
    def nodes(self):
        """Evaluation nodes"""
        return self.data

    @property
    def interpolation_mode(self):
        """Interpolation mode
        """
        return self._interpolation_mode

    def _interp_nodes(self):
        """Nodes to be used for interpolation"""
        if self.interpolation_mode == 'log':
            return np.log10(self.nodes.value)
        else:
            return self.nodes.value

    def _interp_values(self, values):
        """Transform values correctly for interpolation"""
        if self.interpolation_mode == 'log':
            return np.log10(values)
        else:
            return values


class BinnedDataAxis(DataAxis):
    """Data axis for binned axis

    Axis values are interpreted as bin edges
    """
    @classmethod
    def logspace(cls, emin, emax, nbins, unit=None):
        return super(BinnedDataAxis, cls).logspace(
            emin, emax, nbins + 1, unit)

    @property
    def nbins(self):
        """Number of bins"""
        return self.data.size - 1

    @property
    def nodes(self):
        """Evaluation nodes

        Depending on the interpolation mode, either log or lin center are
        returned
        """
        if self.interpolation_mode == 'log':
            return self.log_center()
        else:
            return self.lin_center()

    def lin_center(self):
        """Linear bin centers"""
        return (self.data[:-1] + self.data[1:]) / 2

    def log_center(self):
        """Logarithmic bin centers"""
        return np.sqrt(self.data[:-1] * self.data[1:])
