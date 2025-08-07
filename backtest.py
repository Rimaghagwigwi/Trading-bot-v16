import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import time

class RSIBacktester:
    def __init__(self, symbol="BTCUSDT", initial_capital=10000):
        self.symbol = symbol
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0  # 0 = no position, 1 = long position
        self.position_size = 0  # Number of units held
        self.entry_price = 0
        self.trades = []
        self.portfolio_history = []
        
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI (Relative Strength Index)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Avoid division by zero
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_EMA(self, prices: pd.DataFrame, period=200):
        """Calculate Exponential Moving Average (EMA)"""
        return prices.ewm(span=period, adjust=False).mean()
    
    def get_binance_data(self, interval="1h", limit=1000):
        """Fetch data from Binance API"""
        base_url = "https://api.binance.com/api/v3/klines"
        
        # Calculate start date (2 years ago)
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=730)).timestamp() * 1000)
        
        print(f"Fetching data for {self.symbol} from Binance API...")
        
        all_data = []
        current_start = start_time
        
        try:
            while current_start < end_time:
                params = {
                    'symbol': self.symbol,
                    'interval': interval,
                    'startTime': current_start,
                    'limit': limit
                }
                
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                if not data:
                    break
                
                all_data.extend(data)
                current_start = data[-1][0] + 1  # Take timestamp of last element + 1ms
                
                print(f"Fetched {len(data)} candles, total: {len(all_data)}")
                time.sleep(0.1)  # Avoid overloading the API
                
                # Stop if less than limit (end of data)
                if len(data) < limit:
                    break
            
            # Convert to DataFrame
            df = pd.DataFrame(all_data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Clean and format data
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Convert OHLCV columns to float
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Rename columns to standard format
            df.rename(columns={
                'open': 'Open',
                'high': 'High', 
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            }, inplace=True)
            
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
            print(f"Formatted data: {len(df)} candles fetched")
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
        except Exception as e:
            print(f"Data processing error: {e}")
            return None
    
    def save_data_to_csv(self, data, interval="1h"):
        """Save market data to CSV with specific name"""
        filename = f"{self.symbol}_{interval}.csv"
        try:
            data.to_csv(filename)
            print(f"Data saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving data: {e}")
            return None
    
    def load_data_from_csv(self, interval="1h"):
        """Load data from CSV"""
        import os
        filename = f"{self.symbol}_{interval}.csv"
        try:
            if os.path.exists(filename):
                data = pd.read_csv(filename, index_col=0, parse_dates=True)
                print(f"Data loaded from {filename}")
                return data
            else:
                print(f"File {filename} not found")
                return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def execute_strategy(self, data):
        """Execute RSI-based trading strategy"""
        # Calculate RSI
        data['RSI'] = self.calculate_rsi(data['Close'])
        # OPTIONAL: Calculate EMA for trend confirmation
        # data['EMA'] = self.calculate_EMA(data['Close'], period=50)
        
        # Trading signals
        data['Signal'] = 0
        data.loc[data['RSI'] < 30, 'Signal'] = 1  # Buy signal
        data.loc[data['RSI'] > 70, 'Signal'] = -1  # Sell signal
        
        print("Executing strategy...")
        
        trades_count = 0
        for timestamp, row in data.iterrows():
            if pd.isna(row['RSI']):
                continue
                
            current_price = row['Close']
            rsi = row['RSI']
            signal = row['Signal']
            
            # Trading logic
            if signal == 1 and self.position == 0:  # Buy when RSI < 30
                self.position = 1
                self.entry_price = current_price
                # Invest all available capital
                self.position_size = self.capital / current_price
                
                trade = {
                    'timestamp': timestamp,
                    'type': 'BUY',
                    'price': current_price,
                    'rsi': rsi,
                    'position_size': self.position_size,
                    'capital_invested': self.capital
                }
                self.trades.append(trade)
                trades_count += 1
                
            elif signal == -1 and self.position == 1:  # Sell when RSI > 70
                # Calculate new capital value
                new_capital = self.position_size * current_price
                profit_loss = new_capital - self.capital
                profit_pct = (profit_loss / self.capital) * 100
                
                trade = {
                    'timestamp': timestamp,
                    'type': 'SELL',
                    'price': current_price,
                    'rsi': rsi,
                    'position_size': self.position_size,
                    'capital_after': new_capital,
                    'profit_loss': profit_loss,
                    'profit_pct': profit_pct
                }
                self.trades.append(trade)
                
                # Update capital and reset position
                self.capital = new_capital
                self.position = 0
                self.position_size = 0
                self.entry_price = 0
                
                trades_count += 1
            
            # Record portfolio history
            if self.position == 1:
                current_value = self.position_size * current_price
            else:
                current_value = self.capital
                
            self.portfolio_history.append({
                'timestamp': timestamp,
                'portfolio_value': current_value,
                'rsi': rsi,
                'price': current_price,
                'position': self.position
            })
        
        print(f"Strategy finished: {len(self.trades)} signals generated")
    
    def display_trades_history(self):
        """Display trade history in console"""
        if not self.trades:
            print("No trades executed")
            return
        
        print("\n" + "="*85)
        print("TRADE HISTORY")
        print("="*85)
        print(f"{'Date/Time':<20} {'Type':<6} {'Price':<12} {'RSI':<8} {'P&L':<12} {'P&L%':<8}")
        print("-" * 85)
        
        for trade in self.trades:
            date_str = trade['timestamp'].strftime('%Y-%m-%d %H:%M')
            trade_type = trade['type']
            price = f"{trade['price']:.4f}"
            rsi = f"{trade['rsi']:.1f}"
            
            if trade_type == 'SELL':
                pnl = f"{trade['profit_loss']:+.2f}$"
                pnl_pct = f"{trade['profit_pct']:+.2f}%"
            else:
                pnl = "-"
                pnl_pct = "-"
            
            print(f"{date_str:<20} {trade_type:<6} {price:<12} {rsi:<8} {pnl:<12} {pnl_pct:<8}")
        
        print("-" * 85)
        # Save trade history to CSV
        trades_df = pd.DataFrame(self.trades)
        trades_df['timestamp'] = trades_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        trades_df.to_csv(f"{self.symbol}_trades_history.csv", index=False)
    
    def calculate_and_display_metrics(self):
        """Calculate and display performance metrics"""
        if not self.trades:
            print("No trades executed")
            return
        
        # Calculate final portfolio value
        if self.position == 1 and self.portfolio_history:
            # If still in a position, use last price
            final_value = self.portfolio_history[-1]['portfolio_value']
        else:
            final_value = self.capital
        
        # Metrics calculation
        sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        
        total_completed_trades = len(sell_trades)
        if total_completed_trades > 0:
            profitable_trades = len([t for t in sell_trades if t['profit_loss'] > 0])
            losing_trades = total_completed_trades - profitable_trades
            win_rate = (profitable_trades / total_completed_trades) * 100
            avg_profit = sum([t['profit_loss'] for t in sell_trades]) / total_completed_trades
            
            # Best and worst trade
            profits = [t['profit_loss'] for t in sell_trades]
            best_trade = max(profits)
            worst_trade = min(profits)
        else:
            profitable_trades = losing_trades = 0
            win_rate = avg_profit = best_trade = worst_trade = 0
        
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100
        
        print("\n" + "="*60)
        print(f"BACKTESTING RESULTS - {self.symbol}")
        print("="*60)
        print(f"Initial capital:       ${self.initial_capital:>10,.2f}")
        print(f"Final value:           ${final_value:>10,.2f}")
        print(f"Total profit/loss:     ${final_value - self.initial_capital:>+10,.2f}")
        print(f"Total return:          {total_return:>10.2f}%")
        print("-" * 60)
        print(f"Signals generated:     {len(self.trades):>10}")
        print(f"Completed trades:      {total_completed_trades:>10}")
        
        if total_completed_trades > 0:
            print(f"Winning trades:        {profitable_trades:>10}")
            print(f"Losing trades:         {losing_trades:>10}")
            print(f"Win rate:              {win_rate:>10.1f}%")
            print(f"Avg profit/trade:      ${avg_profit:>+10.2f}")
            print(f"Best trade:            ${best_trade:>+10.2f}")
            print(f"Worst trade:           ${worst_trade:>+10.2f}")
        
        # Current position
        if self.position == 1:
            print(f"Current position:      LONG ({self.position_size:.4f} units)")
        else:
            print(f"Current position:      No position")
        
        # Show trade history
        if self.trades:
            self.display_trades_history()
        
        # Return metrics for final summary
        return {
            'symbol': self.symbol,
            'final_value': final_value,
            'total_return': total_return,
            'total_trades': total_completed_trades,
            'win_rate': win_rate,
            'profitable_trades': profitable_trades
        }
    
    def run_backtest(self, use_saved_data=False, interval="1h"):
        """Run full backtest"""
        print("Starting RSI backtest...")
        print(f"Symbol: {self.symbol}")
        print(f"Initial capital: ${self.initial_capital:,.2f}")
        print(f"Strategy: Buy RSI < 30, Sell RSI > 70")
        print(f"Timeframe: {interval}")
        print("-" * 60)
        
        # Fetch or load data
        if use_saved_data:
            data = self.load_data_from_csv(interval)
            if data is None:
                print("Loading from saved data failed, fetching from API...")
                data = self.get_binance_data(interval)
        else:
            # Check if data exists first
            data = self.load_data_from_csv(interval)
            if data is None:
                data = self.get_binance_data(interval)
            else:
                print(f"Using existing data for {self.symbol}")
        
        if data is None or data.empty:
            print("Unable to fetch data")
            return None
        
        # Save data if fetched from API
        if not use_saved_data:
            self.save_data_to_csv(data, interval)
        
        # Execute strategy
        self.execute_strategy(data)
        
        # Display results and return metrics
        return self.calculate_and_display_metrics()

# Example usage
if __name__ == "__main__":
    # Test with multiple cryptos
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
    all_results = []
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n{'='*60}")
        print(f"BACKTESTING {i}/{len(symbols)} - {symbol}")
        print(f"{'='*60}")
        
        # Create backtester instance
        backtester = RSIBacktester(symbol=symbol, initial_capital=10000)
        
        # Run backtest
        result = backtester.run_backtest(use_saved_data=False, interval="1h")
        
        if result:
            all_results.append(result)
        
        # Pause between requests to respect API limits
        if symbol != symbols[-1]:
            print(f"\nPausing 3 seconds before next backtest...")
            time.sleep(3)
    
    # Display final summary
    if all_results:
        print(f"\n{'='*80}")
        print("FINAL BACKTEST SUMMARY")
        print(f"{'='*80}")
        print(f"{'Crypto':<10} {'Return':<12} {'Trades':<8} {'Win Rate':<10} {'Profit':<12}")
        print("-" * 80)
        
        total_initial = 0
        total_final = 0
        
        for result in all_results:
            initial_capital = 10000
            final_value = result['final_value']
            profit = final_value - initial_capital
            
            total_initial += initial_capital
            total_final += final_value
            
            print(f"{result['symbol']:<10} {result['total_return']:>+8.2f}%   {result['total_trades']:>5}   {result['win_rate']:>6.1f}%   ${profit:>+9.2f}")
        
        overall_return = ((total_final - total_initial) / total_initial) * 100
        total_profit = total_final - total_initial
        
        print("-" * 80)
        print(f"{'TOTAL':<10} {overall_return:>+8.2f}%   {sum(r['total_trades'] for r in all_results):>5}   {sum(r['profitable_trades'] for r in all_results)/sum(r['total_trades'] for r in all_results)*100 if sum(r['total_trades'] for r in all_results) > 0 else 0:>6.1f}%   ${total_profit:>+9.2f}")
        print(f"Total initial portfolio: ${total_initial:,.2f}")
        print(f"Total final portfolio:   ${total_final:,.2f}")