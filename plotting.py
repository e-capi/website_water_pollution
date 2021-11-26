import matplotlib.pyplot as plt
import pandas as pd


def plot_538(lower, upper, forecast, initial):

        # We keep only 36 month of the initial series
    initial = initial[-36:]

    # We add to forecast, lower and upper the last point of initial
    # to join the two curves
    lower = pd.concat([initial[-1:],lower])
    upper = pd.concat([initial[-1:],upper])
    forecast = pd.concat([initial[-1:],forecast])

    with plt.style.context('fivethirtyeight'):

        fig = plt.figure(figsize=(12, 5))
        plt.plot(initial, label='Nitrates')
        plt.plot(forecast, label='Prevision')
        plt.fill_between(lower.index, lower, upper, color='k', alpha=.10)

        plt.legend()
        plt.ylim(bottom=-2)
        plt.show()
    return fig
