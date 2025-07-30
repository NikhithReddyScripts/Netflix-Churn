import streamlit as st
import requests
import numpy as np

# Render API URL (your deployed FastAPI URL)
API_URL = "https://churn-backend.onrender.com/predict"

st.title("📊 Netflix Churn Predictor (PCA-based)")

st.write("Enter 27 PCA-transformed features below:")

# Create 27 input fields
inputs = []
for i in range(27):
    value = st.number_input(f"Feature {i+1}", key=f"feature_{i}")
    inputs.append(value)

if st.button("Predict"):
    payload = {"features": inputs}
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.success(f"🎯 Prediction: {'Churn' if result['prediction'] else 'Not Churn'}")
        st.info(f"📈 Probability of Churn: {result['churn_probability']*100:.2f}%")

    except Exception as e:
        st.error(f"❌ API Error: {e}")
