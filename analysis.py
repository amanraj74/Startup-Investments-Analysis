import pandas as pd

# Load dataset
df = pd.read_csv('investments.csv')
print("Original Dataset:")
print(df.head())
print(df.info())

# Clean data
# Replace '-' with 0 in funding_total_usd
df['funding_total_usd'] = df['funding_total_usd'].replace('-', 0)
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce').fillna(0)

# Fill missing values
df['country_code'] = df['country_code'].fillna('Unknown')
df['market'] = df['market'].fillna('Unknown')
df['status'] = df['status'].fillna('Unknown')
df['category_list'] = df['category_list'].fillna('Unknown')

# Standardize market names
df['market'] = df['market'].str.strip().str.title()

# Fix country code (e.g., EST to EE)
df['country_code'] = df['country_code'].replace('EST', 'EE')

# Remove duplicates
df = df.drop_duplicates(subset='permalink', keep='first')

# Convert dates
df['founded_at'] = pd.to_datetime(df['founded_at'], errors='coerce')
df['first_funding_at'] = pd.to_datetime(df['first_funding_at'], errors='coerce')
df['last_funding_at'] = pd.to_datetime(df['last_funding_at'], errors='coerce')

# Save cleaned dataset
df.to_csv('cleaned_investments.csv', index=False)
print("\nCleaned Dataset:")
print(df.head())