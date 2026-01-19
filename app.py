"""
VNINDEX Random Ticker Selector
A Streamlit app optimized for 20:9 screen aspect ratio
"""

import streamlit as st
import random
from tradingview_screener import Query, col

# Page configuration - optimized for 20:9 aspect ratio
st.set_page_config(
    page_title="VNINDEX Random Picker",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for 20:9 optimization and premium aesthetics
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --dark-bg: #0f0f23;
        --card-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container optimization for 20:9 */
    .main .block-container {
        max-width: 100%;
        padding: 1rem 3rem;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Ticker display card */
    .ticker-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .ticker-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 16px 48px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .ticker-symbol {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }
    
    .company-name {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    
    .sector-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* TradingView link button */
    .tv-link {
        display: inline-block;
        padding: 1rem 3rem;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        text-decoration: none;
        box-shadow: 0 4px 20px rgba(56, 239, 125, 0.3);
        transition: all 0.3s ease;
    }
    
    .tv-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(56, 239, 125, 0.4);
        color: white;
    }
    
    /* Stats bar */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Horizontal layout optimization */
    .horizontal-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        padding: 1rem 0;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_vnindex_stocks():
    """Retrieve all VNINDEX (HOSE) stocks using tradingview-screener"""
    try:
        query = (Query()
                 .set_markets('vietnam')
                 .select('name', 'close', 'volume', 'market_cap_basic', 'price_earnings_ttm', 'sector')
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


def main():
    # Title section
    st.markdown('<h1 class="main-title">🎲 VNINDEX Random Picker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your next investment opportunity</p>', unsafe_allow_html=True)
    
    # Load stock data
    with st.spinner("Loading VNINDEX stocks..."):
        df = get_vnindex_stocks()
    
    if df is None or df.empty:
        st.error("Could not load stock data. Please try again later.")
        return
    
    # Initialize session state for selected ticker
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = None
        st.session_state.selected_data = None
    
    # Create horizontal layout for 20:9 optimization
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Random pick button
        if st.button("🎲 Pick Random Ticker", use_container_width=True):
            random_idx = random.randint(0, len(df) - 1)
            st.session_state.selected_ticker = df.iloc[random_idx]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display selected ticker
        if st.session_state.selected_ticker is not None:
            ticker_data = st.session_state.selected_ticker
            
            # Extract ticker symbol (remove "HOSE:" prefix)
            full_ticker = ticker_data['ticker']
            ticker_symbol = full_ticker.split(':')[1] if ':' in full_ticker else full_ticker
            
            # Build TradingView URL
            tv_url = f"https://www.tradingview.com/symbols/{full_ticker.replace(':', '-')}/?timeframe=6M"
            
            # Ticker card HTML
            sector = ticker_data.get('sector', 'N/A') if ticker_data.get('sector') else 'N/A'
            name = ticker_data.get('name', ticker_symbol)
            
            ticker_html = f"""
            <div class="ticker-card">
                <div class="ticker-symbol">{ticker_symbol}</div>
                <div class="company-name">{name}</div>
                <div class="sector-badge">{sector}</div>
                <br><br>
                <a href="{tv_url}" target="_blank" class="tv-link">
                    📈 View on TradingView
                </a>
                <div class="stats-container">
                    <div class="stat-item">
                        <div class="stat-value">{format_number(ticker_data.get('close', 0)):}</div>
                        <div class="stat-label">Price (VND)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{format_number(ticker_data.get('volume', 0))}</div>
                        <div class="stat-label">Volume</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{format_number(ticker_data.get('market_cap_basic', 0))}</div>
                        <div class="stat-label">Market Cap</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{ticker_data.get('price_earnings_ttm', 0):.1f}x</div>
                        <div class="stat-label">P/E Ratio</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(ticker_html, unsafe_allow_html=True)
        else:
            # Empty state
            st.markdown("""
            <div class="ticker-card">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
                <div class="company-name">Click the button above to pick a random stock</div>
                <div style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">
                    From {count} stocks on VNINDEX
                </div>
            </div>
            """.format(count=len(df)), unsafe_allow_html=True)
    
    # Footer with stock count
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align: center; color: rgba(255,255,255,0.4); font-size: 0.85rem;">'
        f'📊 Total stocks available: {len(df)} | Data refreshes every 5 minutes</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
