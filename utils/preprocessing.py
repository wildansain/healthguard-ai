import pandas as pd

def preprocess_data(df_input):
    df = df_input.copy()

    df.columns = df.columns.str.lower().str.strip()

    if "diajukan" in df.columns:
        df = df.dropna(subset=["diajukan"])

    for col in ["diajukan", "disetujui"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[^\d]", "", regex=True)
            )
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    if (
        "tanggal berobat" in df.columns and
        "tanggal selesai berobat" in df.columns
    ):
        df["tanggal berobat"] = pd.to_datetime(
            df["tanggal berobat"],
            errors="coerce"
        )

        df["tanggal selesai berobat"] = pd.to_datetime(
            df["tanggal selesai berobat"],
            errors="coerce"
        )

        df["durasi_hari"] = (
            df["tanggal selesai berobat"]
            - df["tanggal berobat"]
        ).dt.days.fillna(1)

        df["tahun"] = df["tanggal berobat"].dt.year

    return df