# -*- coding: utf-8 -*-

"""Functions to create plots using matplotlib.
"""
import collections
import math
import numpy as np
import matplotlib.pyplot as plt

from typhon.math import stats as tpstats


__all__ = [
    'plot_distribution_as_percentiles',
    'heatmap',
]


def plot_distribution_as_percentiles(ax, x, y,
                                     nbins=10, bins=None,
                                     ptiles=(5, 25, 50, 75, 95),
                                     linestyles=(":", "--", "-", "--", ":"),
                                     ptile_to_legend=True,
                                     label=None,
                                     **kwargs):
    """Plot the distribution of y vs. x as percentiles.

    Bin y-data according to x-data (using :func:`typhon.math.stats.bin`).
    Then, within each bin, show the distribution by plotting percentiles.

    Arguments:

        ax (AxesSubplot): matplotlib axes to plot into
        x (ndarray): data for x-axis
        y (ndarray): data for y-axis
        nbins (int): Number of bins to use for dividing the x-data.
        bins (ndarray): Specific bins to use for dividing the x-data.
            Supersedes nbins.
        ptiles (ndarray): Percentiles to visualise.
        linestyles (List[str]): List of linestyles corresponding to percentiles
        ptile_to_legend (bool): True: Add a label to each percentile.
            False: Only add a legend to the median.
        label (str or None): Label to use in legend.
        **kwargs: Remaining arguments passed to :func:`AxesSubplot.plot`.
            You probably want to pass at least color.
    """

    if bins is None:
        bins = np.linspace(x.min(), x.max(), nbins)
    scores = tpstats.get_distribution_as_percentiles(x, y, bins, ptiles)

    # Collect where same linestyle is used, so it can be combined in
    # legend
    d_ls = collections.defaultdict(list)
    locallab = None
    for (ls, pt) in zip(linestyles, ptiles):
        d_ls[ls].append(pt)
    for i in range(len(ptiles)):
        if label is not None:
            if math.isclose(ptiles[i], 50):
                locallab = label + " (median)"
            else:
                if ptile_to_legend and linestyles[i] in d_ls:
                    locallab = label + " (p-{:s})".format(
                        "/".join("{:d}".format(x)
                                 for x in d_ls.pop(linestyles[i])))
                else:
                    locallab = None
        else:
            label = None

        ax.plot(bins, scores[:, i], linestyle=linestyles[i], label=locallab,
                **kwargs)


def heatmap(x, y, bins=20, bisectrix=True, ax=None, **kwargs):
    """Plot a heatmap of two data arrays.

    This function is a simple wrapper for :func:`plt.hist2d`.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y data.
        bins (int | [int, int] | array_like | [array, array]):
            The bin specification:

            - If int, the number of bins for the two dimensions
              (nx=ny=bins).

            - If [int, int], the number of bins in each dimension
              (nx, ny = bins).

            - If array_like, the bin edges for the two dimensions
              (x_edges=y_edges=bins).

            - If [array, array], the bin edges in each dimension
              (x_edges, y_edges = bins).

            The default value is 20.

        bisectrix (bool): Toggle drawing of the bisectrix.
        ax (AxesSubplot, optional): Axes to plot in.
        **kwargs: Additional keyword arguments passed to
            :func:`matplotlib.pyplot.hist2d`.

    Returns:
        AxesImage.

    Examples:

    .. plot::
        :include-source:

        import numpy as np
        import matplotlib.pyplot as plt
        from typhon.plots import heatmap


        x = np.random.randn(500)
        y = x + np.random.randn(x.size)

        fig, ax = plt.subplots()
        heatmap(x, y, ax=ax)

        plt.show()

    """
    if ax is None:
        ax = plt.gca()

    # Default keyword arguments to pass to hist2d().
    kwargs_defaults = {
        'cmap': plt.get_cmap('Greys', 8),
        'rasterized': True,
        }

    kwargs_defaults.update(kwargs)

    # Plot the heatmap.
    N, xedges, yedges, img = ax.hist2d(x, y, bins, **kwargs_defaults)

    # Plot the bisectrix.
    if bisectrix:
        ax.plot((x.min(), x.max()), (x.min(), x.max()),
                color='red', linestyle='--', linewidth=2)

    return img
