import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title
st.title("Startup Investments Dashboard")

# Load data
df = pd.read_csv('cleaned_investments.csv')
df['first_funding_year'] = pd.to_datetime(df['first_funding_at'], errors='coerce').dt.year
df['time_to_funding'] = (pd.to_datetime(df['first_funding_at'], errors='coerce') - pd.to_datetime(df['founded_at'], errors='coerce')).dt.days

# Sidebar filters
st.sidebar.header("Filters")
markets = st.sidebar.multiselect("Select Markets", options=df['market'].unique(), default=df['market'].unique()[:5])
countries = st.sidebar.multiselect("Select Countries", options=df['country_code'].unique(), default=['USA', 'CHN', 'GBR'])
status = st.sidebar.multiselect("Select Status", options=df['status'].unique(), default=df['status'].unique())
funding_min, funding_max = st.sidebar.slider("Funding Range (USD)", 0, int(df['funding_total_usd'].max()), (0, 1000000000))

# Filter data
filtered_df = df[
    (df['market'].isin(markets)) &
    (df['country_code'].isin(countries)) &
    (df['status'].isin(status)) &
    (df['funding_total_usd'].between(funding_min, funding_max))
]

# Insight 1: Total funding
st.header("Insight 1: Total Funding")
total_funding = filtered_df['funding_total_usd'].sum()
st.metric("Total Funding (USD)", f"${total_funding:,.2f}")

# Insight 2: Top markets
st.header("Insight 2: Top Markets by Funding")
market_funding = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
fig1 = px.bar(x=market_funding.values, y=market_funding.index, title="Top 10 Markets by Funding")
st.plotly_chart(fig1)

# Insight 3: Country distribution
st.header("Insight 3: Startups by Country")
country_count = filtered_df['country_code'].value_counts().head(10)
fig2 = px.bar(x=country_count.index, y=country_count.values, title="Top 10 Countries by Startup Count")
st.plotly_chart(fig2)

# Insight 4: Status distribution
st.header("Insight 4: Startup Status")
status_counts = filtered_df['status'].value_counts()
fig3 = px.pie(values=status_counts.values, names=status_counts.index, title="Startup Status Distribution")
st.plotly_chart(fig3)

# Insight 5: Top startups
st.header("Insight 5: Top Funded Startups")
top_funded = filtered_df[['name', 'funding_total_usd', 'market']].sort_values('funding_total_usd', ascending=False).head(5)
st.dataframe(top_funded)

# Insight 6: Funding types
st.header("Insight 6: Funding Types")
funding_types = filtered_df[['seed', 'venture', 'angel', 'private_equity', 'debt_financing']].sum()
fig4 = px.bar(x=funding_types.index, y=funding_types.values, title="Funding by Type")
st.plotly_chart(fig4)

# Insight 7: Funding rounds
st.header("Insight 7: Funding Rounds Distribution")
fig5 = px.histogram(filtered_df, x='funding_rounds', title="Distribution of Funding Rounds")
st.plotly_chart(fig5)

# Insight 8: Average funding by market
st.header("Insight 8: Average Funding by Market")
avg_market_funding = filtered_df.groupby('market')['funding_total_usd'].mean().sort_values(ascending=False).head(10)
fig6 = px.bar(x=avg_market_funding.values, y=avg_market_funding.index, title="Top 10 Markets by Average Funding")
st.plotly_chart(fig6)

# Insight 9: Funding trend
st.header("Insight 9: Funding Trend by Year")
yearly_funding = filtered_df.groupby('first_funding_year')['funding_total_usd'].sum()
fig7 = px.line(x=yearly_funding.index, y=yearly_funding.values, title="Funding Trend Over Time")
st.plotly_chart(fig7)

# Insight 10: Time to funding
st.header("Insight 10: Time to First Funding")
fig8 = px.histogram(filtered_df, x='time_to_funding', title="Time to First Funding (Days)")
st.plotly_chart(fig8)