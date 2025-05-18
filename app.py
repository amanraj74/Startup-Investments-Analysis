import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

<<<<<<< HEAD
# Page configuration
st.set_page_config(page_title="Startup Investment Analysis", layout="wide")

# Title of the app
st.title("🚀 Startup Investment Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_investments.csv')
    df.columns = df.columns.str.strip()  # Clean column names
    df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce').fillna(0).astype(int)
    df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce').fillna(0)
    return df

df = load_data()

# Sidebar filters - Clean and User-Friendly
with st.sidebar:
    st.header("🔎 Filter Data")

    with st.expander("Market & Country"):
        selected_markets = st.multiselect("Select Market:", sorted(df['market'].dropna().unique()), default=sorted(df['market'].dropna().unique())[:5])
        selected_countries = st.multiselect("Select Country:", sorted(df['country_code'].dropna().unique()), default=['USA', 'GBR'])

    with st.expander("Startup Info"):
        selected_status = st.multiselect("Select Status:", df['status'].dropna().unique(), default=list(df['status'].dropna().unique()))
        selected_years = st.slider("Founded Year Range:", int(df['founded_year'].min()), int(df['founded_year'].max()), (2005, 2015))

    with st.expander("Funding"):
        min_funding = st.slider("Minimum Funding (USD):", 0, int(df['funding_total_usd'].max()), 1000000, step=500000)

# Filter the data
filtered_df = df[
    df['market'].isin(selected_markets) &
    df['country_code'].isin(selected_countries) &
    df['status'].isin(selected_status) &
    df['founded_year'].between(*selected_years) &
    (df['funding_total_usd'] >= min_funding)
]

# If no data after filtering
if filtered_df.empty:
    st.warning("No data found for the selected filters. Try adjusting them.")
    st.stop()

# Display filtered summary with clickable homepage_url if available
st.markdown("## 📊 Data Overview")
st.write("Filtered Rows:", filtered_df.shape[0])

if 'homepage_url' in filtered_df.columns:
    filtered_df_display = filtered_df.copy()
    filtered_df_display['homepage_url'] = filtered_df_display['homepage_url'].apply(
        lambda x: f"[Visit Website]({x})" if pd.notna(x) else ""
    )
    st.write(filtered_df_display.head().to_markdown(index=False), unsafe_allow_html=True)
else:
    st.write(filtered_df.head())

# Visualization 1: Top Markets by Total Funding
st.markdown("### 💡 Top Markets by Total Funding")
top_markets = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_markets.values, y=top_markets.index, palette='viridis', ax=ax1)
ax1.set_xlabel("Total Funding (USD)")
ax1.set_ylabel("Market")
st.pyplot(fig1)

# Visualization 2: Average Funding by Market
st.markdown("### 📈 Average Funding per Market")
avg_funding = filtered_df.groupby('market')['funding_total_usd'].mean().sort_values(ascending=False).head(5)
fig2, ax2 = plt.subplots()
sns.barplot(x=avg_funding.values, y=avg_funding.index, palette='Oranges', ax=ax2)
ax2.set_xlabel("Average Funding (USD)")
ax2.set_ylabel("Market")
st.pyplot(fig2)

# Visualization 3: Funding Distribution by Status
st.markdown("### 🔍 Funding Distribution by Status")
fig3, ax3 = plt.subplots()
sns.boxplot(x='status', y='funding_total_usd', data=filtered_df, ax=ax3)
ax3.set_yscale('log')
ax3.set_title("Funding by Status")
st.pyplot(fig3)

# Visualization 4: Startup Count by Country
st.markdown("### 🌍 Top Countries by Startup Count")
country_counts = filtered_df['country_code'].value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=country_counts.values, y=country_counts.index, ax=ax4)
ax4.set_title("Top Countries")
ax4.set_xlabel("Startup Count")
st.pyplot(fig4)

# Visualization 5: Funding Over Years
st.markdown("### 📆 Total Funding Over the Years")
yearly_funding = filtered_df.groupby('founded_year')['funding_total_usd'].sum()
fig5 = px.line(x=yearly_funding.index, y=yearly_funding.values, labels={'x': 'Year', 'y': 'Funding'}, title="Funding Over Time")
st.plotly_chart(fig5, use_container_width=True)

# Visualization 6: Funding Rounds vs Total Funding
st.markdown("### 🔄 Funding Rounds vs Total Funding")
fig6 = px.scatter(filtered_df, x='funding_rounds', y='funding_total_usd', color='status',
                  log_y=True, title="Funding Rounds vs Total Funding")
st.plotly_chart(fig6, use_container_width=True)

# Visualization 7: Market Share by Count
st.markdown("### 📊 Market Share (Top 5)")
top_market_counts = filtered_df['market'].value_counts().head(5)
fig7, ax7 = plt.subplots()
ax7.pie(top_market_counts, labels=top_market_counts.index, autopct='%1.1f%%', startangle=140)
ax7.set_title("Startup Share by Market")
st.pyplot(fig7)

# Visualization 8: Funding Type
st.markdown("### 💸 Funding by Type")
funding_columns = ['seed', 'venture', 'round_A', 'round_B', 'round_C', 'round_D']
funding_types_present = [col for col in funding_columns if col in filtered_df.columns]

if funding_types_present:
    funding_by_type = filtered_df[funding_types_present].sum()
    fig8, ax8 = plt.subplots()
    sns.barplot(x=funding_by_type.index, y=funding_by_type.values, palette='Blues', ax=ax8)
    ax8.set_title("Funding by Type")
    st.pyplot(fig8)

# Visualization 9: Acquisition Rate
if 'acquired' in filtered_df['status'].values:
    st.markdown("### 📈 Acquisition Rate by Market")
    status_data = filtered_df.groupby(['market', 'status']).size().unstack(fill_value=0)
    status_data['acq_rate'] = status_data['acquired'] / status_data.sum(axis=1)
    top_acq = status_data['acq_rate'].sort_values(ascending=False).head(5)
    fig9, ax9 = plt.subplots()
    sns.barplot(x=top_acq.values, y=top_acq.index, palette='Greens', ax=ax9)
    ax9.set_title("Top Acquisition Markets")
    st.pyplot(fig9)
else:
    st.info("No acquisitions found in the filtered data.")
=======
# Set page config
st.set_page_config(page_title="Startup Investments Dashboard", layout="wide")

# Title
st.title("🚀 Startup Investments Dashboard")

# Load data
try:
    df = pd.read_csv('cleaned_investments.csv')
except FileNotFoundError:
    st.error("The file 'cleaned_investments.csv' was not found. Please make sure it's in the app directory.")
    st.stop()

# Clean columns and types
df.columns = df.columns.str.strip()
df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce').fillna(0).astype(int)
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce').fillna(0)

# Sidebar filters
st.sidebar.header("📊 Filter Options")

markets = st.sidebar.multiselect("Select Markets", options=df['market'].dropna().unique(), default=df['market'].dropna().unique()[:5])
countries = st.sidebar.multiselect("Select Countries", options=df['country_code'].dropna().unique(), default=['USA', 'GBR'])
status = st.sidebar.multiselect("Select Startup Status", options=df['status'].dropna().unique(), default=df['status'].dropna().unique())
founded_year_range = st.sidebar.slider("Founded Year Range", int(df['founded_year'].min()), int(df['founded_year'].max()), (2005, 2015))
min_funding = st.sidebar.slider("Minimum Total Funding (USD)", 0, int(df['funding_total_usd'].max()), 1000000, step=500000)

# Apply filters
filtered_df = df[
    df['market'].isin(markets) &
    df['country_code'].isin(countries) &
    df['status'].isin(status) &
    (df['founded_year'].between(*founded_year_range)) &
    (df['funding_total_usd'] >= min_funding)
]

# Main layout
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Markets by Total Funding")
        top_markets = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_markets.values, y=top_markets.index, ax=ax1, palette='viridis')
        ax1.set_title('Top 10 Markets by Total Funding (USD)')
        ax1.set_xlabel('Total Funding (USD)')
        ax1.set_ylabel('Market')
        st.pyplot(fig1)

    with col2:
        st.subheader("Top Markets by Average Funding")
        avg_funding = filtered_df.groupby('market')['funding_total_usd'].mean().sort_values(ascending=False).head(5)
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=avg_funding.values, y=avg_funding.index, ax=ax2, palette='Oranges_r')
        ax2.set_title('Top 5 Markets by Average Funding')
        ax2.set_xlabel('Average Funding (USD)')
        ax2.set_ylabel('Market')
        st.pyplot(fig2)

    st.subheader("Funding Distribution by Startup Status")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='status', y='funding_total_usd', data=filtered_df, ax=ax3)
    ax3.set_yscale('log')
    ax3.set_title('Funding by Status')
    st.pyplot(fig3)

    st.subheader("Top Countries by Startup Count")
    country_counts = filtered_df['country_code'].value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=country_counts.values, y=country_counts.index, ax=ax4)
    ax4.set_title('Top 10 Countries by Number of Startups')
    st.pyplot(fig4)

    st.subheader("Funding Over Time")
    funding_by_year = filtered_df.groupby('founded_year')['funding_total_usd'].sum()
    fig5 = px.line(funding_by_year, x=funding_by_year.index, y=funding_by_year.values, labels={'x': 'Founded Year', 'y': 'Total Funding'}, title="Funding Trends Over Time")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Funding Rounds vs Total Funding")
    fig6 = px.scatter(filtered_df, x='funding_rounds', y='funding_total_usd', color='status',
                      labels={'funding_rounds': 'Funding Rounds', 'funding_total_usd': 'Total Funding (USD)'},
                      log_y=True, title="Funding Rounds vs Total Funding")
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Market Share by Number of Startups")
    top_markets_share = filtered_df['market'].value_counts().head(5)
    fig7, ax7 = plt.subplots()
    ax7.pie(top_markets_share, labels=top_markets_share.index, autopct='%1.1f%%', startangle=140)
    ax7.set_title("Top 5 Markets by Startup Count")
    st.pyplot(fig7)

    st.subheader("Funding by Funding Type")
    funding_types = ['seed', 'venture', 'round_A', 'round_B', 'round_C', 'round_D']
    existing_types = [col for col in funding_types if col in filtered_df.columns]
    funding_by_type = filtered_df[existing_types].sum()
    fig8, ax8 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=funding_by_type.index, y=funding_by_type.values, ax=ax8)
    ax8.set_title("Total Funding by Type")
    st.pyplot(fig8)

    st.subheader("Markets with Highest Acquisition Rates")
    if 'acquired' in filtered_df['status'].values:
        market_status = filtered_df.groupby(['market', 'status']).size().unstack(fill_value=0)
        market_status['acquired_rate'] = market_status['acquired'] / market_status.sum(axis=1)
        top_acq = market_status['acquired_rate'].sort_values(ascending=False).head(5)
        fig9, ax9 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_acq.values, y=top_acq.index, ax=ax9)
        ax9.set_title('Top Markets by Acquisition Rate')
        st.pyplot(fig9)
    else:
        st.info("No acquisitions in selected filters.")
        
>>>>>>> 8a0c448ba2a2857893ac1dc8c199ac382b562a27
