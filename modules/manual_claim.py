import streamlit as st


def show_manual_claim():

    st.markdown("### 🩺 Intelligent Claim Assessment")
    st.write(
        "Analisis kelayakan klaim berdasarkan plan yang dipilih."
    )

    # =========================
    # DATA PLAN
    # =========================
    PLAN_DATA = {
        "PLAN RI 400": {
            "type": "RI",
            "limit": 30000000,
            "per_hari": 400000
        },
        "PLAN RI 500": {
            "type": "RI",
            "limit": 35000000,
            "per_hari": 500000
        },
        "PLAN RI 750": {
            "type": "RI",
            "limit": 40000000,
            "per_hari": 750000
        },
        "PLAN RI 950": {
            "type": "RI",
            "limit": 60000000,
            "per_hari": 950000
        },
        "PLAN RI 1200": {
            "type": "RI",
            "limit": 70000000,
            "per_hari": 1200000
        },

        "PLAN RJ 400": {
            "type": "RJ",
            "limit": 5550000
        },
        "PLAN RJ 500": {
            "type": "RJ",
            "limit": 6500000
        },
        "PLAN RJ 750": {
            "type": "RJ",
            "limit": 8500000
        },
        "PLAN RJ 950": {
            "type": "RJ",
            "limit": 11000000
        },
        "PLAN RJ 1200": {
            "type": "RJ",
            "limit": 11000000
        },
    }

    # =========================
    # PILIH PLAN
    # =========================
    plan = st.selectbox(
        "📋 Pilih Plan",
        list(PLAN_DATA.keys())
    )

    data_plan = PLAN_DATA[plan]

    st.markdown("---")

    # =========================
    # FORM INPUT
    # =========================
    with st.form("manual_form"):

        col1, col2 = st.columns(2)

        with col1:
            diajukan = st.number_input(
                "Jumlah Klaim (Rp)",
                min_value=0,
                value=0,
                step=100000
            )

        with col2:

            if data_plan["type"] == "RI":

                durasi = st.number_input(
                    "Durasi Rawat Inap (Hari)",
                    min_value=0,
                    value=0,
                    step=1
                )

            else:

                durasi = 0

                st.caption(
                    "ℹ️ Plan rawat jalan tidak memerlukan durasi rawat inap."
                )

        submitted = st.form_submit_button(
            "🔍 Analisis Klaim"
        )

    # =========================
    # PROSES ANALISIS
    # =========================
    if submitted:

        if diajukan <= 0:
            st.warning(
                "⚠️ Masukkan jumlah klaim terlebih dahulu."
            )
            return

        if data_plan["type"] == "RI" and durasi <= 0:
            st.warning(
                "⚠️ Masukkan durasi rawat inap."
            )
            return

        limit = data_plan["limit"]

        st.markdown("---")

        # =========================
        # RAWAT INAP
        # =========================
        if data_plan["type"] == "RI":

            limit_kamar = (
                data_plan["per_hari"] * durasi
            )

            if diajukan <= limit_kamar:
                hasil = "APPROVED"

            elif diajukan <= (limit_kamar * 1.1):
                hasil = "CONSIDERED"

            else:
                hasil = "REJECTED"

            c1, c2 = st.columns(2)

            with c1:
                st.info(
                    f"💡 Limit Tahunan: Rp {limit:,.0f}"
                )

            with c2:
                st.info(
                    f"💡 Estimasi Limit Kamar: Rp {limit_kamar:,.0f}"
                )

        # =========================
        # RAWAT JALAN
        # =========================
        else:

            if diajukan <= limit:
                hasil = "APPROVED"

            elif diajukan <= (limit * 1.1):
                hasil = "CONSIDERED"

            else:
                hasil = "REJECTED"

            st.info(
                f"💡 Limit Rawat Jalan: Rp {limit:,.0f}"
            )

        st.markdown("---")

        # =========================
        # HASIL
        # =========================
        if hasil == "APPROVED":

            st.success(
                "✅ Klaim berada dalam batas limit dan direkomendasikan untuk disetujui."
            )

        elif hasil == "CONSIDERED":

            st.warning(
                "⚠️ Klaim sedikit melebihi batas limit dan memerlukan review lebih lanjut."
            )

        else:

            st.error(
                "❌ Klaim melebihi batas limit secara signifikan dan direkomendasikan untuk ditolak."
            )

        # =========================
        # RINGKASAN
        # =========================
        st.markdown("### 📋 Ringkasan Analisis")

        st.write(f"**Plan:** {plan}")
        st.write(f"**Nominal Klaim:** Rp {diajukan:,.0f}")

        if data_plan["type"] == "RI":
            st.write(f"**Durasi Rawat Inap:** {durasi} Hari")

        st.write(f"**Status Rekomendasi:** {hasil}")