import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page title
st.title("Startup Investments Dashboard")

# Load cleaned data
try:
    df = pd.read_csv('cleaned_investments.csv')
except FileNotFoundError:
    st.error("The file 'cleaned_investments.csv' was not found. Please ensure it is in the project directory.")
    st.stop()

# Strip whitespace from column names immediately
df.columns = df.columns.str.strip()

# Convert founded_year to numeric, coerce errors to NaN, then fill with 0 or drop
df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce').fillna(0).astype(int)

# Sidebar for filters
st.sidebar.header("Filters")
markets = st.sidebar.multiselect("Select Markets", options=df['market'].unique(), default=df['market'].unique()[:5])
countries = st.sidebar.multiselect("Select Countries", options=df['country_code'].unique(), default=['USA', 'GBR'])
status = st.sidebar.multiselect("Select Status", options=df['status'].unique(), default=df['status'].unique())

# Filter data
filtered_df = df[
    df['market'].isin(markets) &
    df['country_code'].isin(countries) &
    df['status'].isin(status)
]

# Check if filtered_df is empty
if filtered_df.empty:
    st.error("No data available for the selected filters. Please adjust your selections.")
else:
    # Insight 1: Top Markets by Funding
    st.header("Top Markets by Total Funding")
    top_markets = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_markets.values, y=top_markets.index, ax=ax)
    ax.set_title('Top 10 Markets by Total Funding (USD)')
    ax.set_xlabel('Total Funding (USD)')
    ax.set_ylabel('Market')
    st.pyplot(fig)

    # Insight 2: Funding by Status
    st.header("Funding Distribution by Status")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='status', y='funding_total_usd', data=filtered_df, ax=ax)
    ax.set_title('Funding Distribution by Startup Status')
    ax.set_xlabel('Status')
    ax.set_ylabel('Funding (USD)')
    ax.set_yscale('log')
    st.pyplot(fig)

    # Insight 3: Top Countries
    st.header("Top Countries by Number of Startups")
    top_countries = filtered_df['country_code'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax)
    ax.set_title('Top 10 Countries by Number of Startups')
    ax.set_xlabel('Number of Startups')
    ax.set_ylabel('Country')
    st.pyplot(fig)

    # Insight 4: Funding Trends
    st.header("Funding Trends Over Time")
    funding_by_year = filtered_df.groupby('founded_year')['funding_total_usd'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    funding_by_year.plot(kind='line', ax=ax)
    ax.set_title('Total Funding by Founded Year')
    ax.set_xlabel('Founded Year')
    ax.set_ylabel('Total Funding (USD)')
    st.pyplot(fig)

    # Insight 5: Funding Rounds vs. Funding
    st.header("Funding Rounds vs. Total Funding")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='funding_rounds', y='funding_total_usd', data=filtered_df, ax=ax)
    ax.set_title('Funding Rounds vs. Total Funding')
    ax.set_xlabel('Number of Funding Rounds')
    ax.set_ylabel('Total Funding (USD)')
    ax.set_yscale('log')
    st.pyplot(fig)

    # Insight 6: Market Share
    st.header("Market Share by Number of Startups")
    top_markets_count = filtered_df['market'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(top_markets_count, labels=top_markets_count.index, autopct='%1.1f%%')
    ax.set_title('Top 5 Markets by Number of Startups')
    st.pyplot(fig)

    # Insight 7: Funding by Type
    st.header("Funding by Funding Type")
    funding_types = ['seed', 'venture', 'round_A', 'round_B', 'round_C', 'round_D']
    funding_sums = filtered_df[funding_types].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=funding_sums.index, y=funding_sums.values, ax=ax)
    ax.set_title('Total Funding by Funding Type')
    ax.set_xlabel('Funding Type')
    ax.set_ylabel('Total Funding (USD)')
    st.pyplot(fig)

    # Insight 8: Acquisition Rate
    st.header("Top Markets by Acquisition Rate")
    if 'acquired' in filtered_df['status'].unique():
        market_status = filtered_df.groupby(['market', 'status']).size().unstack(fill_value=0)
        market_status['acquired_rate'] = market_status['acquired'] / market_status.sum(axis=1)
        top_acquired = market_status['acquired_rate'].sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_acquired.values, y=top_acquired.index, ax=ax)
        ax.set_title('Top 5 Markets by Acquisition Rate')
        ax.set_xlabel('Acquisition Rate')
        ax.set_ylabel('Market')
        st.pyplot(fig)
    else:
        st.warning("No startups with 'acquired' status found in filtered data to calculate acquisition rates.")