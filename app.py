import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. SETUP ---
st.set_page_config(page_title="GASPAY", layout="wide", page_icon="⛽")

# --- 2. MOBILE-OPTIMIZED STYLING (CSS) ---
st.markdown("""
<style>
    /* FORCE PURE WHITE BACKGROUND */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    [data-testid="stHeader"] {
        background-color: #FFFFFF;
    }
    
    /* UNIVERSAL TEXT COLOR FORCE (BLACK) */
    h1, h2, h3, h4, h5, p, div, label, span, li {
        color: #000000 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* --- DESKTOP STYLES (DEFAULT) --- */
    .header-bar {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%);
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    .header-text {
        color: white !important;
        font-size: 50px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .header-sub {
        color: #F0F2F6 !important;
        font-size: 18px !important;
        font-weight: 400 !important;
        margin-top: 5px;
    }

    /* --- MOBILE OVERRIDES (Aggressive Fixes) --- */
    @media (max-width: 900px) {
        .header-bar {
            padding: 20px 10px !important;
        }
        .header-text {
            font-size: 28px !important;
        }
        .header-sub {
            font-size: 14px !important;
        }
        
        /* Fix the Button Squish on Mobile */
        div.stButton > button {
            padding: 12px 10px !important;
            font-size: 14px !important;
        }
        
        /* Force Metric Values to be smaller on phone so they don't cut off */
        div[data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
    }

    /* METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: #F8F9FE !important;
        border: 2px solid #E3E8F0;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        /* Ensure text doesn't cut off */
        overflow-wrap: break-word;
        white-space: normal; 
    }
    label[data-testid="stMetricLabel"] {
        color: #4169E1 !important;
        font-weight: 800 !important;
        font-size: 13px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #000000 !important;
        font-size: 28px !important; /* Default Desktop Size */
        font-weight: 800 !important;
    }

    /* INPUT FIELD & BUTTON */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 3px solid #4169E1;
        border-radius: 10px;
        padding: 10px;
    }
    div.stButton > button {
        background-color: #4169E1;
        color: white !important;
        width: 100%;
        border: none;
        padding: 15px 20px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 16px;
        margin-top: 2px;
        text-transform: uppercase;
        box-shadow: 0 5px 15px rgba(65, 105, 225, 0.4);
        white-space: nowrap; /* Prevents button text from breaking into 2 lines */
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. DISPLAY HEADER ---
st.markdown("""
<div class="header-bar">
    <p class="header-text">⛽ GASPAY</p>
    <p class="header-sub">OFFICIAL AMBASSADOR PORTAL</p>
</div>
""", unsafe_allow_html=True)

# --- 4. LOAD DATA ---
# REPLACE WITH YOUR LINK
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3CDt_ulHB-4JN80DKixskyHZhE_caf75oKICt-dirQNmBb3gH9WDNDVrkXY2Y0ja862OV1DXv3y72/pub?output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url, usecols=['Timestamp', 'Referral Code'])
        df = df.dropna(subset=['Referral Code'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Referral Code'] = df['Referral Code'].astype(str).str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data(sheet_url)

if not df.empty:
    payout_per_ref = 100
    current_time = pd.Timestamp.now()
    
    # --- 5. SEARCH SECTION ---
    # We use columns, but on mobile Streamlit will auto-stack them if they get too small
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        search_code = st.text_input("Enter Code", placeholder="e.g. REF_MUBARAK", label_visibility="collapsed").strip()
    with col_btn:
        check_pressed = st.button("CHECK BALANCE")

    if check_pressed and search_code:
        my_data = df[df['Referral Code'].str.lower() == search_code.lower()]
        
        if not my_data.empty:
            today_data = my_data[my_data['Timestamp'].dt.date == current_time.date()]
            earned_today = len(today_data) * payout_per_ref
            
            week_start = current_time - timedelta(days=7)
            week_data = my_data[my_data['Timestamp'] >= week_start]
            earned_week = len(week_data) * payout_per_ref
            
            total_customers = len(my_data)
            total_earned = total_customers * payout_per_ref
            
            # User Results
            st.markdown(f"<h3 style='color: #4169E1 !important; margin-top: 20px;'>👋 Results for {search_code.upper()}</h3>", unsafe_allow_html=True)
            
            # 4 Cards Layout
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("My Total Customers", f"{total_customers}")
            c2.metric("My Earnings Today", f"₦ {earned_today:,.0f}")
            c3.metric("Earnings (Week)", f"₦ {earned_week:,.0f}") # Shortened Title
            c4.metric("Total Earnings", f"₦ {total_earned:,.0f}") # Shortened Title
            st.markdown("---")
            
        else:
            st.error(f"❌ Code '{search_code}' not found.")

    # --- 6. COMPANY STATS ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 800;'>🏆 COMPANY OVERALL PERFORMANCE</h3>", unsafe_allow_html=True)
    
    total_program_customers = len(df)
    total_program_payout = total_program_customers * payout_per_ref
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Customers", f"{total_program_customers:,}")
    k2.metric("Total Payouts", f"₦ {total_program_payout:,.0f}")
    
    month_start = current_time - timedelta(days=30)
    month_data = df[df['Timestamp'] >= month_start]
    k3.metric("30-Day Growth", f"{len(month_data)} New")

    st.markdown("---")

    # --- 7. GRAPHS ---
    st.markdown("<h3 style='font-weight: bold;'>📊 Live Activity Charts</h3>", unsafe_allow_html=True)
    
    earner_df = df['Referral Code'].value_counts().reset_index()
    earner_df.columns = ['Referral Code', 'Count']
    earner_df['Payout'] = earner_df['Count'] * payout_per_ref
    
    config = {'staticPlot': True}

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Top Ambassadors**")
        top_10 = earner_df.head(10)
        
        fig_bar = px.bar(
            top_10, x='Referral Code', y='Payout', text='Payout',
            color_discrete_sequence=['#4169E1'] * len(top_10)
        )
        fig_bar.update_traces(texttemplate='₦%{text:.0f}', textposition='outside')
        fig_bar.update_layout(
            font=dict(color="black", size=12),
            xaxis=dict(tickangle=-45, title=None, tickfont=dict(color="black")),
            yaxis=dict(title=None, tickfont=dict(color="black"), showgrid=True, gridcolor='#E0E0E0'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=30, l=10, r=10, b=50)
        )
        st.plotly_chart(fig_bar, use_container_width=True, config=config)

    with col_right:
        st.markdown("**Growth Trend**")
        daily_growth = df.set_index('Timestamp').resample('D').size().reset_index(name='New Customers')
        
        fig_line = px.line(
            daily_growth, x='Timestamp', y='New Customers', markers=True,
            color_discrete_sequence=['#4169E1']
        )
        fig_line.update_layout(
            font=dict(color="black", size=12),
            xaxis=dict(title=None, tickfont=dict(color="black"), showgrid=True, gridcolor='#E0E0E0'),
            yaxis=dict(title=None, tickfont=dict(color="black"), showgrid=True, gridcolor='#E0E0E0'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=30, l=10, r=10, b=50)
        )
        st.plotly_chart(fig_line, use_container_width=True, config=config)

else:
    st.info("System Offline: Waiting for Google Sheet connection...")