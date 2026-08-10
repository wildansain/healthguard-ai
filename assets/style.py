def load_css():
    return """
    <style>

    /* ===== GLOBAL ===== */

    .stApp {
        background: #0D1117;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    h1, h2, h3 {
        font-weight: 700;
        color: #F0F6FC;
    }

    p, label {
        color: #C9D1D9;
    }

    /* ===== SIDEBAR ===== */

    section[data-testid="stSidebar"] {
        background: #161B22;
        border-right: 1px solid #30363D;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: white;
    }

    /* ===== METRIC CARD ===== */

    div[data-testid="metric-container"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    /* ===== BUTTON ===== */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 45px;
        border: none;
        font-weight: 600;
        background: linear-gradient(
            135deg,
            #2563EB,
            #3B82F6
        );
        color: white;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        transition: 0.2s;
    }

    /* ===== FILE UPLOADER ===== */

    .stFileUploader {
        border: 2px dashed #2563EB;
        border-radius: 15px;
        padding: 10px;
        background: rgba(37,99,235,0.05);
    }

    /* ===== DATAFRAME ===== */

    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
    }

    /* ===== PLOTLY ===== */

    .js-plotly-plot .plotly {
        border-radius: 15px;
    }

    </style>
    """