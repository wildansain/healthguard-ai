import pandas as pd
import numpy as np
import io

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder


def detect_anomaly(df_raw):

    data = df_raw.copy()
    data.columns = data.columns.str.lower().str.strip()

    # =========================
    # CLEANING
    # =========================
    for kolom in ["diajukan", "disetujui"]:

        data[kolom] = (
            data[kolom]
            .astype(str)
            .str.replace(r"[^\d]", "", regex=True)
            .replace("", np.nan)
            .astype(float)
        )

    data = data.dropna(
        subset=["diajukan", "disetujui"]
    )

    data["tanggal berobat"] = pd.to_datetime(
        data["tanggal berobat"],
        errors="coerce"
    )

    data["tanggal selesai berobat"] = pd.to_datetime(
        data["tanggal selesai berobat"],
        errors="coerce"
    )

    data["durasi_hari"] = (
        data["tanggal selesai berobat"]
        - data["tanggal berobat"]
    ).dt.days

    # =========================
    # ENCODING
    # =========================
    encoders = {}

    for col in [
        "provinsi",
        "kota",
        "nama provider",
        "benefit",
        "plan id"
    ]:

        if col in data.columns:

            le = LabelEncoder()

            data[col] = le.fit_transform(
                data[col].astype(str)
            )

            encoders[col] = le

    # =========================
    # FEATURES
    # =========================
    fitur = [
        "provinsi",
        "kota",
        "nama provider",
        "benefit",
        "plan id",
        "durasi_hari",
        "diajukan"
    ]

    fitur = [
        f for f in fitur
        if f in data.columns
    ]

    X = data[fitur]

    X = pd.DataFrame(
        SimpleImputer(
            strategy="median"
        ).fit_transform(X),
        columns=X.columns
    )

    # =========================
    # MODEL
    # =========================
    iso = IsolationForest(
        contamination=0.03,
        random_state=42
    )

    data["anomali"] = iso.fit_predict(X)

    anomali_df = data[
        data["anomali"] == -1
    ].copy()

    # =========================
    # THRESHOLD BERDASARKAN DATA
    # =========================

    batas_diajukan = (
        data["diajukan"]
        .quantile(0.95)
    )

    rasio_persetujuan = (
        data["disetujui"]
        / data["diajukan"]
    )

    batas_rasio = (
        rasio_persetujuan
        .quantile(0.05)
    )

    batas_durasi = (
        data["durasi_hari"]
        .quantile(0.95)
    )

    def get_keterangan(row):

        alasan = []

        if row["diajukan"] >= batas_diajukan:
            alasan.append(
                "Nominal klaim sangat tinggi (Top 5%)"
            )

        if row["diajukan"] > 0:

            rasio = (
                row["disetujui"]
                / row["diajukan"]
            )

            if rasio <= batas_rasio:
                alasan.append(
                    "Rasio persetujuan sangat rendah (Bottom 5%)"
                )

        if (
            pd.notna(row["durasi_hari"])
            and row["durasi_hari"] >= batas_durasi
        ):
            alasan.append(
                "Durasi perawatan sangat tinggi (Top 5%)"
            )

        if not alasan:
            return "Pola tidak umum menurut Isolation Forest"

        return "; ".join(alasan)

    anomali_df["Keterangan"] = (
        anomali_df.apply(
            get_keterangan,
            axis=1
        )
    )

    # =========================
    # RISK LEVEL
    # =========================
    def get_risk(row):

        ket = row["Keterangan"]

        skor = 0

        if "Nominal" in ket:
            skor += 1

        if "Rasio" in ket:
            skor += 1

        if "Durasi" in ket:
            skor += 1

        if skor >= 2:
            return "🔴 HIGH RISK"

        return "🟡 MEDIUM RISK"

    anomali_df["Risk_Level"] = (
        anomali_df.apply(
            get_risk,
            axis=1
        )
    )

    anomali_df = anomali_df.sort_values(
        by="diajukan",
        ascending=False
    )

    for col, le in encoders.items():

        if col in anomali_df.columns:

            try:
                anomali_df[col] = (
                    le.inverse_transform(
                        anomali_df[col]
                        .astype(int)
                    )
                )
            except:
                pass

    return anomali_df

def export_anomaly_excel(anomali_df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        anomali_df.to_excel(
            writer,
            index=False
        )

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        format_red = workbook.add_format({
            "bg_color": "#FFC7CE"
        })

        worksheet.conditional_format(
            "A1:Z10000",
            {
                "type": "text",
                "criteria": "containing",
                "value": "HIGH",
                "format": format_red
            }
        )

    return output.getvalue()