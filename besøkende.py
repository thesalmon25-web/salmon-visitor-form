import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime

countries = sorted([country.name for country in pycountry.countries])

st.set_page_config(page_title="Salmon Visitor Info", layout="centered")

st.title("🧭 Welcome to The Salmon Knowledge Centre in Oslo!")

st.subheader("Please answer a few questions")

with st.form("visitor_form"):
    country = st.selectbox("Which country are you from?", countries)
    info_source = st.radio("How did you hear about the Salmon?", ["Friends", "Internet", "Tour agency", "Other"])
    group_size = st.number_input("How many people are in your group?", min_value=1, max_value=100)
    tasted_salmon = st.radio("Did you taste Norwegian salmon before?", ["Yes", "No"])
    can_buy = st.radio("Can you buy Norwegian salmon in your hometown?", ["Yes", "No"])
    first_time = st.radio("Is this your first visit to Norway?", ["Yes", "No"])

    submit = st.form_submit_button("Submit")

if submit:
    st.success("✅ Thank you for your response!")
    st.markdown("### 🎉 Welcome to The Salmon Knowledge Centre!")
    st.markdown("We’re excited to take you on a guided tour of this center. Enjoy your experience!")

    # Save response to a CSV file (or connect to Google Sheets)
    response = {
        "timestamp": datetime.now().isoformat(),
        "country": country,
        "info_source": info_source,
        "group_size": group_size,
        "tasted_salmon": tasted_salmon,
        "can_buy": can_buy,
        "first_time": first_time,
    }
    df = pd.DataFrame([response])
    df.to_csv("visitor_data.csv", mode='a', header=False, index=False)
