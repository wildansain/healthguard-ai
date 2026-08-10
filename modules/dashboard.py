import streamlit as st
import plotly.express as px

def show_dashboard(df):

    st.markdown("### 📊 Executive Dashboard")

    # Filter Tahun
    cols_filter = st.columns(2)

    with cols_filter[0]:
        if 'tahun' in df.columns:
            unique_years = sorted(
                df['tahun'].dropna().astype(int).unique(),
                reverse=True
            )

            opt_years = ["Semua Tahun"] + list(unique_years)

            selected_year = st.selectbox(
                "📅 Filter Periode:",
                opt_years
            )
        else:
            selected_year = "Semua Tahun"

    # Logika Filter
    if selected_year != "Semua Tahun":
        df_display = df[df['tahun'] == selected_year]
    else:
        df_display = df

    # KPI
    c1, c2, c3, c4 = st.columns(4)

    total_diajukan = (
        df_display['diajukan'].sum()
        if not df_display.empty else 0
    )

    total_disetujui = (
        df_display['disetujui'].sum()
        if "disetujui" in df_display.columns else 0
    )

    rate = (
        (total_disetujui / total_diajukan) * 100
        if total_diajukan > 0 else 0
    )

    with c1:
        st.metric(
            "Total Pengajuan",
            f"Rp {total_diajukan/1e9:,.1f} M"
        )

    with c2:
        st.metric(
            "Total Disetujui",
            f"Rp {total_disetujui/1e9:,.1f} M"
        )

    with c3:
        st.metric(
            "Approval Rate",
            f"{rate:.1f}%"
        )

    with c4:
        st.metric(
            "Jumlah Kasus",
            f"{len(df_display):,}"
        )

    st.markdown("---")

    # =========================
    # GRAFIK
    # =========================

    g1, g2 = st.columns(2)

    with g1:

        st.markdown("#### 📍 Top 10 Diagnosa")

        if "diagnosa" in df_display.columns:

            top_diag = (
                df_display["diagnosa"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            top_diag.columns = [
                "Diagnosa",
                "Jumlah"
            ]

            fig = px.bar(
                top_diag,
                x="Jumlah",
                y="Diagnosa",
                orientation="h",
                color="Jumlah",
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with g2:

        st.markdown("#### 🏥 Top Provider")

        if "nama provider" in df_display.columns:

            top_provider = (
                df_display["nama provider"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            top_provider.columns = [
                "Provider",
                "Jumlah"
            ]

            fig2 = px.pie(
                top_provider,
                names="Provider",
                values="Jumlah",
                hole=0.5
            )

            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=450
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )
    
    st.markdown("---")

    st.markdown("#### 📈 Tren Klaim")

    if "tanggal berobat" in df_display.columns:

        trend_data = (
            df_display
            .groupby("tanggal berobat")["diajukan"]
            .sum()
            .reset_index()
        )

        fig3 = px.area(
            trend_data,
            x="tanggal berobat",
            y="diajukan"
        )

        fig3.update_traces(
            line_color="#0EA5E9",
            fillcolor="rgba(14,165,233,0.25)"
        )

        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=500
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )