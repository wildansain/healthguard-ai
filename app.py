import streamlit as st
import pandas as pd

from assets.style import load_css
from utils.loader import load_model_resources
from utils.preprocessing import preprocess_data

from modules.dashboard import show_dashboard
from modules.manual_claim import show_manual_claim
from modules.batch_process import show_batch_process

st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🏥",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

model, encoders = load_model_resources()

with st.sidebar:

    st.markdown(
        """
        # 🏥 HealthGuard AI
        ### Claim Analytics Platform
        """
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Excel",
        type=["xlsx"]
    )

    if uploaded_file:
        menu = st.radio(
            "MENU",
            [
                "📊 Dashboard & Filter",
                "🩺 Cek Klaim Manual",
                "📥 Batch Process & Export"
            ]
        )
    else:
        menu = None

if uploaded_file is None:

    st.markdown("# 🏥 HealthGuard AI")

    st.markdown(
        """
        ### Intelligent Healthcare Claim Analytics Platform

        Solusi analisis klaim kesehatan berbasis **Artificial Intelligence**,
        **Machine Learning**, dan **Anomaly Detection** untuk membantu proses
        verifikasi klaim secara cepat, akurat, dan efisien.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("## 📊")
        st.subheader("Dashboard Analytics")
        st.caption(
            "Visualisasi data klaim dan insight bisnis secara real-time."
        )

    with col2:
        st.markdown("## 🩺")
        st.subheader("Manual Claim Assessment")
        st.caption(
            "Evaluasi klaim berdasarkan plan dan limit manfaat."
        )

    with col3:
        st.markdown("## 🤖")
        st.subheader("AI Anomaly Detection")
        st.caption(
            "Deteksi otomatis klaim mencurigakan menggunakan Machine Learning."
        )

    st.write("")
    st.write("")

    st.info(
        """
        🚀 **Mulai Analisis**

        Upload file Excel pada panel sebelah kiri untuk mengakses:

        • Dashboard & Analytics  
        • Manual Claim Assessment  
        • AI Anomaly Detection & Export
        """
    )

else:

    df_raw = pd.read_excel(
        uploaded_file,
        header=1
    )

    df = preprocess_data(df_raw)

    if menu == "📊 Dashboard & Filter":
        show_dashboard(df)

    elif menu == "🩺 Cek Klaim Manual":
        show_manual_claim()

    elif menu == "📥 Batch Process & Export":
        show_batch_process(
            df,
            df_raw,
            uploaded_file
        )