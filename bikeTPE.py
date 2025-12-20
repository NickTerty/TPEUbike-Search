import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="臺北Youbike查詢", layout="centered")
st.title("Youbike 臺北即時資料查詢")

# JSON url source
url_tpe = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'

# try to find datas
try:
    req = requests.get(url_tpe, timeout=10)
    data = req.json()
    df = pd.DataFrame(data)

    # List all administrative districts of Taipei
    areas = sorted(df['sarea'].unique())

    # Create the selecting list with the first district as default
    selected_area = st.selectbox("請選擇要查詢的行政區：", areas, index=0)

    # Filter out the data for this district
    df_area = df[df['sarea'] == selected_area]

    # Show the data of sites
    df_show = df_area[['sna', 'ar', 'available_rent_bikes', 'available_return_bikes']].copy()
    df_show.columns = ['站名', '地址', '可借車數', '可還車數']

    st.subheader(f"📍 {selected_area} 站點列表")
    st.dataframe(df_show, use_container_width=True)
    st.info(f"目前 {selected_area} 共有 {len(df_show)} 個站點")

# If it was not found or unsuccessful, show it failed
except Exception as e:
    st.error(f"資料取得失敗：{e}")
