import pandas as pd
import matplotlib.pyplot as plt

def get_data(tickers, dates):
    df = pd.DataFrame(index=dates)
    if 'SPY' not in tickers:
        tickers.insert(0, 'SPY')
    
    for ticker in tickers:
        df_temp = pd.read_csv(
            f"data/{ticker}.csv",
            index_col="Date",
            usecols=['Date', 'Adj Close'],
            na_values='nan',
            parse_dates=True
            )
        df_temp = df_temp.rename(columns={'Adj Close':ticker})
        df = df.join(df_temp)
        if ticker == 'SPY':
            df = df.dropna(subset=['SPY'])
    
    return df

def get_rolling_mean(df, window=20):
    return df.rolling(window=window).mean()

def get_rolling_std(df, window=20):
    return df.rolling(window=window).std()

def get_bollinger_bands(rm, rstd):
    # Array Operations
    upper_band = rm + (rstd * 2)
    lower_band = rm - (rstd * 2)
    return upper_band, lower_band

# Executing Functions

def bollinger_bands():
    # Adjust Time Period
    start_date = '2012-01-01'
    end_date = '2012-12-31'
    ##

    # Adjust Tickers
    tickers = ['SPY']
    ##

    dates = pd.date_range(start_date, end_date)

    df = get_data(tickers, dates)


    ## Computing Rolling Mean
    rm_SPY = get_rolling_mean(df['SPY'], window=20)

    ## Compute Rolling Standard Deviation
    rstd_SPY = get_rolling_std(df['SPY'], window=20)

    ## Compute Upper and Lower Bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    ## Plot Values
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling Mean', ax=ax)
    upper_band.plot(label='Upper Band', ax=ax)
    lower_band.plot(label='Lower Band', ax=ax)

    ## Set Labels
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    bollinger_bands()

