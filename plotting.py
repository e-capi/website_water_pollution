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

        fig = plt.figure(figsize=(12,5))
        ax = plt.axes()

        ax.set_facecolor("white")
        fig.patch.set_facecolor('white')
        for location in ['left','right','bottom','top']:
            ax.spines[location].set_visible(False)

        plt.plot(initial,label='Historique')
        plt.plot(forecast,label='Prévision du modèle')
        plt.fill_between(lower.index,lower,upper,color='k',alpha=.10)

        plt.xticks(rotation=50)

        plt.title('Concentration en Nitrate (mg/L)')
        plt.legend()
        plt.ylim(bottom=-1,top=(ax.get_ylim()[1]+4))
        plt.show()


    return fig
