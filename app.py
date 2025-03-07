import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from textblob import TextBlob  # For sentiment analysis

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "0bf7211cc3b9751e106a1d438e8cf9e4"

# Function to fetch macroeconomic data from Alpha Vantage
def fetch_macro_data(function):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": function,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)

    if sentiment_score > 0.1:
        return "Bullish 🟢", sentiment_score
    elif sentiment_score < -0.1:
        return "Bearish 🔴", sentiment_score
    else:
        return "Neutral ⚪", sentiment_score

# Function to determine if FED statement is dovish or hawkish
def analyze_fed_statement(text):
    dovish_keywords = ["accommodative", "stimulus", "easing", "cut rates", "support growth"]
    hawkish_keywords = ["tighten", "inflation", "raise rates", "restrictive", "slow growth"]

    dovish_count = sum(text.lower().count(word) for word in dovish_keywords)
    hawkish_count = sum(text.lower().count(word) for word in hawkish_keywords)

    if dovish_count > hawkish_count:
        return "Dovish 🕊️"
    elif hawkish_count > dovish_count:
        return "Hawkish 🦅"
    else:
        return "Neutral ⚪"

# Streamlit app
st.title("Fundamental Analysis for NQ and ES Markets")

# Sidebar for user input
st.sidebar.header("User Input")
symbol = st.sidebar.selectbox("Select Futures Contract", ["NQ", "ES"])

# Fetch macroeconomic data
st.header("Macroeconomic Data Analysis")
st.write("This section analyzes the latest US macroeconomic data and its impact on the market.")

# Fetch GDP data
gdp_data = fetch_macro_data("REAL_GDP")
if "data" in gdp_data:
    gdp_df = pd.DataFrame(gdp_data["data"])
    gdp_df["value"] = pd.to_numeric(gdp_df["value"])
    st.subheader("GDP Growth")
    st.write(gdp_df)
    latest_gdp = gdp_df["value"].iloc[0]
    st.write(f"**Latest GDP Growth**: {latest_gdp:.2f}%")
else:
    st.write("No GDP data found.")

# Fetch CPI data
cpi_data = fetch_macro_data("CPI")
if "data" in cpi_data:
    cpi_df = pd.DataFrame(cpi_data["data"])
    cpi_df["value"] = pd.to_numeric(cpi_df["value"])
    st.subheader("Consumer Price Index (CPI)")
    st.write(cpi_df)
    latest_cpi = cpi_df["value"].iloc[0]
    st.write(f"**Latest CPI**: {latest_cpi:.2f}%")
else:
    st.write("No CPI data found.")

# Fetch unemployment data
unemployment_data = fetch_macro_data("UNEMPLOYMENT")
if "data" in unemployment_data:
    unemployment_df = pd.DataFrame(unemployment_data["data"])
    unemployment_df["value"] = pd.to_numeric(unemployment_df["value"])
    st.subheader("Unemployment Rate")
    st.write(unemployment_df)
    latest_unemployment = unemployment_df["value"].iloc[0]
    st.write(f"**Latest Unemployment Rate**: {latest_unemployment:.2f}%")
else:
    st.write("No unemployment data found.")

# Fetch interest rate data
interest_rate_data = fetch_macro_data("FEDERAL_FUNDS_RATE")
if "data" in interest_rate_data:
    interest_rate_df = pd.DataFrame(interest_rate_data["data"])
    interest_rate_df["value"] = pd.to_numeric(interest_rate_df["value"])
    st.subheader("Federal Funds Rate")
    st.write(interest_rate_df)
    latest_interest_rate = interest_rate_df["value"].iloc[0]
    st.write(f"**Latest Federal Funds Rate**: {latest_interest_rate:.2f}%")
else:
    st.write("No interest rate data found.")

# Fundamental analysis based on circular flow of income
st.header("Fundamental Analysis Based on Circular Flow of Income")
st.write("""
The circular flow of income includes:
- **Households**: Provide labor and consume goods/services.
- **Businesses**: Produce goods/services and pay wages.
- **Government**: Collects taxes and spends on public goods.
- **Foreign Sector**: Exports and imports goods/services.
""")

# Analyze the impact of macroeconomic data
st.subheader("Impact of Macroeconomic Data")
if "latest_gdp" in locals() and "latest_cpi" in locals() and "latest_unemployment" in locals() and "latest_interest_rate" in locals():
    st.write(f"""
    - **GDP Growth**: {latest_gdp:.2f}%  
      A positive GDP growth indicates a strong economy, which is **bullish** for equity markets.
    - **CPI**: {latest_cpi:.2f}%  
      High CPI (inflation) can be **bearish**, as it may lead to higher interest rates and reduced consumer spending.
    - **Unemployment Rate**: {latest_unemployment:.2f}%  
      Low unemployment is **bullish**, as it indicates a strong labor market and consumer spending.
    - **Federal Funds Rate**: {latest_interest_rate:.2f}%  
      Low interest rates are **bullish**, as they encourage borrowing and investment.
    """)
else:
    st.write("Unable to analyze macroeconomic data due to missing values.")

# Manual input for FED statements
st.header("FED Statement Analysis")
st.write("Paste the latest two FED statements below to analyze their tone (hawkish/dovish).")

# Input for two FED statements
statement1 = st.text_area("Paste the first FED statement here:")
statement2 = st.text_area("Paste the second FED statement here:")

# Analyze the statements
if statement1 and statement2:
    st.subheader("Analysis of FED Statements")

    # Analyze the first statement
    st.write("**First Statement Analysis**")
    tone1 = analyze_fed_statement(statement1)
    st.write(f"**Tone**: {tone1}")
    st.write("---")

    # Analyze the second statement
    st.write("**Second Statement Analysis**")
    tone2 = analyze_fed_statement(statement2)
    st.write(f"**Tone**: {tone2}")
    st.write("---")

    # Compare the two statements
    st.subheader("Comparison of FED Statements")
    comparison_data = {
        "Statement": ["Statement 1", "Statement 2"],
        "Tone": [tone1, tone2],
    }
    df_comparison = pd.DataFrame(comparison_data)
    st.write(df_comparison)
else:
    st.write("Please paste two FED statements to analyze.")

# Final market sentiment analysis
st.header("Final Market Sentiment Analysis")
if "latest_gdp" in locals() and "latest_cpi" in locals() and "latest_unemployment" in locals() and "latest_interest_rate" in locals():
    # Calculate overall sentiment
    bullish_count = 0
    bearish_count = 0

    if latest_gdp > 0:
        bullish_count += 1
    else:
        bearish_count += 1

    if latest_cpi < 2:  # Low inflation is bullish
        bullish_count += 1
    else:
        bearish_count += 1

    if latest_unemployment < 5:  # Low unemployment is bullish
        bullish_count += 1
    else:
        bearish_count += 1

    if latest_interest_rate < 2:  # Low interest rates are bullish
        bullish_count += 1
    else:
        bearish_count += 1

    # Include FED statement tone in sentiment analysis
    if statement1 and statement2:
        if "Dovish" in tone1:
            bullish_count += 1
        elif "Hawkish" in tone1:
            bearish_count += 1

        if "Dovish" in tone2:
            bullish_count += 1
        elif "Hawkish" in tone2:
            bearish_count += 1

    # Determine overall sentiment
    if bullish_count > bearish_count:
        st.success("**Overall Market Sentiment**: Bullish 🟢")
    elif bearish_count > bullish_count:
        st.error("**Overall Market Sentiment**: Bearish 🔴")
    else:
        st.warning("**Overall Market Sentiment**: Neutral ⚪")
else:
    st.write("Unable to determine market sentiment due to missing data.")