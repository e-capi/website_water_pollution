import matplotlib.pyplot as plt
import pandas as pd


def plot_24(df, length, forecast, upper=None, lower=None):
    length = int(length)
    df = df['initial']
    df = df[-24:] #Time series calculated on the last 24 months



    forecast = pd.concat([df[[-1]], forecast])
    lower = pd.concat([df[[-1]], lower])
    upper = pd.concat([df[[-1]], upper])
    index = df.index[-(length + 2):-1] + df.index.freq * (length + 1)

    fig = plt.figure(figsize=(10, 4), dpi=100)
    plt.plot(df, label='Last 24 months', color='black')
    plt.plot(forecast,
             label=f'{length} months Forecast',
             color='orange',
             ls='--')
    plt.fill_between(lower.index, lower[0], upper[0], color='k', alpha=0.15) #HARD CODE [0] to be check
    plt.title(f'Nitrate Concentration Forecast for the next {length} months')
    plt.legend(loc='upper left', fontsize=8)

    return fig
