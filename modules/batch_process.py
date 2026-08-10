import streamlit as st
import pandas as pd

from utils.anomaly import (
    detect_anomaly,
    export_anomaly_excel
)


def show_batch_process(df, df_raw, uploaded_file):

    st.markdown("### 📥 Batch Processing - AI Anomaly Detection")

    st.write(
        "Deteksi klaim anomali menggunakan kombinasi Machine Learning & Rule-Based Insight."
    )

    st.info(
        f"File terdeteksi: **{uploaded_file.name}** ({len(df)} baris data)"
    )

    if "hasil_excel" not in st.session_state:
        st.session_state["hasil_excel"] = None

    if "df_anomali" not in st.session_state:
        st.session_state["df_anomali"] = None

    if st.button(
        "🚀 Jalankan Deteksi Anomali",
        type="primary"
    ):

        with st.spinner(
            "🔍 Menganalisis data klaim..."
        ):

            try:

                anomali_df = detect_anomaly(
                    df_raw
                )

                hasil_excel = (
                    export_anomaly_excel(
                        anomali_df
                    )
                )

                st.session_state[
                    "hasil_excel"
                ] = hasil_excel

                st.session_state[
                    "df_anomali"
                ] = anomali_df

                st.success(
                    f"✅ Selesai! Ditemukan {len(anomali_df)} data anomali."
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    if st.session_state["df_anomali"] is not None:

        df_show = st.session_state["df_anomali"]

        st.markdown("---")

        st.download_button(
            label="📥 Download Excel Anomali",
            data=st.session_state["hasil_excel"],
            file_name="hasil_anomali.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # =========================
        # RINGKASAN HASIL DETEKSI
        # =========================

        st.markdown("### 📊 Ringkasan Hasil Deteksi")

        high_risk = len(
            df_show[
                df_show["Risk_Level"]
                .str.contains("HIGH", na=False)
            ]
        )

        medium_risk = len(
            df_show[
                df_show["Risk_Level"]
                .str.contains("MEDIUM", na=False)
            ]
        )

        persentase_anomali = (
            len(df_show) / len(df) * 100
            if len(df) > 0
            else 0
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Jumlah Anomali",
                len(df_show)
            )

        with col2:
            st.metric(
                "High Risk",
                high_risk
            )

        with col3:
            st.metric(
                "Medium Risk",
                medium_risk
            )

        col4, col5 = st.columns(2)

        with col4:
            st.metric(
                "Persentase Anomali",
                f"{persentase_anomali:.2f}%"
            )

        with col5:

            if (
                "nama provider" in df_show.columns
                and not df_show["nama provider"].isna().all()
            ):

                provider_count = (
                    df_show["nama provider"]
                    .value_counts()
                )

                provider_terbanyak = (
                    provider_count.idxmax()
                )

                jumlah_provider = (
                    provider_count.max()
                )

                st.metric(
                    "Provider Terbanyak",
                    f"{provider_terbanyak} ({jumlah_provider})"
                )

            else:

                st.metric(
                    "Provider Terbanyak",
                    "-"
                )

        # =========================
        # HIGHLIGHT DATA ANOMALI
        # =========================

        st.markdown(
            "### 🎯 Highlight Data Anomali"
        )

        def highlight_row(row):

            if "HIGH" in str(row["Risk_Level"]):
                return [
                    "background-color:#7f1d1d"
                ] * len(row)

            if "MEDIUM" in str(row["Risk_Level"]):
                return [
                    "background-color:#92400e"
                ] * len(row)

            return [""] * len(row)

        # Hapus kolom yang semuanya kosong
        df_display = df_show.dropna(
            axis=1,
            how="all"
        )

        # Hapus kolom teknis yang tidak perlu
        kolom_hide = [
            "anomali"
        ]

        df_display = df_display.drop(
            columns=[
                c for c in kolom_hide
                if c in df_display.columns
            ],
            errors="ignore"
        )

        st.dataframe(
            df_display.style.apply(
                highlight_row,
                axis=1
            ),
            use_container_width=True
        )

        # =========================
        # RESET
        # =========================

        if st.button("🔄 Reset"):

            st.session_state[
                "hasil_excel"
            ] = None

            st.session_state[
                "df_anomali"
            ] = None

            st.rerun()
        
        st.markdown("---")

        st.markdown("### 📖 Dasar Klasifikasi Anomali")

        st.write("""
        Data dikategorikan sebagai anomali menggunakan algoritma Isolation Forest yang mendeteksi pola klaim yang berbeda dari mayoritas data.

        Setelah anomali terdeteksi, sistem memberikan interpretasi dan tingkat risiko berdasarkan indikator-indikator berikut.
        """)

        parameter_df = pd.DataFrame({
            "Parameter": [
                "Nominal Klaim Tinggi",
                "Rasio Persetujuan Rendah",
                "Durasi Perawatan Tinggi",
                "Pola Tidak Umum",
                "HIGH RISK",
                "MEDIUM RISK"
            ],
            "Kriteria": [
                "Masuk kelompok 5% nominal klaim tertinggi pada dataset",
                "Masuk kelompok 5% rasio persetujuan terendah pada dataset",
                "Masuk kelompok 5% durasi perawatan terlama pada dataset",
                "Memiliki pola yang berbeda dari mayoritas data menurut Isolation Forest",
                "Memenuhi 2 atau lebih indikator anomali",
                "Memenuhi 1 indikator anomali atau hanya terdeteksi oleh Isolation Forest"
            ]
        })

        st.dataframe(
            parameter_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            """
            Catatan:
            Threshold indikator dihitung secara otomatis menggunakan metode persentil
            sehingga menyesuaikan karakteristik dataset yang dianalisis.
            """
        )