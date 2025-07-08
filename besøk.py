import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime
import os
from PIL import Image
import base64

st.set_page_config(page_title="Salmon Visitor Info", layout="centered")
# Improved CSS for visibility
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #003366;
        color: white;
    }
    /* General text styling */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: white !important;
    }
    /* Form labels */
    .stTextLabel, .stRadio > label, .stCheckbox > label, .stSelectbox > label, .stMultiSelect > label {
        color: white !important;
        font-weight: 500 !important;
    }
    /* Radio and checkbox options */
    .stRadio [role="radiogroup"] label span, 
    .stCheckbox [role="checkbox"] label span,
    .stSelectbox [role="combobox"] {
        color: white !important;
    }
    /* Selected items */
    [data-baseweb="select"] [aria-selected="true"] {
        color: black !important;
    }
    /* Dropdown options */
    [role="listbox"] li {
        color: black !important;
    }
    /* Text input */
    .stTextInput input, .stTextArea textarea {
        color: black !important;
        background-color: white !important;
    }
    img {
        border: 2px solid white;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)
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
        "welcome": "Thank you for visiting The Salmon Knowledge Centre!",
        "enjoy": "Have a good time ahead!",
        "refresh": "🔄 A new form will appear in 5 seconds..."
    },
    "Norsk": {
        "title": "🧭Velkommen til The Salmon Kunnskapssenter i Oslo!",
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
        "welcome": "Takk for at du besøkte The Salmon Kunnskapssenter!",
        "enjoy": "Ha en god tid videre!",
        "refresh": "🔄 Et nytt skjema vises om 5 sekunder..."
    }
}

# (The rest of the logic remains the same from the original code)
# You can paste it here again or let me know if you want it inserted too.


if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    lang = st.selectbox("Choose Language / Velg språk", ["English", "Norsk"])
    st.session_state.lang = lang
    t = translations[lang]

    st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <h1 style='flex: 1;'>{t['title']}</h1>
        <img src='data:image/png;base64,{logo_base64}' width='90' style='margin-left: 10px;'/>
    </div>
    """, unsafe_allow_html=True)

    st.subheader(t["subheader"])

    with st.form("visitor_form"):
        country = st.selectbox(t["country"], countries)
        info_source = st.radio(t["info_source"], t["info_options"], key="info", index=None)
        gender = st.radio(t["gender"], t["gender_options"], key="gender", index=None)
        age = st.radio(t["age"], t["age_options"], key="age", index=None)
        enjoyed = st.radio(t["enjoyed"], t["enjoyed_options"], key="enjoyed", index=None)

        satisfaction = st.radio(t["satisfaction"], ["5", "4", "3", "2", "1"], horizontal=True, key="satisfaction", index=None)
        staff = st.radio(t["staff"], ["5", "4", "3", "2", "1"], horizontal=True, key="staff", index=None)
        cleanliness = st.radio(t["cleanliness"], ["5", "4", "3", "2", "1"], horizontal=True, key="cleanliness", index=None)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**{t['purchase_factors']}**")
        purchase_factors = [option for option in t["purchase_options"] if st.checkbox(option, key=f"purchase_{option}")]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**{t['association']}**")
        association = [option for option in t["association_options"] if st.checkbox(option, key=f"assoc_{option}")]

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
else:
    t = translations.get(st.session_state.get("lang", "English"), translations["English"])
    st.markdown(f"# {t['thanks']}")
    st.markdown(f"### {t['welcome']}")
    st.markdown(f"### {t['enjoy']}")
    if logo_base64:
        st.markdown(f"<img src='data:image/png;base64,{logo_base64}' width='120'/>", unsafe_allow_html=True)
    st.markdown("""
        <meta http-equiv="refresh" content="5">
    """, unsafe_allow_html=True)
