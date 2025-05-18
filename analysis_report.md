# Startup Investments Analysis Report

## Introduction
This report summarizes the analysis of the Startup Investments dataset, including data cleaning, exploratory data analysis (EDA), and key insights. The findings are presented in an interactive Streamlit dashboard.

## Data Cleaning
- **Non-numeric values**: Converted "-" in `funding_total_usd` to NaN and then to numeric.
- **Missing values**: Filled numerical columns with 0 or median (e.g., `founded_year`) and categorical columns with "Unknown" (e.g., `country_code`).
- **Duplicates**: Removed duplicate rows.
- **Formatting**: Stripped spaces in `market` and converted date columns to datetime.
- **Output**: Saved cleaned data to `cleaned_investments.csv`.

## Exploratory Data Analysis
The EDA focused on identifying trends and patterns in startup funding. The following insights were derived:

1. **Top Markets by Funding**: Biotechnology and Software markets receive the highest funding, indicating investor interest in tech and health.
2. **Funding by Status**: Acquired startups have higher median funding than closed ones, suggesting successful exits attract more capital.
3. **Top Countries**: The USA dominates with the most startups, followed by the UK and China.
4. **Funding Trends**: Funding peaked around 2010-2015, reflecting a tech investment boom.
5. **Funding Rounds**: Startups with more funding rounds tend to raise more total funding.
6. **Market Share**: Software and E-commerce are the most common markets by startup count.
7. **Funding Types**: Venture funding is the largest contributor, followed by round_B and round_C.
8. **Markets with the highest acquisition rates**: Markets like Analytics and Mobile have high acquisition rates, indicating strong exit potential.

## Visualizations
Visualizations for each insight are included in the Streamlit dashboard and saved as PNG files (e.g., `top_markets.png`).

## Streamlit Dashboard
The dashboard allows users to:
- Filter by markets, countries, and status.
- View interactive visualizations for all 8 insights.
- Explore data dynamically through dropdowns and multiselect filters.

## Conclusion
The analysis reveals key trends in startup investments, such as the dominance of tech and biotech, the importance of venture funding, and the high acquisition potential in certain markets. The Streamlit dashboard makes these insights accessible and interactive.

## Recommendations
- Investors should focus on Software and Biotechnology for high funding opportunities.
- Startups in Analytics or Mobile markets may prioritize acquisition strategies.
- Further analysis could explore regional trends or funding success by startup age.