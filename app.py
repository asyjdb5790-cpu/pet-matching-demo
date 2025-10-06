import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="走失寵物資訊平台", page_icon="🐾", layout="centered")

st.title("🐶 走失寵物資訊平台 Demo")

# --- 選單 ---
st.sidebar.header("📋 搜尋條件")
search_mode = st.sidebar.selectbox("選擇模式", ["🔍 搜尋走失寵物", "📤 登錄走失資訊"])

# --- 建立資料庫 ---
if not os.path.exists("lost_pets.csv"):
    df = pd.DataFrame(columns=["名稱","品種","地區","日期","圖片"])
    df.to_csv("lost_pets.csv", index=False)

# --- 搜尋模式 ---
if search_mode == "🔍 搜尋走失寵物":
    breed = st.selectbox("選擇品種", ["不限", "柴犬", "米克斯", "拉布拉多", "貓咪"])
    area = st.selectbox("選擇地區", ["不限", "高雄", "台南", "台中", "台北"])
    st.write("🔎 搜尋結果：")

    df = pd.read_csv("lost_pets.csv")
    if breed != "不限":
        df = df[df["品種"] == breed]
    if area != "不限":
        df = df[df["地區"] == area]

    if df.empty:
        st.warning("目前沒有符合條件的資料。")
    else:
        for i, row in df.iterrows():
            st.subheader(f"🐾 {row['名稱']} - {row['品種']}")
            st.write(f"📍 地區：{row['地區']}　📅 日期：{row['日期']}")
            if os.path.exists(row["圖片"]):
                st.image(row["圖片"], width=300)

# --- 登錄模式 ---
else:
    st.header("📤 上傳走失寵物資料")
    name = st.text_input("寵物名稱")
    breed = st.selectbox("品種", ["柴犬", "米克斯", "拉布拉多", "貓咪"])
    area = st.selectbox("地區", ["高雄", "台南", "台中", "台北"])
    date = st.date_input("走失日期")
    photo = st.file_uploader("上傳寵物照片", type=["jpg", "png"])

    if photo and name:
        img = Image.open(photo)
        img_path = f"images/{name}.png"
        os.makedirs("images", exist_ok=True)
        img.save(img_path)

        new_data = pd.DataFrame([[name, breed, area, date, img_path]], 
                                columns=["名稱","品種","地區","日期","圖片"])
        df = pd.read_csv("lost_pets.csv")
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("lost_pets.csv", index=False)
        st.success("✅ 已成功登錄資料！")
        st.image(img, caption=f"{name} 的照片", width=300)
