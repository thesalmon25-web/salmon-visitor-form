import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Salmon Visitor Info", layout="centered")

# Get list of countries
countries = sorted([country.name for country in pycountry.countries])

# Title and subtitle
st.title("🧭 Welcome to The Salmon Knowledge Centre in Oslo!")
st.subheader("Please answer a few questions")

# Initialize session state
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

# Show form if not submitted
if not st.session_state.form_submitted:
    with st.form("visitor_form"):
        country = st.selectbox("Which country are you from?", countries)
        info_source = st.radio("How did you hear about the Salmon?", ["Friends", "Internet", "Tour agency", "Other"])
        group_size = st.number_input("How many people are in your group?", min_value=1, max_value=100)
        tasted_salmon = st.radio("Did you taste Norwegian salmon before?", ["Yes", "No"])
        can_buy = st.radio("Can you buy Norwegian salmon in your hometown?", ["Yes", "No"])
        first_time = st.radio("Is this your first visit to Norway?", ["Yes", "No"])

        submit = st.form_submit_button("Submit")

        if submit:
            # Save the form data
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

            st.session_state.form_submitted = True
            st.rerun()

# Show thank you message
if st.session_state.form_submitted:
    st.success("✅ Thank you for your response!")
    st.markdown("### 🎉 Welcome to The Salmon Knowledge Centre!")
    st.markdown("We’re excited to take you on a guided tour of this center. Enjoy your experience!")

    # Countdown message
    st.info("🔄 A new form will appear in 5 seconds...")

    # Use Streamlit's built-in JS to rerun by triggering a click on a hidden Streamlit button
    st.markdown("""
        <meta http-equiv="refresh" content="5">
    """, unsafe_allow_html=True)

