import joblib
import streamlit as st

@st.cache_resource
def load_model_resources():
    try:
        model = joblib.load("models/model_klaim.pkl")
        encoders = joblib.load("models/encoders_klaim.pkl")
        return model, encoders
    except:
        return None, None