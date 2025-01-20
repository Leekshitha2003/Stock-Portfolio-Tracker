import yfinance as yf
import pandas as pd

class StockPortfolio:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=["Ticker", "Shares", "Average Price"])

    def add_stock(self, ticker, shares, average_price):
        ticker = ticker.upper()
        if ticker in self.portfolio["Ticker"].values:
            print(f"{ticker} is already in your portfolio.")
        else:
            new_stock = {"Ticker": ticker, "Shares": shares, "Average Price": average_price}
            self.portfolio = pd.concat([self.portfolio, pd.DataFrame([new_stock])], ignore_index=True)
            print(f"Added {ticker} to your portfolio.")

    def remove_stock(self, ticker):
        ticker = ticker.upper()
        if ticker in self.portfolio["Ticker"].values:
            self.portfolio = self.portfolio[self.portfolio["Ticker"] != ticker]
            print(f"Removed {ticker} from your portfolio.")
        else:
            print(f"{ticker} is not in your portfolio.")

    def track_performance(self):
        if self.portfolio.empty:
            print("Your portfolio is empty.")
            return

        performance = []
        for _, stock in self.portfolio.iterrows():
            ticker = stock["Ticker"]
            shares = stock["Shares"]
            avg_price = stock["Average Price"]

            try:
                stock_data = yf.Ticker(ticker).history(period="1d")
                if stock_data.empty:
                    print(f"No data found for {ticker}. Skipping.")
                    continue
                
                current_price = stock_data["Close"].iloc[-1]
                market_value = shares * current_price
                profit_loss = (current_price - avg_price) * shares
                
                performance.append({
                    "Ticker": ticker,
                    "Shares": shares,
                    "Average Price": avg_price,
                    "Current Price": current_price,
                    "Market Value": market_value,
                    "Profit/Loss": profit_loss
                })
            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")

        performance_df = pd.DataFrame(performance)
        print("\nPortfolio Performance:")
        print(performance_df.to_string(index=False))

    def show_portfolio(self):
        if self.portfolio.empty:
            print("Your portfolio is empty.")
        else:
            print("\nCurrent Portfolio:")
            print(self.portfolio.to_string(index=False))

# Example usage
def main():
    portfolio = StockPortfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Performance")
        print("4. Show Portfolio")
        print("5. Exit")
        try:
            choice = input("Enter your choice: ")

            if choice == "1":
                ticker = input("Enter stock ticker: ")
                try:
                    shares = int(input("Enter number of shares: "))
                    average_price = float(input("Enter average price: "))
                    portfolio.add_stock(ticker, shares, average_price)
                except ValueError:
                    print("Invalid input. Please enter valid numbers for shares and average price.")
            elif choice == "2":
                ticker = input("Enter stock ticker to remove: ")
                portfolio.remove_stock(ticker)
            elif choice == "3":
                portfolio.track_performance()
            elif choice == "4":
                portfolio.show_portfolio()
            elif choice == "5":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
