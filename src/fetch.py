import csv
import os
import yfinance as yf

def fetch_data():

    ticker = yf.Ticker("GC=F")
    data_history = ticker.history(period="5y")

    data_gold = []
    for index, row in data_history.iterrows():
        data = {
            "Date": str(index.date()),
            "Open": float(row["Open"]),
            "High": float(row["High"]),
            "Low": float(row["Low"]),
            "Close": float(row["Close"]),
        }
        data_gold.append(data)

    print(f"Data loaded: {len(data_gold)} hari")

    os.makedirs("data", exist_ok=True)

    with open("data/gold_data.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Date", "Open", "High", "Low", "Close"]
        )
        writer.writeheader()
        writer.writerows(data_gold)

    print(f"Data saved: {len(data_gold)} rows → data/gold_data.csv")

if __name__ == "__main__":
    fetch_data()
