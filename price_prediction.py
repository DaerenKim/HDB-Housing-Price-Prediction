import streamlit as st
import pandas as pd
import numpy as np
import catboost as cb
from sklearn.preprocessing import StandardScaler

# Load saved model
cat_model = cb.CatBoostRegressor()
cat_model.load_model("Model/catboost_hdb_model.cbm")

# Page configuration
st.set_page_config(page_title="HDB Price Predictor", page_icon="🏠", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #155724;'>🏠 HDB Price Predictor</h1>", unsafe_allow_html=True)
st.write("---")  

# Sidebar Inputs
st.sidebar.header("Enter Property Details")
town = st.sidebar.selectbox("Town", ["Ang Mo Kio", "Bedok", "Bishan", "Bukit Merah", "Bukit Timah",
"Central Area", "Choa Chu Kang", "Clementi", "Geylang", "Hougang",
"Jurong East", "Jurong West", "Kallang/Whampoa", "Marine Parade",
"Pasir Ris", "Punggol", "Queenstown", "Sembawang", "Sengkang",
"Serangoon", "Tampines", "Toa Payoh", "Woodlands", "Yishun"])
flat_type = st.sidebar.selectbox("Flat Type", ["1 Room", "2 Room", "3 Room", "4 Room", "5 Room", "Executive", "Multi-Generation"])
storey_range = st.sidebar.selectbox("Storey Range", ["01 To 03", "04 To 06", "07 To 09", "10 To 12",
"13 To 15", "16 To 18", "19 To 21", "22 To 24",
"25 To 27", "28 To 30", "31 To 33", "34 To 36",
"37 To 39", "40 To 42", "43 To 45", "46 To 48",
"49 To 51"])
year = st.sidebar.number_input("Year Purchased", min_value=1990, max_value=2030, value=2025)
floor_area_sqm = st.sidebar.number_input("Floor Area (sqm)", min_value=0, max_value=400, value=50)
lease_commence_date = st.sidebar.number_input("Lease Commence Year", min_value=1960, max_value=2030, value=2000)

# Prepare input DataFrame
input_df = pd.DataFrame({
    'year': [year],
    'floor_area_sqm': [floor_area_sqm],
    'lease_commence_date': [lease_commence_date],
    'flat_type': [flat_type],
    'town': [town],
    'storey_range': [storey_range]
})

# Scale numeric features 
numeric_features = ['year', 'floor_area_sqm', 'lease_commence_date']
scaler = StandardScaler()
input_df[numeric_features] = scaler.fit_transform(input_df[numeric_features])

# Convert categorical columns to string
cat_features = ['flat_type', 'town', 'storey_range']
for col in cat_features:
    input_df[col] = input_df[col].astype(str)

# Predict Button
if st.button("Predict Price", help="Click to predict HDB price based on inputs"):
    prediction = cat_model.predict(input_df)[0]
    margin = 26101.58777084649
    upper = int(prediction + margin)
    lower = int(prediction - margin)

    st.markdown(
        f"""
        <div style="
            text-align: center;
            background: linear-gradient(135deg, #d4edda, #a8e6a2);
            color: #155724;             
            border: 2px solid #c3e6cb;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0px;
            box-shadow: 3px 3px 15px rgba(0,0,0,0.1);
        ">
            <h2 style="margin: 0;">🏠 Predicted HDB Price</h2>
            <p style="font-size:28px; margin: 15px 0 0 0;">
                Approximately between <strong>${lower:,.0f}</strong> to <strong>${upper:,.0f}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
