import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Salmon Visitor Info", layout="centered")

lang = st.selectbox("Choose Language / Velg språk", ["English", "Norsk"])


translations = {
    "English": {
        "title": "🧭 Welcome to The Salmon Knowledge Centre in Oslo!",
        "subheader": "Please answer a few questions",
        "country": "Which country are you from?",
        "info_source": "How did you hear about the Salmon?",
        "info_options": ["Friends", "Internet", "Tour agency", "Other"],
        "group_size": "How many people are in your group?",
        "tasted_salmon": "Did you taste Norwegian salmon before?",
        "can_buy": "Can you buy Norwegian salmon in your hometown?",
        "first_time": "Is this your first visit to Norway?",
        "yes": "Yes",
        "no": "No",
        "submit": "Submit",
        "thanks": "✅ Thank you for your response!",
        "welcome": "### 🎉 Welcome to The Salmon Knowledge Centre!",
        "enjoy": "We’re excited to take you on a guided tour of this center. Enjoy your experience!",
        "refresh": "🔄 A new form will appear in 5 seconds..."
    },
    "Norsk": {
        "title": "🧭 Velkommen til The Salmon Kunnskapssenteret i Oslo!",
        "subheader": "Vennligst svar på noen spørsmål",
        "farm_visited": "Har du tidligere besøkt et lakseoppdrettsanlegg?",
        "eat_regularly": "Spiser du norsk laks regelmessig?",
        "association": "Hva forbinder du mest med norsk laks?",
        "association_options": [
            "Helse og ernæring",
            "Norsk eksport og næring",
            "Miljø og bærekraft",
            "Ingen spesielle assosiasjoner"
        ],
        "purchase_factor": "Hva er viktigst for deg når du kjøper sjømat?",
        "purchase_options": ["Pris", "Smak", "Opprinnelse og bærekraft", "Tilgjengelighet"],
        "yes": "Ja",
        "no": "Nei",
        "submit": "Send inn",
        "thanks": "✅ Takk for ditt svar!",
        "welcome": "### 🎉 Velkommen til Laksesenteret!",
        "enjoy": "Vi gleder oss til å ta deg med på en guidet tur i senteret. Nyt opplevelsen!",
        "refresh": "🔄 Et nytt skjema vises om 5 sekunder..."
    }
}


t = translations[lang]
countries = sorted([country.name for country in pycountry.countries])

st.title(t["title"])
st.subheader(t["subheader"])

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    with st.form("visitor_form"):
        if lang == "English":
            country = st.selectbox(t["country"], countries)
            info_source = st.radio(t["info_source"], t["info_options"])
            group_size = st.number_input(t["group_size"], min_value=1, max_value=100)
            tasted_salmon = st.radio(t["tasted_salmon"], [t["yes"], t["no"]])
            can_buy = st.radio(t["can_buy"], [t["yes"], t["no"]])
            first_time = st.radio(t["first_time"], [t["yes"], t["no"]])
        else:
            farm_visited = st.radio(t["farm_visited"], [t["yes"], t["no"]])
            eat_regularly = st.radio(t["eat_regularly"], [t["yes"], t["no"]])
            association = st.radio(t["association"], t["association_options"])
            purchase_factor = st.radio(t["purchase_factor"], t["purchase_options"])

        submit = st.form_submit_button(t["submit"])

        if submit:
            if lang == "English":
                response = {
                    "timestamp": datetime.now().isoformat(),
                    "country": country,
                    "info_source": info_source,
                    "group_size": group_size,
                    "tasted_salmon": tasted_salmon,
                    "can_buy": can_buy,
                    "first_time": first_time,
                    "language": lang
                }
            else:
                response = {
                    "timestamp": datetime.now().isoformat(),
                    "farm_visited": farm_visited,
                    "eat_regularly": eat_regularly,
                    "association": association,
                    "purchase_factor": purchase_factor,
                    "language": lang
                }
            df = pd.DataFrame([response])
            df.to_csv("visitor_data.csv", mode='a', header=False, index=False)

            st.session_state.form_submitted = True
            st.rerun()

if st.session_state.form_submitted:
    st.success(t["thanks"])
    st.markdown(t["welcome"])
    st.markdown(t["enjoy"])

    st.info(t["refresh"])

    st.markdown("""
        <meta http-equiv="refresh" content="5">
    """, unsafe_allow_html=True)
