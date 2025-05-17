@classmethod
        def rolling_hurst_exponent(cls, window: int = 100):
            """Calculate Hurst Exponent in a rolling window."""
            def hurst_exponent(ts):
                if len(ts) < 20 or np.any(np.isnan(ts)) or np.std(ts) == 0:
                    return np.nan
                try:
                    H, _, _ = compute_Hc(ts)
                    return H if 0 <= H <= 1 else np.nan
                except:
                    return np.nan
            cls.data['hurst'] = cls.data['prev_close'].rolling(window=window, min_periods=window).apply(hurst_exponent, raw=True)

@classmethod
        def calculate_cusum(cls, window: int = 4, delta: float = 0.8):
            """Calculate CUSUM indicators."""
            rolling_sigma = cls.data['prev_close'].rolling(window=window).std()
            k = delta * rolling_sigma.fillna(0)
            price = cls.data['prev_close'].values
            mu = cls.data['prev_filtered_close'].values
            S_hi = np.zeros(len(cls.data))
            S_lo = np.zeros(len(cls.data))
            for i in range(1, len(cls.data)):
                S_hi[i] = max(0, S_hi[i-1] + (price[i] - mu[i] - k.iloc[i]))
                S_lo[i] = max(0, S_lo[i-1] + (-price[i] + mu[i] - k.iloc[i]))
            cls.data['cusum_hi'] = S_hi
            cls.data['cusum_lo'] = S_lo

@classmethod
        def calculate_fdi(cls, window: int = 35):
            """Calculate Fractal Dimension Index."""
            def fractal_dimension(series):
                n = len(series)
                if n <= 1 or np.all(np.isnan(series)):
                    return np.nan
                L = np.sum(np.abs(np.diff(series)))
                d = np.max(np.abs(series - series[0]))
                return np.log(n) / (np.log(n) + np.log(d / L)) if L != 0 and d != 0 else np.nan
            cls.data['fdi'] = cls.data['prev_filtered_close'].rolling(window=window, min_periods=window).apply(fractal_dimension, raw=True)

@classmethod
        def calculate_supertrend(cls, atr_length=14, factor=3.0):
            """Calculate Supertrend indicator."""
            cls.data['tr'] = np.maximum(
                cls.data['prev_high'] - cls.data['prev_low'],
                np.maximum(
                    abs(cls.data['prev_high'] - cls.data['prev_close'].shift(1)),
                    abs(cls.data['prev_low'] - cls.data['prev_close'].shift(1))
                )
            )
            cls.data['atr'] = cls.data['tr'].rolling(window=atr_length).mean()
            hl2 = (cls.data['prev_high'] + cls.data['prev_low']) / 2
            upper_band = hl2 + (factor * cls.data['atr'])
            lower_band = hl2 - (factor * cls.data['atr'])
            supertrend = [0] * len(cls.data)
            direction = [1] * len(cls.data)
            for i in range(1, len(cls.data)):
                if cls.data['prev_close'].iloc[i] > upper_band.iloc[i-1]:
                    supertrend[i] = lower_band.iloc[i]
                    direction[i] = -1
                elif cls.data['prev_close'].iloc[i] < lower_band.iloc[i-1]:
                    supertrend[i] = upper_band.iloc[i]
                    direction[i] = 1
                else:
                    supertrend[i] = supertrend[i-1]
                    direction[i] = direction[i-1]
            cls.data['supertrend'] = supertrend
            cls.data['supertrend_direction'] = direction

@classmethod
        def calculate_rsi(cls, lengths=[14, 7]):
            """Calculate RSI for multiple lengths."""
            for length in lengths:
                delta = cls.data['prev_close'].diff()
                gain = np.where(delta > 0, delta, 0)
                loss = np.where(delta < 0, -delta, 0)
                avg_gain = pd.Series(gain, index=cls.data.index).rolling(window=length, min_periods=1).mean()
                avg_loss = pd.Series(loss, index=cls.data.index).rolling(window=length, min_periods=1).mean()
                rs = avg_gain / avg_loss
                cls.data[f'rsi_{length}'] = 100 - (100 / (1 + rs))

@classmethod
        def calculate_macd(cls, fast_length=6, slow_length=12, signal_length=18):
            """Calculate MACD indicator."""
            fast_ema = cls.data['prev_close'].ewm(span=fast_length, adjust=False).mean()
            slow_ema = cls.data['prev_close'].ewm(span=slow_length, adjust=False).mean()
            cls.data['macd'] = fast_ema - slow_ema
            cls.data['macd_signal'] = cls.data['macd'].ewm(span=signal_length, adjust=False).mean()
            cls.data['macd_histogram'] = cls.data['macd'] - cls.data['macd_signal']

@classmethod
        def calculate_bollinger_bands(cls, window: int = 14, num_std: float = 2.5):
            """Calculate Bollinger Bands."""
            cls.data['bb_middle'] = cls.data['prev_close'].rolling(window=window).mean()
            rolling_std = cls.data['prev_close'].rolling(window=window).std()
            cls.data['bb_upper'] = cls.data['bb_middle'] + (rolling_std * num_std)
            cls.data['bb_lower'] = cls.data['bb_middle'] - (rolling_std * num_std)

@classmethod
        def calculate_atr(cls, period: int = 21):
            """Calculate Average True Range (ATR)."""
            # True Range (TR) is the maximum of:
            # 1. Current high - current low
            # 2. abs(current high - previous close)
            # 3. abs(current low - previous close)
            cls.data['prev_close'] = cls.data['close'].shift(1)
        
            high_low = cls.data['high'] - cls.data['low']
            high_prev_close = abs(cls.data['high'] - cls.data['prev_close'])
            low_prev_close = abs(cls.data['low'] - cls.data['prev_close'])
        
            cls.data['tr'] = np.maximum.reduce([high_low, high_prev_close, low_prev_close])
        
            # ATR using Wilder's smoothing (similar to EMA with adjust=False)
            cls.data['atr'] = cls.data['tr'].ewm(span=period, adjust=False).mean()
