import streamlit as st
import requests
import numpy as np

# Backend API URL
API_URL = "https://netflix-churn.onrender.com/predict"

st.title("📊 Netflix Churn Predictor")

st.write("Paste **27 comma-separated PCA values** below:")

# Text input for PCA features
input_str = st.text_area("Enter PCA features (comma-separated)", height=150)

if st.button("Predict"):
    try:
        # Convert text input to list of floats
        features = [float(x.strip()) for x in input_str.split(",")]

        if len(features) != 27:
            st.error("❌ Please enter exactly 27 PCA values.")
        else:
            payload = {"features": features}
            response = requests.post(API_URL, json=payload)
            

            result = response.json()
            st.success(f"🎯 Prediction: {'Churn' if result['prediction'] else 'Not Churn'}")
            

    except ValueError:
        st.error("❌ Invalid input. Make sure all values are numbers separated by commas.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

