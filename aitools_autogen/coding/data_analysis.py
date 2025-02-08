# To accomplish the tasks you've outlined, we'll split the work into two Python scripts for better organization and clarity. The first script will handle data loading, cleaning, and the calculations for total revenue and units sold per product, as well as the average monthly revenue per store. The second script will focus on generating the line plot for the trend of total revenue over time.

### Script 1: Data Loading, Cleaning, and Calculations


# filename: data_analysis.py

import pandas as pd

def read_data(file_path):
    """Reads CSV data into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print("File not found.")
        return None

def clean_data(df):
    """Removes records with missing values."""
    clean_df = df.dropna()
    return clean_df

def calculate_totals(df):
    """Calculates total revenue and units sold per product."""
    totals = df.groupby('Product ID').agg({'Units Sold': 'sum', 'Revenue': 'sum'}).reset_index()
    return totals

def calculate_average_monthly_revenue(df):
    """Calculates average monthly revenue per store."""
    # Convert 'Date' to datetime and extract year and month for grouping
    df['Date'] = pd.to_datetime(df['Date'])
    df['YearMonth'] = df['Date'].dt.to_period('M')
    average_revenue = df.groupby(['Store ID', 'YearMonth']).agg({'Revenue': 'mean'}).reset_index()
    return average_revenue

def main():
    file_path = 'monthly_sales.csv'
    df = read_data(file_path)
    if df is not None:
        df = clean_data(df)
        totals = calculate_totals(df)
        average_revenue = calculate_average_monthly_revenue(df)
        
        # Save the results to text files
        totals.to_csv('product_totals.csv', index=False)
        average_revenue.to_csv('average_monthly_revenue.csv', index=False)
        print("Results saved.")

if __name__ == "__main__":
    main()