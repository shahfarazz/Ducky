

### Script 2: Generating Line Plot for Total Revenue Trend


# filename: revenue_trend_plot.py

import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_path):
    """Reads CSV data into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("File not found.")
        return None

def generate_revenue_trend_plot(df):
    """Generates a line plot showing the trend of total revenue over time."""
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    monthly_revenue = df.resample('M').sum()['Revenue']
    
    plt.figure(figsize=(10, 6))
    monthly_revenue.plot(kind='line', marker='o', linestyle='-')
    plt.title('Total Revenue Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue')
    plt.grid(True)
    plt.savefig('total_revenue_trend.png')
    plt.show()

def main():
    file_path = 'monthly_sales.csv'
    df = read_data(file_path)
    if df is not None:
        generate_revenue_trend_plot(df)

if __name__ == "__main__":
    main()