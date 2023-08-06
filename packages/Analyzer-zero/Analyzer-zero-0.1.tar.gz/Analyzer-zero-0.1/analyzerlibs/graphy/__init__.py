import matplotlib.style
import matplotlib.pylab as plt
matplotlib.style.use('ggplot')
plt.ion()

from pandas import DataFrame, Series


def draw(data, index=None, columns=None, kind='line', **kargs):
    """
    draw some data quickly
    """
    dd = None
    if isinstance(data, dict):
        dd = Series(data)
    else:
        dd = DataFrame(data)

    if index:
        dd.index = index
    if columns:
        dd.columns = columns
    ax = dd.plot(kind=kind, **kargs)
    plt.show()
    return ax, dd
