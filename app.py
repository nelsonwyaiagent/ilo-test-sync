import streamlit as st
import pandas as pd
import requests
from io import StringIO

# --- CONFIGURATION ---
GITHUB_USER = "nelsonwyaiagent"
REPO_NAME = "ilo-test-sync"
FILE_NAME = "inventory.csv"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/{FILE_NAME}"

st.set_page_config(
    page_title="HPE iLO Hardware Inventory",
    page_icon="🖥️",
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    try:
        response = requests.get(RAW_URL)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        else:
            st.error(f"Could not fetch data from GitHub. Status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

st.title("🖥️ HPE iLO Hardware Inventory")
st.markdown("Real-time hardware specifications synced from iLO management interfaces.")

df = load_data()

if df is not None:
    # --- TOP METRICS ---
    col1, col2, col3 = st.columns(3)
    
    total_servers = len(df)
    # We now count unique sockets/servers instead of cores
    total_sockets = total_servers # Simplified: 1 server = 1 entry in this list
    total_ram = df['RAM_GB'].sum()
    
    col1.metric("Total Servers", total_servers)
    col2.metric("Total CPU Sockets", total_sockets)
    col3.metric("Total Memory", f"{total_ram} GB")

    st.markdown("---")

    # --- SEARCH AND FILTER ---
    st.subheader("📦 Detailed Inventory")
    search_term = st.text_input("🔍 Search by Server Name, IP, or Model", "")
    
    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df

    # Display the table
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    st.caption(f"Last synced from GitHub: {RAW_URL}")
else:
    st.warning("Waiting for inventory data to be uploaded to GitHub...")
