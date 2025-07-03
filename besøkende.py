import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Salmon Visitor Info", layout="centered")

lang = st.selectbox("Choose Language / Velg språk", ["English", "Norsk"])

countries = sorted([country.name for country in pycountry.countries])

translations = {
    "English": {
        "title": "🧭 Welcome to The Salmon Knowledge Centre in Oslo!",
        "subheader": "Please answer a few questions",
        "country": "Which country are you from?",
        "info_source": "How did you hear about us?",
        "info_options": ["Internet/Social Media", "Friend", "Tour Guide", "Other"],
        "gender": "What is your gender?",
        "gender_options": ["Male", "Female", "Non-binary", "Prefer not to say"],
        "age": "What is your age range?",
        "age_options": ["Under 18", "18–24", "25–34", "35–44", "45–54", "55–64", "65 or older"],
        "enjoyed": "Which part of this visit did you enjoy the most?",
        "enjoyed_options": ["Introduction video", "Guided tour", "The restaurant"],
        "satisfaction": "In overall, how satisfied were you with your museum visit?",
        "staff": "How would you rate the helpfulness and friendliness of our staff?",
        "cleanliness": "How satisfied were you with the cleanliness and the facilities (restrooms, seating, signage)?",
        "purchase_factors": "What is important for you when you buy the salmon? (You can choose multiple answers)",
        "purchase_options": ["Price", "Taste", "Nutrition", "Origin and sustainability", "Availability"],
        "association": "What do you most associate with Norwegian salmon? (You can choose multiple answers)",
        "association_options": ["Health and nutrition", "Export and production", "Environment and sustainability", "Nothing special"],
        "improvement": "What could we improve to enhance your museum experience? (Optional, max 100 words)",
        "submit": "Submit",
        "thanks": "✅ Thank you for your response!",
        "welcome": "### 🎉 Welcome to The Salmon Knowledge Centre!",
        "enjoy": "We’re excited to take you on a guided tour of this center. Enjoy your experience!",
        "refresh": "🔄 A new form will appear in 5 seconds..."
    },
    "Norsk": {
        "title": "🧭 Velkommen til The Salmon Kunnskapssenter i Oslo!",
        "subheader": "Vennligst svar på noen spørsmål",
        "country": "Hvilket land kommer du fra?",
        "info_source": "Hvordan hørte du om oss?",
        "info_options": ["Internett / sosiale medier", "Venn", "Reiseleder", "Annet"],
        "gender": "Hva er ditt kjønn?",
        "gender_options": ["Mann", "Kvinne", "Ikke-binær", "Foretrekker å ikke si"],
        "age": "Hva er din aldersgruppe?",
        "age_options": ["Under 18", "18–24", "25–34", "35–44", "45–54", "55–64", "65 år eller eldre"],
        "enjoyed": "Hvilken del av besøket likte du best?",
        "enjoyed_options": ["Introduksjonsvideo", "Guidet tur", "Restauranten"],
        "satisfaction": "Hvor fornøyd var du med museumsbesøket totalt sett?",
        "staff": "Hvordan vil du vurdere hjelpsomheten og vennligheten til våre ansatte?",
        "cleanliness": "Hvor fornøyd var du med renslighet og fasiliteter (toaletter, sitteplasser, skilt)?",
        "purchase_factors": "Hva er viktig for deg når du kjøper laks? (Du kan velge flere alternativer)",
        "purchase_options": ["Pris", "Smak", "Ernæring", "Opprinnelse og bærekraft", "Tilgjengelighet"],
        "association": "Hva forbinder du mest med norsk laks? (Du kan velge flere alternativer)",
        "association_options": ["Helse og ernæring", "Eksport og produksjon", "Miljø og bærekraft", "Ingenting spesielt"],
        "improvement": "Hva kan vi forbedre for å gjøre museumsopplevelsen bedre? (Valgfritt, maks 100 ord)",
        "submit": "Send inn",
        "thanks": "✅ Takk for ditt svar!",
        "welcome": "### 🎉 Velkommen til The Salmon Kunnskapssenter!",
        "enjoy": "Vi gleder oss til å ta deg med på en guidet tur i senteret. Nyt opplevelsen!",
        "refresh": "🔄 Et nytt skjema vises om 5 sekunder..."
    }
}

t = translations[lang]

st.title(t["title"])
st.subheader(t["subheader"])

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    with st.form("visitor_form"):
        country = st.selectbox(t["country"], countries)
        info_source = st.radio(t["info_source"], t["info_options"])
        gender = st.radio(t["gender"], t["gender_options"])
        age = st.radio(t["age"], t["age_options"])
        enjoyed = st.radio(t["enjoyed"], t["enjoyed_options"])
        satisfaction = st.radio(t["satisfaction"], ["1", "2", "3", "4", "5"])
        staff = st.radio(t["staff"], ["1", "2", "3", "4", "5"])
        cleanliness = st.radio(t["cleanliness"], ["1", "2", "3", "4", "5"])
        purchase_factors = st.multiselect(t["purchase_factors"], t["purchase_options"])
        association = st.multiselect(t["association"], t["association_options"])
        improvement = st.text_area(t["improvement"], max_chars=600)

        submit = st.form_submit_button(t["submit"])

        if submit:
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")

            response = {
                "date": date_str,
                "time": time_str,
                "lang": lang,
                "country": country,
                "info_source": info_source,
                "gender": gender,
                "age": age,
                "enjoyed": enjoyed,
                "satisfaction": satisfaction,
                "staff": staff,
                "cleanliness": cleanliness,
                "purchase_factors": ", ".join(purchase_factors),
                "association": ", ".join(association),
                "improvement": improvement
            }

            file_exists = os.path.isfile("visitor_data.csv")
            df = pd.DataFrame([response])
            df.to_csv("visitor_data.csv", mode='a', header=not file_exists, index=False)

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
