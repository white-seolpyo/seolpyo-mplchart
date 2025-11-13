import matplotlib.pyplot as plt
import pandas as pd


def switch_backend(newbackend='TkAgg'):
    "call matplotlib.pyplot.switch_backend(newbackend)"
    return plt.switch_backend(newbackend)


def close(fig='all'):
    "call matplotlib.pyplot.close(fig)"
    return plt.close(fig)

def show(Close=True):
    """
    call matplotlib.pyplot.show()
    ```if Close``` if True, run matplotlib.pyplot.close('all') after window closee.
    """
    plt.show()
    if Close:
        close()
    return


def list_to_DataFrame(item_list):
    "return pd.DataFrame(item_list)"
    return pd.DataFrame(item_list)

