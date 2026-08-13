import streamlit as st


# =========================================================
# FORMAT RUPIAH
# =========================================================

def format_rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")


# =========================================================
# MANUAL CLAIM
# =========================================================

def show_manual_claim():

    st.markdown("### 🩺 Intelligent Claim Assessment")

    st.write(
        "Analisis kelayakan klaim berdasarkan jenis plan, "
        "limit tahunan, harga kamar per hari, dan durasi perawatan."
    )

    # =====================================================
    # DATA PLAN
    # =====================================================

    PLAN_DATA = {

        # =================================================
        # RAWAT INAP
        # =================================================

        "RI": {

            "400": {
                "limit_tahunan": 30_000_000,
                "per_hari": 400_000
            },

            "500": {
                "limit_tahunan": 35_000_000,
                "per_hari": 500_000
            },

            "750": {
                "limit_tahunan": 40_000_000,
                "per_hari": 750_000
            },

            "950": {
                "limit_tahunan": 60_000_000,
                "per_hari": 950_000
            },

            "1200": {
                "limit_tahunan": 70_000_000,
                "per_hari": 1_200_000
            }
        },

        # =================================================
        # RAWAT JALAN
        # =================================================

        "RJ": {

            "400": {
                "limit_tahunan": 5_550_000
            },

            "500": {
                "limit_tahunan": 6_500_000
            },

            "750": {
                "limit_tahunan": 8_500_000
            },

            "950": {
                "limit_tahunan": 11_000_000
            },

            "1200": {
                "limit_tahunan": 11_000_000
            }
        }
    }

    # =====================================================
    # INFORMASI PLAN RI
    # =====================================================

    st.markdown("### 🏥 Informasi Plan Rawat Inap (RI)")

    ri_table = []

    for kelas, data in PLAN_DATA["RI"].items():

        ri_table.append({
            "PLAN": f"PLAN RI {kelas}",
            "Limit / Tahun": format_rupiah(
                data["limit_tahunan"]
            ),
            "Kamar / Hari": format_rupiah(
                data["per_hari"]
            )
        })

    st.dataframe(
        ri_table,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # INFORMASI PLAN RJ
    # =====================================================

    st.markdown("### 🚶 Informasi Plan Rawat Jalan (RJ)")

    rj_table = []

    for kelas, data in PLAN_DATA["RJ"].items():

        rj_table.append({
            "PLAN": f"PLAN RJ {kelas}",
            "Limit Rawat Jalan": format_rupiah(
                data["limit_tahunan"]
            )
        })

    st.dataframe(
        rj_table,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # =====================================================
    # PILIH JENIS PLAN
    # =====================================================

    st.markdown("### 🔍 Cek Klaim Manual")

    jenis_plan = st.selectbox(
        "📋 Pilih Jenis Plan",
        [
            "PLAN RI",
            "PLAN RJ"
        ]
    )

    if jenis_plan == "PLAN RI":
        tipe = "RI"
    else:
        tipe = "RJ"

    # =====================================================
    # PILIH KELAS PLAN
    # =====================================================

    kelas = st.selectbox(
        "📌 Pilih Plan",
        [
            "400",
            "500",
            "750",
            "950",
            "1200"
        ]
    )

    data_plan = PLAN_DATA[tipe][kelas]

    nama_plan = f"PLAN {tipe} {kelas}"

    st.markdown("---")

    # =====================================================
    # INFORMASI PLAN TERPILIH
    # =====================================================

    st.markdown("### 📌 Informasi Plan Terpilih")

    if tipe == "RI":

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                f"""
                **Plan**

                {nama_plan}
                """
            )

        with col2:

            st.info(
                f"""
                **Limit Tahunan**

                {format_rupiah(
                    data_plan["limit_tahunan"]
                )}
                """
            )

        with col3:

            st.info(
                f"""
                **Kamar / Hari**

                {format_rupiah(
                    data_plan["per_hari"]
                )}
                """
            )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                f"""
                **Plan**

                {nama_plan}
                """
            )

        with col2:

            st.info(
                f"""
                **Limit Rawat Jalan**

                {format_rupiah(
                    data_plan["limit_tahunan"]
                )}
                """
            )

    st.markdown("---")

    # =====================================================
    # FORM INPUT
    # =====================================================

    st.markdown("### 📝 Input Data Klaim")

    with st.form("manual_form"):

        # -------------------------------------------------
        # JUMLAH KLAIM
        # -------------------------------------------------

        diajukan = st.number_input(
            "💰 Jumlah Klaim (Rp)",
            min_value=0,
            value=0,
            step=100_000
        )

        # -------------------------------------------------
        # RAWAT INAP
        # -------------------------------------------------

        if tipe == "RI":

            durasi = st.number_input(
                "🛏️ Durasi Rawat Inap (Hari)",
                min_value=1,
                value=1,
                step=1
            )

            st.caption(
                "Limit kamar: "
                + format_rupiah(
                    data_plan["per_hari"]
                )
                + " per hari"
            )

        # -------------------------------------------------
        # RAWAT JALAN
        # -------------------------------------------------

        else:

            durasi = 0

            st.caption(
                "ℹ️ Rawat jalan tidak memerlukan durasi rawat inap."
            )

        # -------------------------------------------------
        # BUTTON
        # -------------------------------------------------

        submitted = st.form_submit_button(
            "🔍 Analisis Klaim",
            use_container_width=True
        )

    # =====================================================
    # PROSES ANALISIS
    # =====================================================

    if submitted:

        # =================================================
        # VALIDASI JUMLAH KLAIM
        # =================================================

        if diajukan <= 0:

            st.warning(
                "⚠️ Masukkan jumlah klaim terlebih dahulu."
            )

            return

        # =================================================
        # VALIDASI DURASI RI
        # =================================================

        if tipe == "RI" and durasi <= 0:

            st.warning(
                "⚠️ Masukkan durasi rawat inap."
            )

            return

        # =================================================
        # RAWAT INAP
        # =================================================

        if tipe == "RI":

            # ---------------------------------------------
            # LIMIT TAHUNAN
            # ---------------------------------------------

            limit_tahunan = data_plan[
                "limit_tahunan"
            ]

            # ---------------------------------------------
            # LIMIT BERDASARKAN DURASI
            # ---------------------------------------------

            limit_kamar = (
                data_plan["per_hari"] * durasi
            )

            # ---------------------------------------------
            # LIMIT EFEKTIF
            #
            # Batas yang digunakan adalah yang paling kecil
            # antara limit kamar dan limit tahunan.
            # ---------------------------------------------

            limit_efektif = min(
                limit_kamar,
                limit_tahunan
            )

            # ---------------------------------------------
            # CEK STATUS
            # ---------------------------------------------

            if diajukan <= limit_efektif:

                hasil = "APPROVED"

            elif diajukan <= (
                limit_efektif * 1.10
            ):

                hasil = "CONSIDERED"

            else:

                hasil = "REJECTED"

        # =================================================
        # RAWAT JALAN
        # =================================================

        else:

            # Untuk RJ hanya menggunakan limit RJ

            limit_tahunan = data_plan[
                "limit_tahunan"
            ]

            limit_efektif = limit_tahunan

            if diajukan <= limit_efektif:

                hasil = "APPROVED"

            elif diajukan <= (
                limit_efektif * 1.10
            ):

                hasil = "CONSIDERED"

            else:

                hasil = "REJECTED"

        # =================================================
        # HASIL ANALISIS
        # =================================================

        st.markdown("---")

        st.markdown("### 📊 Hasil Analisis")

        # =================================================
        # APPROVED
        # =================================================

        if hasil == "APPROVED":

            st.success(
                "✅ KLAIM DISETUJUI\n\n"
                "Nominal klaim masih berada dalam "
                "batas manfaat plan."
            )

        # =================================================
        # CONSIDERED
        # =================================================

        elif hasil == "CONSIDERED":

            st.warning(
                "⚠️ KLAIM MEMERLUKAN PERTIMBANGAN\n\n"
                "Nominal klaim sedikit melebihi batas "
                "manfaat dan memerlukan review lebih lanjut."
            )

        # =================================================
        # REJECTED
        # =================================================

        else:

            st.error(
                "❌ KLAIM DITOLAK\n\n"
                "Nominal klaim melebihi batas manfaat "
                "secara signifikan."
            )

        # =================================================
        # DETAIL LIMIT
        # =================================================

        st.markdown("### 💰 Detail Limit")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Nominal Klaim",
                format_rupiah(diajukan)
            )

        with col2:

            st.metric(
                "Limit Efektif",
                format_rupiah(limit_efektif)
            )

        with col3:

            selisih = diajukan - limit_efektif

            if selisih > 0:

                st.metric(
                    "Melebihi Limit",
                    format_rupiah(selisih)
                )

            else:

                st.metric(
                    "Sisa Limit",
                    format_rupiah(
                        abs(selisih)
                    )
                )

        # =================================================
        # DETAIL RAWAT INAP
        # =================================================

        if tipe == "RI":

            st.markdown(
                "### 🛏️ Detail Perhitungan Rawat Inap"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Durasi",
                    f"{durasi} Hari"
                )

            with col2:

                st.metric(
                    "Kamar / Hari",
                    format_rupiah(
                        data_plan["per_hari"]
                    )
                )

            with col3:

                st.metric(
                    "Limit Berdasarkan Durasi",
                    format_rupiah(
                        limit_kamar
                    )
                )

            # ---------------------------------------------
            # INFORMASI LIMIT TAHUNAN
            # ---------------------------------------------

            st.info(
                f"""
                **Perhitungan Limit**

                Limit kamar:
                {format_rupiah(data_plan["per_hari"])}
                × {durasi} hari
                =
                **{format_rupiah(limit_kamar)}**

                Limit tahunan:
                **{format_rupiah(limit_tahunan)}**

                Limit yang digunakan:
                **{format_rupiah(limit_efektif)}**
                """
            )

            # ---------------------------------------------
            # PERINGATAN LIMIT TAHUNAN
            # ---------------------------------------------

            if limit_kamar > limit_tahunan:

                st.warning(
                    "⚠️ Perhitungan berdasarkan durasi "
                    "melebihi limit tahunan plan. "
                    "Karena itu limit tahunan digunakan "
                    "sebagai batas maksimal."
                )

        # =================================================
        # DETAIL RAWAT JALAN
        # =================================================

        else:

            st.markdown(
                "### 🚶 Detail Rawat Jalan"
            )

            st.info(
                f"""
                Limit Rawat Jalan:

                **{format_rupiah(limit_tahunan)}**
                """
            )

        # =================================================
        # RINGKASAN ANALISIS
        # =================================================

        st.markdown("---")

        st.markdown("### 📋 Ringkasan Analisis")

        st.write(
            f"**Plan:** {nama_plan}"
        )

        if tipe == "RI":

            st.write(
                "**Jenis Perawatan:** Rawat Inap"
            )

            st.write(
                f"**Durasi Rawat Inap:** "
                f"{durasi} Hari"
            )

            st.write(
                f"**Kamar / Hari:** "
                f"{format_rupiah(data_plan['per_hari'])}"
            )

            st.write(
                f"**Limit Berdasarkan Durasi:** "
                f"{format_rupiah(limit_kamar)}"
            )

            st.write(
                f"**Limit Tahunan:** "
                f"{format_rupiah(limit_tahunan)}"
            )

        else:

            st.write(
                "**Jenis Perawatan:** Rawat Jalan"
            )

            st.write(
                f"**Limit Rawat Jalan:** "
                f"{format_rupiah(limit_tahunan)}"
            )

        st.write(
            f"**Nominal Klaim:** "
            f"{format_rupiah(diajukan)}"
        )

        st.write(
            f"**Limit Efektif:** "
            f"{format_rupiah(limit_efektif)}"
        )

        st.write(
            f"**Status Rekomendasi:** "
            f"**{hasil}**"
        )