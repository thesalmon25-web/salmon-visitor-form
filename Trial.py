import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime
import os
from PIL import Image
import base64
import requests


st.set_page_config(page_title="Salmon Visitor Info", layout="centered")

# Logo handling
logo_path = "logo.png"

def get_base64_logo(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

try:
    logo = Image.open(logo_path)
except:
    logo = None

logo_base64 = get_base64_logo(logo_path)

# Country list
countries = sorted([country.name for country in pycountry.countries])

# Translations
translations = {
    "English": {
        "title": "🧭 Welcome to The Salmon Knowledge Centre in Oslo!",
        "subheader": "Please answer a few questions",
        "country": "1. Which country are you from?",
        "info_source": "2. How did you hear about us?",
        "info_options": ["Internet/Social Media", "Friend", "Tour Guide", "Other"],
        "gender": "3. What is your gender?",
        "gender_options": ["Male", "Female", "Non-binary", "Prefer not to say"],
        "age": "4. What is your age range?",
        "age_options": ["Under 18", "18–24", "25–34", "35–44", "45–54", "55–64", "65 or older"],
        "enjoyed": "5. Which part of this visit did you enjoy the most?",
        "enjoyed_options": ["Introduction video", "Guided tour", "The restaurant"],
        "satisfaction": "6. Overall, how satisfied were you with your museum visit?",
        "staff": "7. How would you rate the helpfulness and friendliness of our staff?",
        "cleanliness": "8. How satisfied were you with the cleanliness and facilities?",
        "purchase_factors": "9. What is important when you buy salmon? (Choose multiple)",
        "purchase_options": ["Price", "Taste", "Nutrition", "Origin and sustainability", "Availability"],
        "association": "10. What do you associate with Norwegian salmon? (Choose multiple)",
        "association_options": ["Health and nutrition", "Export and production", "Environment and sustainability", "Nothing special"],
        "improvement": "11. How could we improve your museum experience?",
        "submit": "Submit",
        "thanks": "✅ Thank you for your response!",
        "welcome": "Thank you for visiting The Salmon Knowledge Centre!",
        "enjoy": "Have a good time ahead!",
        "refresh": "🔄 A new form will appear in 5 seconds..."
    },
    "Norsk": {
        "title": "🧭 Velkommen til The Salmon Kunnskapssenter i Oslo!",
        "subheader": "Vennligst svar på noen spørsmål",
        "country": "1. Hvilket land kommer du fra?",
        "info_source": "2. Hvordan hørte du om oss?",
        "info_options": ["Internett/sosiale medier", "Venn", "Reiseleder", "Annet"],
        "gender": "3. Hva er ditt kjønn?",
        "gender_options": ["Mann", "Kvinne", "Ikke-binær", "Foretrekker å ikke si"],
        "age": "4. Hva er din aldersgruppe?",
        "age_options": ["Under 18", "18–24", "25–34", "35–44", "45–54", "55–64", "65 år eller eldre"],
        "enjoyed": "5. Hvilken del av besøket likte du best?",
        "enjoyed_options": ["Introduksjonsvideo", "Guidet tur", "Restauranten"],
        "satisfaction": "6. Hvor fornøyd var du med museumsbesøket?",
        "staff": "7. Hvordan vil du vurdere våre ansattes hjelpsomhet?",
        "cleanliness": "8. Hvor fornøyd var du med renhold og fasiliteter?",
        "purchase_factors": "9. Hva er viktig når du kjøper laks? (Flere svar)",
        "purchase_options": ["Pris", "Smak", "Ernæring", "Opprinnelse og bærekraft", "Tilgjengelighet"],
        "association": "10. Hva forbinder du med norsk laks? (Flere svar)",
        "association_options": ["Helse og ernæring", "Eksport og produksjon", "Miljø og bærekraft", "Ingenting spesielt"],
        "improvement": "11. Hvordan kan vi forbedre museumsopplevelsen?",
        "submit": "Send inn",
        "thanks": "✅ Takk for ditt svar!",
        "welcome": "Takk for at du besøkte The Salmon Kunnskapssenter!",
        "enjoy": "Ha en god tid videre!",
        "refresh": "🔄 Et nytt skjema vises om 5 sekunder..."
    }
}

def submit_to_google_form(response, lang):
    if lang == "English":
        form_url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSdDL9fd4XMimQfY24hSk93Nbn7nPhdKmGmwFwJmehfEV_A01w/formResponse"
        field_map = {
            "country": "entry.873859373",
            "info_source": "entry.41075558",
            "gender": "entry.914717827",
            "age": "entry.1399763828",
            "enjoyed": "entry.2128747736",
            "satisfaction": "entry.9538383",
            "staff": "entry.663603190",
            "cleanliness": "entry.873529602",
            "purchase_factors": "entry.274987497",
            "association": "entry.11108432",
            "improvement": "entry.1731226948"
        }
    else:
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf3tu1dxqnLZyf4p-dFYBMbcNftwH5tLSPDMRKj-q6AYLaVTw/formResponse"
        field_map = {
            "country": "entry.1492465706",
            "info_source": "entry.732089430",
            "gender": "entry.828310117",
            "age": "entry.2138315189",
            "enjoyed": "entry.514293138",
            "satisfaction": "entry.344841686",
            "staff": "entry.2028615564",
            "cleanliness": "entry.511209905",
            "purchase_factors": "entry.561301552",
            "association": "entry.913843733",
            "improvement": "entry.1038394107"
        }

    payload = {
        field_map["country"]: response["country"],
        field_map["info_source"]: response["info_source"],
        field_map["gender"]: response["gender"],
        field_map["age"]: response["age"],
        field_map["enjoyed"]: response["enjoyed"],
        field_map["satisfaction"]: response["satisfaction"],
        field_map["staff"]: response["staff"],
        field_map["cleanliness"]: response["cleanliness"],
        field_map["improvement"]: response["improvement"]
    }

    for val in response["purchase_factors"]:
        payload[field_map["purchase_factors"]] = payload.get(field_map["purchase_factors"], []) + [val]
    for val in response["association"]:
        payload[field_map["association"]] = payload.get(field_map["association"], []) + [val]

    data = []
    for key, value in payload.items():
        if isinstance(value, list):
            for v in value:
                data.append((key, v))
        else:
            data.append((key, value))

    response_req = requests.post(form_url, data=data)
    return response_req.status_code == 200

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    lang = st.selectbox("Choose Language / Velg språk", ["English", "Norsk"])
    st.session_state.lang = lang
    t = translations[lang]

    st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <h1 style='flex: 1; color: #003366;'>{t['title']}</h1>
        <img src='data:image/png;base64,{logo_base64}' width='90' style='margin-left: 10px;'/>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='color: #0066cc; font-size: 20px;'>{t['subheader']}</div>", unsafe_allow_html=True)

    with st.form("visitor_form"):
        st.markdown(f'<div class="question">{t["country"]}</div>', unsafe_allow_html=True)
        country = st.selectbox("country_select", countries, label_visibility="collapsed")

        radio_qs = [("info_source", t["info_source"], t["info_options"]),
                    ("gender", t["gender"], t["gender_options"]),
                    ("age", t["age"], t["age_options"]),
                    ("enjoyed", t["enjoyed"], t["enjoyed_options"]),
                    ("satisfaction", t["satisfaction"], ["5", "4", "3", "2", "1"]),
                    ("staff", t["staff"], ["5", "4", "3", "2", "1"]),
                    ("cleanliness", t["cleanliness"], ["5", "4", "3", "2", "1"])]

        for q_id, q_text, q_options in radio_qs:
            st.markdown(f'<div class="question">{q_text}</div>', unsafe_allow_html=True)
            st.radio(f"{q_id}_radio", q_options, key=q_id, label_visibility="collapsed")

        checkbox_qs = [("purchase_factors", t["purchase_factors"], t["purchase_options"]),
                       ("association", t["association"], t["association_options"])]
        for q_id, q_text, q_options in checkbox_qs:
            st.markdown(f'<div class="question">{q_text}</div>', unsafe_allow_html=True)
            for option in q_options:
                st.checkbox(option, key=f"{q_id}_{option}")

        st.markdown(f'<div class="question">{t["improvement"]}</div>', unsafe_allow_html=True)
        improvement = st.text_area("improvement_text", label_visibility="collapsed", max_chars=600)

        submit = st.form_submit_button(t["submit"])

        if submit:
            response_data = {
                "country": country,
                "info_source": st.session_state.get("info_source"),
                "gender": st.session_state.get("gender"),
                "age": st.session_state.get("age"),
                "enjoyed": st.session_state.get("enjoyed"),
                "satisfaction": st.session_state.get("satisfaction"),
                "staff": st.session_state.get("staff"),
                "cleanliness": st.session_state.get("cleanliness"),
                "purchase_factors": [opt for opt in checkbox_qs[0][2] if st.session_state.get(f"purchase_factors_{opt}")],
                "association": [opt for opt in checkbox_qs[1][2] if st.session_state.get(f"association_{opt}")],
                "improvement": improvement
            }

            success = submit_to_google_form(response_data, lang)
            if success:
                st.session_state.form_submitted = True
                st.rerun()
            else:
                st.error("⚠️ Submission may have failed. Please try again.")

else:
    t = translations.get(st.session_state.get("lang", "English"), translations["English"])
    st.markdown(f"<div class='thanks-header'>{t['thanks']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='thanks-message'>{t['welcome']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='thanks-message'>{t['enjoy']}</div>", unsafe_allow_html=True)
    if logo_base64:
        st.markdown(f"<img src='data:image/png;base64,{logo_base64}' width='120'/>", unsafe_allow_html=True)
    st.markdown("""
        <meta http-equiv="refresh" content="5">
    """, unsafe_allow_html=True)

