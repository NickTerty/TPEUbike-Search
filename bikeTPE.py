import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="臺北Youbike查詢", layout="centered")
st.title("Youbike 臺北即時資料查詢")

# JSON 來源網址
url_tpe = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'

# 嘗試抓資料
try:
    req = requests.get(url_tpe, timeout=10)
    data = req.json()
    df = pd.DataFrame(data)

    # 取出行政區清單
    areas = sorted(df['sarea'].unique())

    # 建立選單（預設顯示第一個行政區）
    selected_area = st.selectbox("請選擇要查詢的行政區：", areas, index=0)

    # 篩選出該行政區的資料
    df_area = df[df['sarea'] == selected_area]

    # 顯示站點資訊
    df_show = df_area[['sna', 'ar', 'available_rent_bikes', 'available_return_bikes']].copy()
    df_show.columns = ['站名', '地址', '可借車數', '可還車數']

    st.subheader(f"📍 {selected_area} 站點列表")
    st.dataframe(df_show, use_container_width=True)
    st.info(f"目前 {selected_area} 共有 {len(df_show)} 個站點")

except Exception as e:
    st.error(f"資料取得失敗：{e}")
