"""
VNINDEX Random Stock Picker
Simple random stock selector for HOSE exchange
"""

import streamlit as st
import random
from tradingview_screener import Query, col

# Page configuration
st.set_page_config(
    page_title="VNINDEX Random Picker",
    page_icon="🎲",
    layout="centered"
)

# Custom CSS - minimal styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .ticker-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .ticker-symbol {
        font-size: 3.5rem;
        font-weight: bold;
        color: #38ef7d;
        margin: 1rem 0;
    }
    
    .company-name {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0.5rem;
    }
    
    .sector-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        font-size: 0.9rem;
        color: #667eea;
        margin: 1rem 0;
    }
    
    .metrics-row {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        flex: 1;
        min-width: 120px;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        margin-top: 0.3rem;
    }
    
    .tv-button {
        display: inline-block;
        padding: 0.8rem 2rem;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        margin-top: 1.5rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: opacity 0.3s ease;
    }
    
    .tv-button:hover {
        opacity: 0.9;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
    }
    
    .stButton > button:hover {
        opacity: 0.9;
    }
    
    .footer-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_vnindex_stocks():
    """Retrieve all VNINDEX (HOSE) stocks"""
    try:
        query = (Query()
                 .set_markets('vietnam')
                 .select('name', 'close', 'volume', 'market_cap_basic', 'sector')
                 .where(col('exchange') == 'HOSE')
                 .limit(9999)
                 .get_scanner_data())
        
        count, df = query
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


def format_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num is None or num != num:  # Check for None or NaN
        return "N/A"
    if num >= 1e12:
        return f"{num/1e12:.1f}T"
    elif num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return f"{num:.0f}"


def safe_get(data, key, default=0):
    """Safely get a value from series, handling NaN"""
    val = data.get(key, default)
    if val is None or (isinstance(val, float) and val != val):
        return default
    return val


def main():
    # Title
    st.markdown('<h1 class="main-title">🎲 VNINDEX Random Picker</h1>', unsafe_allow_html=True)
    
    # Load stock data
    with st.spinner("Loading HOSE stocks..."):
        df = get_vnindex_stocks()
    
    if df is None or df.empty:
        st.error("Could not load stock data. Please try again later.")
        return
    
    # Initialize session state
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = None
    
    # Pick button
    if st.button("🎲 Pick a Random Stock"):
        random_idx = random.randint(0, len(df) - 1)
        st.session_state.selected_ticker = df.iloc[random_idx]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display selected ticker
    if st.session_state.selected_ticker is not None:
        ticker_data = st.session_state.selected_ticker
        
        # Get ticker symbol from name or index
        # TradingView returns data without explicit ticker field, so we use the symbol identifier
        ticker_symbol = ticker_data.get('symbol', '').split(':')[-1] or ticker_data.get('name', 'UNKNOWN')
        
        # Build TradingView URL
        tv_url = f"https://www.tradingview.com/symbols/HOSE-{ticker_symbol}/?timeframe=6M"
        
        # Get data
        name = ticker_data.get('name', ticker_symbol)
        sector = ticker_data.get('sector', 'N/A')
        price = safe_get(ticker_data, 'close')
        volume = safe_get(ticker_data, 'volume')
        market_cap = safe_get(ticker_data, 'market_cap_basic')
        
        # Ticker card header
        st.markdown(f"""
        <div class="ticker-card">
            <div class="ticker-symbol">{ticker_symbol}</div>
            <div class="company-name">{name}</div>
            <div class="sector-badge">{sector}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics using Streamlit columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Price (VND)", format_number(price))
        
        with col2:
            st.metric("Volume", format_number(volume))
        
        with col3:
            st.metric("Market Cap", format_number(market_cap))
        
        # TradingView button
        st.markdown(f'<div style="text-align: center; margin-top: 2rem;"><a href="{tv_url}" target="_blank" class="tv-button">📈 View on TradingView</a></div>', unsafe_allow_html=True)
    else:
        # Empty state
        st.markdown(f"""
        <div class="ticker-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <div class="company-name">Click the button above to pick a random stock!</div>
            <div style="color: rgba(255, 255, 255, 0.5); font-size: 0.95rem; margin-top: 1rem;">
                Selecting from {len(df)} stocks on HOSE
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(
        f'<div class="footer-text">📊 Showing stocks from HOSE ({len(df)} total) | Data refreshes every 5 minutes</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
