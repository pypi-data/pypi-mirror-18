from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import functools

from measurement_stats import ValueUncertainty
from measurement_stats import distributions as mdists


def unzip(values, raw=False):
    """

    :param values:

    :param raw: (optional) If True, the values and uncertainty lists will be
        raw instead the standard truncated formats specified by error
        propagation rules
    :return: tuple containing a list of values and a list of uncertainties
    """

    vals = []
    uncs = []

    if isinstance(values[0], (list, tuple)):
        values = values[0]

    for v in values:
        vals.append(v.raw if raw else v.value)
        uncs.append(v.raw_uncertainty if raw else v.uncertainty)

    return vals, uncs


def join(values, uncertainties):
    """

    :param values:
    :param uncertainties:
    :return:
    """

    out = []
    for i in range(len(values)):
        if isinstance(uncertainties, (list, tuple)):
            unc = uncertainties[i]
        else:
            unc = uncertainties
        out.append(ValueUncertainty(values[i], unc))

    return out


def from_serialized(serialized):
    """

    :param serialized:
    :return:
    """

    return [
        ValueUncertainty(
            x.get('raw', x['value']),
            x.get('raw_uncertainty', x['uncertainty'])
        ) for x in serialized
    ]


def deviations(expected, values):
    """

    :param expected:
    :param values:
    :return:
    """

    out = []

    if hasattr(expected, 'raw_uncertainty'):
        for v in values:
            err = math.sqrt(
                v.raw_uncertainty ** 2 +
                expected.raw_uncertainty ** 2
            )
            out.append(abs(v.raw - expected.raw) / err)
    else:
        for v in values:
            out.append(abs(v.value - expected) / v.uncertainty)

    return out


def windowed_smooth(measurements, size=1, population_size=512):
    """
    Returns a new list of measurements with the same length as the source
    measurements, where each value in the result is calculated as the median
    and weighted MAD of the nearest +/- size measurements and the measurement
    itself.

    For example, if the resulting value for measurement X10 with a size of 2
    would be median +/- the weighted MAD of the measurements
    (X8, X9, X10, X11, X12)

    Edge conditions are handled so that they are smoothed with partial windows

    :param measurements:
    :param size:
        The extend of the smoothing window.
    :param population_size:
    :return:
    """

    window = []
    window_populations = []

    while len(window) < size + 1:
        m = measurements[len(window)]

        window.append(m)
        window_populations.append(
            mdists.population(
                mdists.Distribution([m]),
                count=population_size
            )
        )

    out = []

    for i in range(len(measurements)):
        pop_combined = []
        for p in window_populations:
            pop_combined += p

        out.append(ValueUncertainty(
            mdists.percentile(pop_combined),
            mdists.weighted_median_average_deviation(pop_combined)
        ))

        append_index = i + size + 1

        if append_index >= len(measurements):
            window.pop(0)
            window_populations.pop(0)
            continue

        m = measurements[append_index]
        d = mdists.Distribution([m])
        pop = mdists.population(d, population_size)
        window.append(m)
        window_populations.append(pop)

        while len(window) > (2 * size + 1):
            window.pop(0)
            window_populations.pop(0)

    return out


def box_smooth(measurements, size=2, population_size=512):
    """

    :param measurements:
    :param size:
    :param population_size:
    :return:
    """

    out = []

    for i in range(0, len(measurements), size):
        d = mdists.Distribution(measurements[i:(i + size)])
        pop = mdists.population(d, count=population_size)
        median = mdists.percentile(pop)
        mad = mdists.weighted_median_average_deviation(pop)
        while len(out) < (i + size):
            out.append(ValueUncertainty(median, mad))

    return out


def maximum(measurements):
    """

    :param measurements:
    :return:
    """

    def max_compare(a, b):
        if a is None:
            return b
        elif b is None:
            return a

        if a.value > b.value:
            return a
        elif b.value > a.value:
            return b

        return a if a.uncertainty < b.uncertainty else b

    return functools.reduce(max_compare, measurements)


def minimum(measurements):
    """

    :param measurements:
    :return:
    """

    def min_compare(a, b):
        if a is None:
            return b
        elif b is None:
            return a

        if a.value < b.value:
            return a
        elif b.value < a.value:
            return b

        return b if b.uncertainty < a.uncertainty else a

    return functools.reduce(min_compare, measurements)
