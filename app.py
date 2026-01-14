import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="Referral Dashboard", layout="wide")

st.title("🚀 Referral Program Performance")
st.write("Live analysis of referral payouts and growth.")

# --- 2. LOAD DATA ---
# REPLACE THIS WITH YOUR LINK
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3CDt_ulHB-4JN80DKixskyHZhE_caf75oKICt-dirQNmBb3gH9WDNDVrkXY2Y0ja862OV1DXv3y72/pub?output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url, usecols=['Timestamp', 'Referral Code'])
        df = df.dropna(subset=['Referral Code'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        # Clean whitespace just in case " REF01 " is typed as "REF01"
        df['Referral Code'] = df['Referral Code'].astype(str).str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data(sheet_url)

if not df.empty:
    # --- GLOBAL CALCULATIONS ---
    payout_per_ref = 100
    
    # Calculate counts for everyone
    earner_df = df['Referral Code'].value_counts().reset_index()
    earner_df.columns = ['Referral Code', 'Count']
    earner_df['Payout (₦)'] = earner_df['Count'] * payout_per_ref

    # --- 3. NEW FEATURE: SEARCH BAR ---
    st.divider()
    st.subheader("🔎 Check Your Earnings")
    
    col_search, col_result = st.columns([1, 2])
    
    with col_search:
        # The search box
        search_code = st.text_input("Enter your Referral Code:", placeholder="e.g. REF_MUBARAK").strip()

    with col_result:
        if search_code:
            # Filter data to find the specific code
            user_stat = earner_df[earner_df['Referral Code'].str.lower() == search_code.lower()]
            
            if not user_stat.empty:
                # Get the numbers
                my_count = user_stat.iloc[0]['Count']
                my_payout = user_stat.iloc[0]['Payout (₦)']
                
                # Show the Big Green Card
                st.success(f"### 🎉 Results for {search_code}")
                c1, c2 = st.columns(2)
                c1.metric("Your Total Referrals", f"{my_count}")
                c2.metric("Your Total Earnings", f"₦ {my_payout:,.0f}")
            else:
                st.warning(f"Code '{search_code}' not found. Check your spelling!")
        else:
            st.info("Type a code on the left to see specific stats.")

    st.divider()

    # --- 4. GLOBAL DASHBOARD (Total Stats) ---
    st.subheader("📊 Global Program Stats")
    
    # Row 1: The Scoreboard
    total_referrals = len(df)
    total_payout = total_referrals * payout_per_ref
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Referrals (All Time)", f"{total_referrals:,}")
    col2.metric("Total Payouts Due", f"₦ {total_payout:,.0f}")
    
    # Velocity
    last_7_days = df[df['Timestamp'] > (pd.Timestamp.now() - pd.Timedelta(days=7))]
    col3.metric("Last 7 Days Activity", f"{len(last_7_days)} New Refs")

    # Row 2: Charts
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("🏆 Top Earners Leaderboard")
        top_n = st.slider("Show Top N Earners:", 5, 50, 10)
        top_earners = earner_df.head(top_n)
        
        fig_bar = px.bar(top_earners, x='Referral Code', y='Payout (₦)',
                         text='Payout (₦)', title=f"Top {top_n} Earners",
                         color='Payout (₦)', color_continuous_scale='Greens')
        fig_bar.update_traces(texttemplate='₦%{text:.0f}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("📈 Growth Trend")
        daily_growth = df.set_index('Timestamp').resample('D').size().reset_index(name='Daily Referrals')
        fig_line = px.line(daily_growth, x='Timestamp', y='Daily Referrals', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)