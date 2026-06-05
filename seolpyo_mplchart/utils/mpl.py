import matplotlib.pyplot as plt


def show(*args, **kwargs):
    "call matplotlib.pyplot.show(*args, **kwargs)"
    plt.show(*args, **kwargs)
    return

def switch_backend(backend='TkAgg'):
    "call matplotlib.pyplot.switch_backend(newbackend)"
    return plt.switch_backend(backend)

def close(fig='all'):
    "call matplotlib.pyplot.close(fig)"
    return plt.close(fig)

