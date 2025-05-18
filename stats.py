# stats.py
import pandas as pd

# Load the cleaned dataset
df = pd.read_csv('cleaned_investments.csv')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Convert funding column to numeric (force non-numeric to NaN)
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')

# Drop rows with missing funding values
df = df.dropna(subset=['funding_total_usd'])
# Calculate descriptive statistics
total_startups = len(df)
average_funding = df['funding_total_usd'].mean()
status_distribution = df['status'].value_counts(normalize=True) * 100

# Print the results
print("Total Startups:", total_startups)
print(f"Average Funding (USD): ${average_funding:,.2f}")
print("Status Distribution (%):")
print(status_distribution.round(2))
