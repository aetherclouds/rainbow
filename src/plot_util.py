import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll

# MODIFIED FROM https://stackoverflow.com/a/36074775/15806103

def colorline(
        ax, x, y, z=None, cmap='copper', norm=plt.Normalize(0.0, 1.0),
        linewidth=1, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """
    
    # Default colors equally spaced on [0,1]:
    if z is None:
        # # use this to generate the rainbow gradient n times
        # n_rainbows = 2
        # z = np.fromfunction(lambda i: (i*n_rainbows/len(x))%1, [len(x)], dtype=float)
        z = np.linspace(0, 1, len(x))

    # Special case if a single number:
    # to check for numerical input -- this is a hack
    if not hasattr(z, "__iter__"):
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                            linewidth=linewidth, alpha=alpha)


    ax.add_collection(lc)

    return lc

def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments