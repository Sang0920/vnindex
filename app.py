"""
VNINDEX Random Ticker Selector
A Streamlit app optimized for 20:9 screen aspect ratio
With advanced quantitative scoring and animations
"""

import streamlit as st
import random
import time
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
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        min-width: 80px;
    }
    
    .stat-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-value.positive {
        color: #38ef7d;
    }
    
    .stat-value.negative {
        color: #f5576c;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Performance section */
    .perf-section {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .perf-title {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 1rem;
        font-weight: 500;
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
    
    /* Slot machine animation */
    @keyframes slotSpin {
        0% { transform: translateY(0); }
        25% { transform: translateY(-100%); }
        50% { transform: translateY(-200%); }
        75% { transform: translateY(-100%); }
        100% { transform: translateY(0); }
    }
    
    .slot-machine {
        animation: slotSpin 0.5s ease-in-out;
    }
    
    /* Confetti animation */
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        top: 0;
        animation: confetti-fall 3s ease-out forwards;
        z-index: 1000;
    }
    
    /* Score gauge */
    .score-gauge {
        width: 100%;
        height: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .score-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 1s ease-out;
    }
    
    /* 52-week position bar */
    .position-bar {
        width: 100%;
        height: 12px;
        background: linear-gradient(90deg, #f5576c 0%, #ffd700 50%, #38ef7d 100%);
        border-radius: 6px;
        position: relative;
        margin: 1rem 0;
    }
    
    .position-marker {
        position: absolute;
        top: -4px;
        width: 20px;
        height: 20px;
        background: white;
        border-radius: 50%;
        transform: translateX(-50%);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Score card */
    .score-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .score-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_vnindex_stocks():
    """Retrieve all VNINDEX (HOSE) stocks using tradingview-screener"""
    try:
        query = (Query()
                 .set_markets('vietnam')
                 .select(
                     'name', 'close', 'volume', 'market_cap_basic', 'price_earnings_ttm', 'sector',
                     # Performance metrics
                     'change',           # Daily change %
                     'Perf.W',           # Weekly performance
                     'Perf.1M',          # 1-month performance
                     'Perf.3M',          # 3-month performance  
                     'Perf.6M',          # 6-month performance
                     'Perf.Y',           # 1-year performance
                     'Perf.YTD',         # Year-to-date performance
                     # Additional metrics
                     'dividend_yield_recent',  # Dividend yield
                     'earnings_per_share_basic_ttm',  # EPS
                     'price_52_week_high',  # 52-week high
                     'price_52_week_low',   # 52-week low
                     'beta_1_year',         # Beta
                     'average_volume_10d_calc',  # 10-day avg volume
                 )
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


def calculate_momentum_score(ticker_data):
    """
    Calculate momentum score based on weighted performance metrics.
    Weights: 6M = 40%, 3M = 25%, 1M = 20%, 1W = 15%
    Returns score from 0-100
    """
    weights = {
        'Perf.6M': 0.40,
        'Perf.3M': 0.25,
        'Perf.1M': 0.20,
        'Perf.W': 0.15,
    }
    
    weighted_sum = 0
    total_weight = 0
    
    for key, weight in weights.items():
        val = safe_get(ticker_data, key)
        if val is not None and val == val:  # Not NaN
            # Normalize: +50% = 100 score, -50% = 0 score
            normalized = max(0, min(100, (val + 50) * 1))
            weighted_sum += normalized * weight
            total_weight += weight
    
    if total_weight > 0:
        return weighted_sum / total_weight
    return 50  # Neutral


def calculate_value_score(ticker_data):
    """
    Calculate value score based on P/E ratio and dividend yield.
    Lower P/E and higher yield = higher score
    Returns score from 0-100
    """
    pe = safe_get(ticker_data, 'price_earnings_ttm')
    div_yield = safe_get(ticker_data, 'dividend_yield_recent')
    
    # P/E score: Lower is better (P/E of 5 = 100, P/E of 50 = 0)
    pe_score = 0
    if pe and pe > 0:
        pe_score = max(0, min(100, (50 - pe) * 2.22))
    
    # Dividend yield score: Higher is better (10% = 100, 0% = 0)
    div_score = 0
    if div_yield and div_yield > 0:
        div_score = min(100, div_yield * 10)
    
    # Weighted: 70% P/E, 30% dividend
    return pe_score * 0.7 + div_score * 0.3


def calculate_composite_score(ticker_data):
    """
    Calculate composite investment score.
    60% momentum + 40% value
    Returns score from 0-100
    """
    momentum = calculate_momentum_score(ticker_data)
    value = calculate_value_score(ticker_data)
    return momentum * 0.6 + value * 0.4


def calculate_52week_position(ticker_data):
    """
    Calculate where current price sits in the 52-week range.
    Returns percentage (0 = at low, 100 = at high)
    """
    high = safe_get(ticker_data, 'price_52_week_high')
    low = safe_get(ticker_data, 'price_52_week_low')
    current = safe_get(ticker_data, 'close')
    
    if high and low and current and high > low:
        position = (current - low) / (high - low) * 100
        return max(0, min(100, position))
    return 50  # Default to middle


def generate_confetti_html():
    """Generate confetti animation HTML for celebration effect"""
    colors = ['#667eea', '#764ba2', '#38ef7d', '#f093fb', '#ffd700', '#ff6b6b']
    confetti_pieces = []
    
    for i in range(30):
        color = random.choice(colors)
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        size = random.randint(8, 15)
        confetti_pieces.append(
            f'<div class="confetti" style="left: {left}%; background: {color}; '
            f'animation-delay: {delay}s; width: {size}px; height: {size}px; '
            f'border-radius: {random.choice(["50%", "0%"])}"></div>'
        )
    
    return ''.join(confetti_pieces)


def get_score_color(score):
    """Get color based on score (0-100)"""
    if score >= 70:
        return "#38ef7d"  # Green
    elif score >= 50:
        return "#ffd700"  # Gold
    elif score >= 30:
        return "#f093fb"  # Pink
    else:
        return "#f5576c"  # Red


def format_percent(num):
    """Format percentage with + sign for positive values and color class"""
    if num is None or num != num:  # Check for None or NaN
        return "N/A", ""
    sign = "+" if num >= 0 else ""
    color_class = "positive" if num >= 0 else "negative"
    return f"{sign}{num:.2f}%", color_class


def safe_get(data, key, default=0):
    """Safely get a value from series, handling NaN"""
    val = data.get(key, default)
    if val is None or (isinstance(val, float) and val != val):
        return default
    return val


def main():
    # Title section
    st.markdown('<h1 class="main-title">🎲 VNINDEX Random Picker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your next investment opportunity with AI-powered scoring</p>', unsafe_allow_html=True)
    
    # Load stock data
    with st.spinner("Loading VNINDEX stocks..."):
        df = get_vnindex_stocks()
    
    if df is None or df.empty:
        st.error("Could not load stock data. Please try again later.")
        return
    
    # Sidebar for smart filtering
    with st.sidebar:
        st.markdown("## 🎯 Smart Filters")
        
        # Sector filter
        sectors = ['All Sectors'] + sorted(df['sector'].dropna().unique().tolist())
        selected_sector = st.selectbox("📁 Sector", sectors)
        
        # Market cap filter
        st.markdown("💰 Market Cap Range")
        min_cap, max_cap = st.slider(
            "Market Cap (Trillion VND)",
            min_value=0.0,
            max_value=500.0,
            value=(0.0, 500.0),
            step=10.0
        )
        
        # Hot stocks filter
        hot_stocks_only = st.checkbox("🔥 Hot Stocks Only (Positive 6M)", value=False)
        
        # Lucky pick mode
        lucky_mode = st.checkbox("🍀 Lucky Mode (Favor High Momentum)", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 Dataset Info")
        st.markdown(f"**Total Stocks:** {len(df)}")
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_sector != 'All Sectors':
        filtered_df = filtered_df[filtered_df['sector'] == selected_sector]
    
    # Market cap filter (convert to trillion VND)
    if 'market_cap_basic' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['market_cap_basic'].fillna(0) >= min_cap * 1e12) &
            (filtered_df['market_cap_basic'].fillna(0) <= max_cap * 1e12)
        ]
    
    if hot_stocks_only and 'Perf.6M' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Perf.6M'].fillna(0) > 0]
    
    # Update sidebar with filtered count
    with st.sidebar:
        st.markdown(f"**Filtered Stocks:** {len(filtered_df)}")
    
    # Initialize session state for selected ticker and animation
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = None
    if 'show_confetti' not in st.session_state:
        st.session_state.show_confetti = False
    if 'animation_key' not in st.session_state:
        st.session_state.animation_key = 0
    
    # Create horizontal layout for 20:9 optimization
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Random pick button
        if st.button("🎲 Pick Random Ticker", use_container_width=True):
            if len(filtered_df) > 0:
                if lucky_mode and 'Perf.6M' in filtered_df.columns:
                    # Weighted random selection favoring high momentum
                    momentum_scores = filtered_df['Perf.6M'].fillna(0) + 100  # Shift to positive
                    momentum_scores = momentum_scores.clip(lower=1)  # Ensure positive weights
                    weights = momentum_scores / momentum_scores.sum()
                    random_idx = filtered_df.sample(1, weights=weights).index[0]
                    st.session_state.selected_ticker = filtered_df.loc[random_idx]
                else:
                    random_idx = random.randint(0, len(filtered_df) - 1)
                    st.session_state.selected_ticker = filtered_df.iloc[random_idx]
                
                # Check for confetti
                perf_6m = safe_get(st.session_state.selected_ticker, 'Perf.6M')
                st.session_state.show_confetti = perf_6m > 0 if perf_6m else False
                st.session_state.animation_key += 1
            else:
                st.warning("No stocks match your filters. Try adjusting the criteria.")
        
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
            
            # Format performance metrics
            change_val, change_class = format_percent(safe_get(ticker_data, 'change'))
            perf_w_val, perf_w_class = format_percent(safe_get(ticker_data, 'Perf.W'))
            perf_1m_val, perf_1m_class = format_percent(safe_get(ticker_data, 'Perf.1M'))
            perf_3m_val, perf_3m_class = format_percent(safe_get(ticker_data, 'Perf.3M'))
            perf_6m_val, perf_6m_class = format_percent(safe_get(ticker_data, 'Perf.6M'))
            perf_y_val, perf_y_class = format_percent(safe_get(ticker_data, 'Perf.Y'))
            perf_ytd_val, perf_ytd_class = format_percent(safe_get(ticker_data, 'Perf.YTD'))
            
            # Format other metrics
            pe_ratio = safe_get(ticker_data, 'price_earnings_ttm')
            pe_display = f"{pe_ratio:.1f}x" if pe_ratio else "N/A"
            
            div_yield = safe_get(ticker_data, 'dividend_yield_recent')
            div_display = f"{div_yield:.2f}%" if div_yield else "N/A"
            
            eps = safe_get(ticker_data, 'earnings_per_share_basic_ttm')
            eps_display = format_number(eps) if eps else "N/A"
            
            high_52w = safe_get(ticker_data, 'price_52_week_high')
            low_52w = safe_get(ticker_data, 'price_52_week_low')
            
            beta = safe_get(ticker_data, 'beta_1_year')
            beta_display = f"{beta:.2f}" if beta else "N/A"
            
            # Header card with ticker info and link
            header_html = f"""
            <div class="ticker-card">
                <div class="ticker-symbol">{ticker_symbol}</div>
                <div class="company-name">{name}</div>
                <div class="sector-badge">{sector}</div>
                <br><br>
                <a href="{tv_url}" target="_blank" class="tv-link">
                    📈 View on TradingView
                </a>
            </div>
            """
            st.markdown(header_html, unsafe_allow_html=True)
            
            # Performance metrics using Streamlit columns
            st.markdown('<p style="color: rgba(255,255,255,0.6); text-align: center; margin-top: 1.5rem; font-weight: 500;">📊 Performance</p>', unsafe_allow_html=True)
            perf_cols = st.columns(7)
            
            perf_data = [
                ("Today", change_val, change_class),
                ("1 Week", perf_w_val, perf_w_class),
                ("1 Month", perf_1m_val, perf_1m_class),
                ("3 Months", perf_3m_val, perf_3m_class),
                ("6 Months", perf_6m_val, perf_6m_class),
                ("1 Year", perf_y_val, perf_y_class),
                ("YTD", perf_ytd_val, perf_ytd_class),
            ]
            
            for i, (label, value, color_class) in enumerate(perf_data):
                with perf_cols[i]:
                    color = "#38ef7d" if color_class == "positive" else "#f5576c" if color_class == "negative" else "#667eea"
                    # Highlight 6 Months (index 4) with special styling
                    if i == 4:  # 6 Months
                        st.markdown(f'''
                        <div style="text-align: center; padding: 0.8rem 0.5rem; background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%); border: 2px solid {color}; border-radius: 12px; box-shadow: 0 0 15px {color}40;">
                            <span style="color: {color}; font-size: 1.6rem; font-weight: 800;">{value}</span><br>
                            <span style="color: rgba(255,255,255,0.8); font-size: 0.8rem; text-transform: uppercase; font-weight: 600;">⭐ {label}</span>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="text-align: center;"><span style="color: {color}; font-size: 1.2rem; font-weight: 700;">{value}</span><br><span style="color: rgba(255,255,255,0.5); font-size: 0.7rem; text-transform: uppercase;">{label}</span></div>', unsafe_allow_html=True)
            
            # Key metrics
            st.markdown('<p style="color: rgba(255,255,255,0.6); text-align: center; margin-top: 1.5rem; font-weight: 500;">📈 Key Metrics</p>', unsafe_allow_html=True)
            metric_cols = st.columns(7)
            
            metrics_data = [
                ("Price (VND)", format_number(safe_get(ticker_data, 'close'))),
                ("Volume", format_number(safe_get(ticker_data, 'volume'))),
                ("Market Cap", format_number(safe_get(ticker_data, 'market_cap_basic'))),
                ("P/E Ratio", pe_display),
                ("EPS (TTM)", eps_display),
                ("Div Yield", div_display),
                ("Beta", beta_display),
            ]
            
            for i, (label, value) in enumerate(metrics_data):
                with metric_cols[i]:
                    st.markdown(f'<div style="text-align: center;"><span style="color: #667eea; font-size: 1.2rem; font-weight: 700;">{value}</span><br><span style="color: rgba(255,255,255,0.5); font-size: 0.7rem; text-transform: uppercase;">{label}</span></div>', unsafe_allow_html=True)
            
            # 52-Week Range
            st.markdown('<p style="color: rgba(255,255,255,0.6); text-align: center; margin-top: 1.5rem; font-weight: 500;">📉 52-Week Range</p>', unsafe_allow_html=True)
            range_cols = st.columns([1, 1, 1, 1, 1])
            
            with range_cols[1]:
                st.markdown(f'<div style="text-align: center;"><span style="color: #f5576c; font-size: 1.2rem; font-weight: 700;">{format_number(low_52w)}</span><br><span style="color: rgba(255,255,255,0.5); font-size: 0.7rem; text-transform: uppercase;">52W Low</span></div>', unsafe_allow_html=True)
            with range_cols[2]:
                st.markdown(f'<div style="text-align: center;"><span style="color: #667eea; font-size: 1.2rem; font-weight: 700;">{format_number(safe_get(ticker_data, "close"))}</span><br><span style="color: rgba(255,255,255,0.5); font-size: 0.7rem; text-transform: uppercase;">Current</span></div>', unsafe_allow_html=True)
            with range_cols[3]:
                st.markdown(f'<div style="text-align: center;"><span style="color: #38ef7d; font-size: 1.2rem; font-weight: 700;">{format_number(high_52w)}</span><br><span style="color: rgba(255,255,255,0.5); font-size: 0.7rem; text-transform: uppercase;">52W High</span></div>', unsafe_allow_html=True)
            
            # 52-Week Position Bar
            position = calculate_52week_position(ticker_data)
            st.markdown(f'''
            <div style="margin: 1.5rem 0;">
                <p style="color: rgba(255,255,255,0.6); text-align: center; font-weight: 500; margin-bottom: 0.5rem;">📍 52-Week Position: {position:.1f}%</p>
                <div class="position-bar">
                    <div class="position-marker" style="left: {position}%;"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # AI Scores Section
            st.markdown('<p style="color: rgba(255,255,255,0.6); text-align: center; margin-top: 1.5rem; font-weight: 500;">🤖 AI Investment Scores</p>', unsafe_allow_html=True)
            
            # Calculate scores
            momentum_score = calculate_momentum_score(ticker_data)
            value_score = calculate_value_score(ticker_data)
            composite_score = calculate_composite_score(ticker_data)
            
            score_cols = st.columns(3)
            
            with score_cols[0]:
                color = get_score_color(momentum_score)
                st.markdown(f'''
                <div class="score-card">
                    <div class="score-value" style="background: linear-gradient(135deg, {color} 0%, {color}aa 100%); -webkit-background-clip: text;">{momentum_score:.0f}</div>
                    <div class="score-label">Momentum Score</div>
                    <div class="score-gauge">
                        <div class="score-fill" style="width: {momentum_score}%; background: {color};"></div>
                    </div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; margin-top: 0.5rem;">6M=40% | 3M=25% | 1M=20% | 1W=15%</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with score_cols[1]:
                color = get_score_color(value_score)
                st.markdown(f'''
                <div class="score-card">
                    <div class="score-value" style="background: linear-gradient(135deg, {color} 0%, {color}aa 100%); -webkit-background-clip: text;">{value_score:.0f}</div>
                    <div class="score-label">Value Score</div>
                    <div class="score-gauge">
                        <div class="score-fill" style="width: {value_score}%; background: {color};"></div>
                    </div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; margin-top: 0.5rem;">P/E=70% | Dividend=30%</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with score_cols[2]:
                color = get_score_color(composite_score)
                st.markdown(f'''
                <div class="score-card">
                    <div class="score-value" style="background: linear-gradient(135deg, {color} 0%, {color}aa 100%); -webkit-background-clip: text;">{composite_score:.0f}</div>
                    <div class="score-label">⭐ Investment Score</div>
                    <div class="score-gauge">
                        <div class="score-fill" style="width: {composite_score}%; background: {color};"></div>
                    </div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; margin-top: 0.5rem;">Momentum=60% | Value=40%</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Confetti for positive 6M performance
            if st.session_state.show_confetti:
                st.markdown(generate_confetti_html(), unsafe_allow_html=True)

        else:
            # Empty state
            st.markdown(f"""
            <div class="ticker-card">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
                <div class="company-name">Click the button above to pick a random stock</div>
                <div style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">
                    From {len(filtered_df)} filtered stocks ({len(df)} total on VNINDEX)
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer with stock count
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="text-align: center; color: rgba(255,255,255,0.4); font-size: 0.85rem;">'
        f'📊 Showing {len(filtered_df)} of {len(df)} stocks | 🤖 AI Scoring Enabled | Data refreshes every 5 minutes</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
