import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fredapi import Fred
from statsmodels.tsa.api import VAR
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.vector_ar.var_model import VAR


# List of major bank stock tickers
bank_tickers = ['JPM', 'BAC', 'WFC', 'C', 'GS']

# Download historical stock price data
start_date = '2000-01-01'
end_date = '2022-12-31'
bank_data = yf.download(bank_tickers, start=start_date, end=end_date)['Adj Close']

# Set your FRED API key
fred_api_key = '4aa9edf824639f4000ca73c83da6f512'
fred = Fred(api_key=fred_api_key)

# Download GDP data
gdp_data = fred.get_series('GDP', start_date, end_date)

# Assign a name to the GDP series
gdp_data.name = 'GDP'

# Merge the datasets
data = bank_data.join(gdp_data, how='outer')

# Fill missing values using forward fill
data.fillna(method='ffill', inplace=True)

# Fill any remaining missing values using backward fill
data.fillna(method='bfill', inplace=True)

def remove_outliers_iqr(data, column_names, factor=1.5):
    for col in column_names:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
    return data

# List of columns to check for outliers
columns_to_check = ['JPM', 'BAC', 'WFC', 'C', 'GS', 'GDP']

# Remove outliers
data = remove_outliers_iqr(data, columns_to_check)

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Plot time series data for major banks
bank_data.plot(subplots=True, title='Major Banks Stock Prices')
plt.show()

# Plot time series data for GDP
gdp_data.plot(title='GDP')
plt.show()

# Calculate the correlation matrix
correlation_matrix = data.corr()

# Visualize the correlation matrix using a heatmap
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.show()

# Calculate monthly returns
monthly_returns = data.pct_change().dropna()

# Split the dataset into training and testing sets
print("splitting data for train and test")
split_index = int(0.8 * len(monthly_returns))
train_data = monthly_returns[:split_index]
test_data = monthly_returns[split_index:]


# Normalize the data
print("Normalize the data")
train_mean = train_data.mean()
train_std = train_data.std()

train_data_normalized = (train_data - train_mean) / train_std
test_data_normalized = (test_data - train_mean) / train_std


# Create and fit the VAR model
print("Creating model")
model = VAR(train_data_normalized)
model_fit = model.fit(maxlags=12, ic='aic')


# Forecast the future returns
print("Future returns")
forecast = model_fit.forecast(train_data_normalized.values, steps=len(test_data))


# Calculate the safety scores
print("Calculating safety scores")
forecast_df = pd.DataFrame(forecast, index=test_data.index, columns=test_data.columns)

# Remove the GDP column from the forecast_df
forecast_df = forecast_df.drop(columns=['GDP'])


forecast_std = forecast_df.std()
safety_scores = 1 / forecast_std

print("Safety scores:")
print(safety_scores.sort_values(ascending=False))


# Calculate the Mean Absolute Error for each bank
mae_scores = {}
for ticker in bank_tickers:
    ticker_col = f"{ticker}"
    mae_scores[ticker] = mean_absolute_error(test_data[ticker_col], forecast_df[ticker_col])

print("Mean Absolute Error scores:")
print(mae_scores)


# Calculate the safety scores
forecast_std = forecast_df.std()
safety_scores = 1 / forecast_std

print("Safety scores:")
print(safety_scores.sort_values(ascending=False))


# Visualize the actual vs. predicted stock prices for each bank
for ticker in bank_tickers:
    ticker_col = f"{ticker}"
    plt.figure(figsize=(12, 6))
    plt.plot(test_data[ticker_col], label='Actual')
    plt.plot(forecast_df[ticker_col], label='Predicted', linestyle='--')
    plt.title(f"{ticker} - Actual vs. Predicted Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()
  

# Visualize the safety scores as a bar plot
plt.figure(figsize=(10, 5))
safety_scores.sort_values(ascending=False).plot(kind='bar')
plt.title("Bank Safety Scores")
plt.xlabel("Bank")
plt.ylabel("Safety Score")
plt.show()




