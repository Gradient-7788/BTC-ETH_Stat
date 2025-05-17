def strat(data):
    """
    Simplified strategy function to generate trading signals based on Supertrend, regime, and MACD for entry,
    and Heikin-Ashi and regime for exit.

    Parameters:
    - data: DataFrame containing market data with calculated indicators and regimes.
            Assumes 'macd', 'macd_signal', and 'macd_histogram' are pre-calculated.

    Returns:
    - final_data: DataFrame with generated signals and trade types.
    """

    # Initialize signals and trade_type column
    data['signals'] = 0
    data['trade_type'] = " "

    # Helper function to close positions
    def close_position(stoploss=False):
        """
        Closes the current position and updates the necessary variables.

        Parameters:
        - stoploss: Boolean indicating if the closure is due to a stop-loss hit.
        """
        nonlocal current_position, entry_price, entry_date, highest_since_entry, lowest_since_entry

        if current_position == 1:
            data.at[i+1, 'signals'] = -1  # Signal to close long position
        elif current_position == -1:
            data.at[i+1, 'signals'] = 1  # Signal to close short position
        data.at[i+1, 'trade_type'] = 'close'
        current_position = 0  # Reset position to no position
        entry_price = None  # Reset entry price
        entry_date = None  # Reset entry date
        highest_since_entry = None  # Reset highest price since entry
        lowest_since_entry = None  # Reset lowest price since entry

        return

    # Initialize Trading Variables
    entry_price = None  # Price at which the position was entered
    entry_date = None  # Timestamp when the position was entered
    current_position = 0  # 0 = no position, 1 = long position, -1 = short position
    highest_since_entry = None  # Highest price since entering a long position
    lowest_since_entry = None  # Lowest price since entering a short position

    # Strategy Parameters
    TRAILING_STOPLOSS_PCT_long = 0.125  # trailing stop-loss 
    TRAILING_STOPLOSS_PCT_short =0.05

    # Main loop to process data
    for i in range(len(data)):  
        current_price = data['prev_close'].iloc[i]
        current_time = data.index[i]

        # # Ensure open positions are closed at the end of the data
        # if i == len(data) - 1 and current_position != 0:
        #     close_position()
        #     continue

        # Handle trailing stop-loss for long positions
        if current_position == 1:
            highest_since_entry = max(highest_since_entry or current_price, current_price)
            trailing_stop_price = highest_since_entry * (1 - TRAILING_STOPLOSS_PCT_long)

            if current_price <= trailing_stop_price:
                close_position(stoploss=True)
                continue

        # Handle trailing stop-loss for short positions
        elif current_position == -1:
            lowest_since_entry = min(lowest_since_entry or current_price, current_price)
            trailing_stop_price = lowest_since_entry * (1 + TRAILING_STOPLOSS_PCT_short)

            if current_price >= trailing_stop_price:
                close_position(stoploss=True)
                continue

        # LONG ENTRY CONDITIONS 
        if current_position == 0 :
            if (
                (data['regime'].iloc[i] == 'bullish' and 
                data['macd_histogram'].iloc[i] > 0 and data['macd_histogram'].iloc[i] > data['macd_histogram'].iloc[i-1] and
                data['prev_close'].iloc[i] > data['bb_upper'].iloc[i] and
                # data['adx'].iloc[i] > 15 and data['plus_di'].iloc[i] > data['minus_di'].iloc[i] and
                data['rsi'].iloc[i] > 70) ##
                ):
                data.at[i+1, 'signals'] = 1  # Signal for long entry
                data.at[i+1, 'trade_type'] = 'long'
                current_position = 1  # Update current position to long
                entry_price = current_price  # Set entry price
                entry_date = current_time  # Set entry time
                highest_since_entry = current_price  # Initialize highest price since entry

            # SHORT ENTRY CONDITIONS 
            elif (
                (data['regime'].iloc[i] == 'bearish' and  
                data['macd_histogram'].iloc[i] < 0 and data['macd_histogram'].iloc[i] < data['macd_histogram'].iloc[i-1] and 
                data['prev_close'].iloc[i] < data['bb_lower'].iloc[i] and
                data['adx'].iloc[i] > 35 and data['plus_di'].iloc[i] < data['minus_di'].iloc[i] and
                data['rsi'].iloc[i] < 60

                
                ) 
            ):
                data.at[i+1, 'signals'] = -1  # Signal for short entry
                data.at[i+1, 'trade_type'] = 'short'
                current_position = -1  # Update current position to short
                entry_price = current_price  # Set entry price
                entry_date = current_time  # Set entry time
                lowest_since_entry = current_price  # Initialize lowest price since entry

        # LONG EXIT CONDITIONS 
        elif current_position == 1 and (
            (data['regime'].iloc[i] == 'bearish' and 
            data['supertrend_direction'].iloc[i] == -1 and 
            data['prev_close'].iloc[i] < data['bb_lower'].iloc[i] and
            data['macd_histogram'].iloc[i] < 0 ) or 
            (data['macd_histogram'].iloc[i] < 0 and data['rsi'].iloc[i] > 90 )
            
            ):
            close_position(stoploss=False)  # Close long position

        # SHORT EXIT CONDITIONS 
        elif current_position == -1 and (
            (data['regime'].iloc[i] =='bullish' and
            data['supertrend_direction'].iloc[i] == 1 and
            data['prev_close'].iloc[i] > data['bb_upper'].iloc[i]  and
            data['macd_histogram'].iloc[i] > 0 ) or
            (data['macd_histogram'].iloc[i] > 0 and data['rsi'].iloc[i] <20 ) 
            ):
            close_position(stoploss=False)  # Close short position

    return data


def perform_backtest(csv_file_path):
    """
    Perform backtesting using the untrade SDK.

    Parameters:
    - csv_file_path (str): Path to the CSV file containing historical price data and signals.

    Returns:
    - result (generator): Generator object that yields backtest results.
    """
    # Create an instance of the untrade client
    client = Client()

    # Perform backtest using the provided CSV file path
    result = client.backtest(
        jupyter_id="team_akatsuki",  
        file_path=csv_file_path,
        leverage=1,  
    )

    return result
