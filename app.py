import streamlit as st
import pandas as pd
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

    /* HEADER BAR */
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

    /* MOBILE ADJUSTMENTS */
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
        div.stButton > button {
            padding: 12px 10px !important;
            font-size: 14px !important;
        }
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
        font-size: 28px !important;
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
        white-space: nowrap;
    }

    /* CUSTOM TABLE STYLE (FIXES DARK MODE ISSUE) */
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 18px;
        width: 100%;
        border-radius: 10px 10px 0 0;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
        font-family: 'Helvetica Neue', sans-serif;
    }
    .styled-table thead tr {
        background-color: #4169E1; /* Royal Blue Header */
        color: #ffffff !important;
        text-align: left;
    }
    .styled-table th, .styled-table td {
        padding: 12px 15px;
        color: #000000 !important; /* Force Black Text */
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
        background-color: #ffffff; /* Force White Row Background */
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3; /* Light Grey Striping */
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #4169E1;
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

# --- 4. LOAD DATA (NO ZEROS) ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3CDt_ulHB-4JN80DKixskyHZhE_caf75oKICt-dirQNmBb3gH9WDNDVrkXY2Y0ja862OV1DXv3y72/pub?output=csv"

@st.cache_data(ttl=10)
def load_data(url):
    try:
        df = pd.read_csv(url, usecols=['Timestamp', 'Referral Code'])
        df = df.dropna(subset=['Referral Code'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Referral Code'] = df['Referral Code'].astype(str).str.strip()
        # Remove "0" codes
        df = df[df['Referral Code'] != '0']
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data(sheet_url)

if not df.empty:
    payout_per_ref = 100
    current_time = pd.Timestamp.now()
    
    # --- 5. SEARCH SECTION ---
    st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 10px;'>Enter your referral code to see how much you've made</p>", unsafe_allow_html=True)
    
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
            
            st.markdown(f"<h3 style='color: #4169E1 !important; margin-top: 20px;'>👋 Results for {search_code.upper()}</h3>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("My Order No", f"{total_customers}") # Renamed as requested? Contextually "Order No" means Count here.
            c2.metric("My Earnings Today", f"₦ {earned_today:,.0f}")
            c3.metric("Earnings (Week)", f"₦ {earned_week:,.0f}")
            c4.metric("Total Earnings", f"₦ {total_earned:,.0f}")
            st.markdown("---")
            
        else:
            st.error(f"❌ Code '{search_code}' not found.")

    # --- 6. OVERALL AMBASSADORS PERFORMANCE (FUNAAB) ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 800;'>🏆 Overall Ambassadors Performance (FUNAAB)</h3>", unsafe_allow_html=True)
    
    total_program_customers = len(df)
    total_program_payout = total_program_customers * payout_per_ref
    total_ambassadors = df['Referral Code'].nunique()
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Total customers onboarded", f"{total_program_customers:,}")
    k2.metric("Total Payouts from Gasfeel", f"₦ {total_program_payout:,.0f}")
    k3.metric("Total Number of Ambassadors", f"{total_ambassadors}")

    st.markdown("---")

    # --- 7. LEADERBOARD (HTML TABLE - FORCED COLORS) ---
    st.markdown("<h3 style='font-weight: bold; text-align: center; margin-bottom: 20px;'>📜 LEADERBOARD</h3>", unsafe_allow_html=True)
    
    # Prepare Data
    earner_df = df['Referral Code'].value_counts().reset_index()
    earner_df.columns = ['Ambassador Name', 'Order No'] # RENAMED HERE
    earner_df['Total Earnings'] = earner_df['Order No'] * payout_per_ref
    earner_df = earner_df.sort_values(by='Total Earnings', ascending=False).reset_index(drop=True)
    
    # Add Rank Column
    earner_df.insert(0, 'Rank', earner_df.index + 1)
    
    # Format Money Column for Display
    earner_df['Total Earnings'] = earner_df['Total Earnings'].apply(lambda x: f"₦ {x:,.0f}")
    
    # Convert to HTML Table
    table_html = earner_df.to_html(index=False, classes="styled-table", justify="left", border=0)
    
    # Inject HTML Table
    st.markdown(table_html, unsafe_allow_html=True)

else:
    st.info("System Offline: Waiting for Google Sheet connection...")
