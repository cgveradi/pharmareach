import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "pharmareach_logo.png")

st.set_page_config(
    page_title="PharmaReach HVT Module",
    page_icon=logo_path if os.path.exists(logo_path) else "⚛️",
    layout="wide"
)

# --- MAIN HEADER WITH SYSTEM STATUS ---
head_col1, head_col2, head_col3 = st.columns([1, 3, 1])

with head_col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=600)
    else:
        st.write("⚛️")

with head_col2:
    st.markdown(
        "<h2 style='margin-bottom: 0px; padding-bottom: 0px; margin-left: 50px; margin-top: 50px; padding-bottom: 0;'>STRATEGIC HVT FINDER</h2>"
        "<p style='font-style: italic;margin-top: 0px; margin-left: 95px; color: #18BC9C; font-weight: 700;'>Unified Clinical Intelligence Platform</p>",
        unsafe_allow_html=True
    )

with head_col3:
    st.write("")  # Spacer
    st.markdown(
        "<div style='text-align: right; border-left: 2px solid #18BC9C; padding-left: 10px;'>"
        "<span style='color: #18BC9C; font-weight: bold;'>🟢 SYSTEM ONLINE</span><br>"
        "<span style='font-size: 0.8em; color: gray;'>DATABASE: JAN 2026</span><br>"
        "<span style='font-size: 0.8em; color: gray;'>VERSION: 1.0.1</span>"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()
# --- BRANDING & CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@700&family=Lato:wght@400;700&display=swap');

        html, body, [class*="css"], .stMarkdown, p, span, label {
            font-family: 'Lato', sans-serif !important;
        }

        h1, h2, h3, b, strong, [data-testid="stMetricValue"] {
            font-family: 'Barlow', sans-serif !important;
        }

        [data-testid="stSidebar"] { background-color: #002626; }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMetric label { color: white !important; }
        
        div.stButton > button:first-child {
            background-color: #18BC9C;
            color: white;
            border-radius: 8px;
            font-family: 'Barlow', sans-serif;
            font-weight: 700;
            height: 3em;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Data Engine


def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(
        current_dir, "..", "reports", "PharmaReach_Final_Strategy_Report.csv"))
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    return pd.read_csv(csv_path)


if 'df' not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# 3. Sidebar Configuration
st.sidebar.metric("TOTAL PHYSICIANS ANALYZED", f"{len(df):,}")
st.sidebar.divider()
st.sidebar.header("SEARCH FILTERS")
target_specialty = st.sidebar.selectbox(
    "SELECT SPECIALTY", sorted(df['specialty'].unique()))
target_city = st.sidebar.text_input("ENTER CITY", "New York")

# 4. Filter & Result Logic
if st.button('IDENTIFY HIGH-VALUE TARGETS'):
    clean_city = target_city.strip().title()
    results = df[(df['specialty'] == target_specialty) & (
        df['city'].str.contains(target_city, case=False, na=False))]
    top_5 = results.sort_values(by='lead_score', ascending=False).head(5)

    if not top_5.empty:
        market_leader = results.groupby('primary_manufacturer')[
            'total_spend'].sum().idxmax()
        st.success(
            f"**MARKET INTELLIGENCE:** {market_leader} is the dominant investor in {clean_city} for {target_specialty}.")

        st.subheader(
            f"TOP 5 {target_specialty.upper()} TARGETS IN {clean_city.upper()}")

        for i, row in top_5.iterrows():
            with st.expander(f"⭐ {row['full_name']} | LEAD SCORE: {row['lead_score']:.1f}"):
                sci_ratio = (row['research_spend'] / row['total_spend']
                             ) * 100 if row['total_spend'] > 0 else 0

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("SEGMENT", row['segment_name'])
                c2.metric("SCIENTIFIC DNA 🧬", f"{sci_ratio:.1f}%")
                c3.metric("MARKET LOYALTY 🔒", f"{row['mfg_loyalty_pct']:.1f}%")
                c4.metric("TOP RIVAL", row['primary_manufacturer'])

                st.markdown(
                    f"**Annual Strategic Spend:** `${row['total_spend']:,.0f}`")
                st.progress(row['lead_score'] / 100)

        st.divider()
        csv_download = top_5.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD TACTICAL LIST (CSV)",
                           csv_download, f"PharmaReach_{clean_city}.csv", "text/csv")
        st.caption(
            "ℹ️ Ranking based on Weighted Lead Score (70% Volume | 30% Scientific Authority)")
    else:
        st.error(
            "No physicians found. Please verify spelling or try a major metropolitan hub.")

st.sidebar.markdown("---")
st.sidebar.markdown("**PharmaReach v1.0.1**")
