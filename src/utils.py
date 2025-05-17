@classmethod
        def calculate_prev_ohlcv(cls):
            """Calculate previous OHLCV columns by shifting current values."""
            cls.data['prev_open'] = cls.data['open'].shift(1)
            cls.data['prev_high'] = cls.data['high'].shift(1)
            cls.data['prev_low'] = cls.data['low'].shift(1)
            cls.data['prev_close'] = cls.data['close'].shift(1)
            cls.data['prev_volume'] = cls.data['volume'].shift(1)
            cls.data.dropna(subset=['prev_open', 'prev_high', 'prev_low', 'prev_close', 'prev_volume'], inplace=True)

@classmethod
        def initialize(cls, data: pd.DataFrame):
            """
            Initialize the class with a DataFrame.
            
            Parameters:
            - data (pd.DataFrame): DataFrame with 'open', 'high', 'low', 'close', 'volume' columns
            """
            if not all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume']):
                raise ValueError("DataFrame must contain 'open', 'high', 'low', 'close', and 'volume' columns")
            cls.data = data.copy()

@classmethod
        def identify_regimes(cls, window: int = 5, delta: float = 0.8, h_factor=1.5):

            rolling_sigma = cls.data['prev_close'].rolling(window=window).std()
            k = delta * rolling_sigma
            rolling_h = h_factor * rolling_sigma

            conditions = [
                # Bullish regime:
                ((cls.data['cusum_hi'] > rolling_h) & (cls.data['hurst'] > 0.5) & (cls.data['fdi'] <1.5)),

                # Bearish regime: 
                ((cls.data['cusum_lo'] > rolling_h) & (cls.data['hurst'] > 0.5) & (cls.data['fdi'] <1.5))
            ]
            choices = ['bullish', 'bearish']
            cls.data['regime'] = np.select(conditions, choices, default='No Trend')

def calculate_profit_growth(df):
    position = 0  # 0: no position, 1: long, -1: short
    entry_price = 0
    cumulative_return = 100  # Starting value
    returns = []

    for idx, row in df.iterrows():
        if position == 0:  # No position
            if row['signals'] == 1:  # Long entry
                position = 1
                entry_price = row['close']
            elif row['signals'] == -1:  # Short entry
                position = -1
                entry_price = row['close']
            returns.append(cumulative_return)
            
        elif position == 1:  # In long position
            if row['signals'] == -1:  # Long exit
                position = 0
                pct_change = (row['close'] - entry_price) / entry_price
                entry_price = 0
            returns.append(cumulative_return)
            
        elif position == -1:  # In short position
            if row['signals'] == 1:  # Short exit
                position = 0
                pct_change = (entry_price - row['close']) / entry_price
                cumulative_return *= (1 + pct_change)
                entry_price = 0
            returns.append(cumulative_return)
    
    return pd.Series(returns, index=df.index)

# Calculate cumulative returns
df['cumulative_returns'] = calculate_profit_growth(df)






