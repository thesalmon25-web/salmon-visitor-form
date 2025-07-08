import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime
import os
from PIL import Image
import base64

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

# CSS for proper visibility
st.markdown(
    """
    <style>
    /* Base styling */
    .stApp, body {
        background-color: white !important;
        font-family: Arial, sans-serif;
    }
    
    /* Questions styling */
    .question {
        font-size: 20px !important;
        color: #003366 !important;
        font-weight: 600 !important;
        margin: 15px 0 8px 0 !important;
    }
    
    /* Answers styling */
    .stRadio [role="radiogroup"], 
    .stCheckbox [role="group"],
    .stSelectbox [data-baseweb="select"],
    .stTextArea textarea {
        font-size: 18px !important;
        color: #0066cc !important;
    }
    
    /* Input fields */
    [data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid #0066cc !important;
    }
    
    /* Submit button */
    .stButton > button {
        background-color: #0066cc !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 10px 24px !important;
        margin: 25px 0 !important;
    }
    
    /* Thank you page */
    .thanks-header {
        color: #003366 !important;
        font-size: 28px !important;
    }
    .thanks-message {
        color: #0066cc !important;
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    lang = st.selectbox("Choose Language / Velg språk", ["English", "Norsk"])
    t = translations[lang]

    st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <h1 style='flex: 1; color: #003366;'>{t['title']}</h1>
        <img src='data:image/png;base64,{logo_base64}' width='90' style='margin-left: 10px;'/>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='color: #0066cc; font-size: 20px;'>{t['subheader']}</div>", unsafe_allow_html=True)

    with st.form("visitor_form"):
        # Question 1 - Country dropdown
        st.markdown(f'<div class="question">{t["country"]}</div>', unsafe_allow_html=True)
        country = st.selectbox("country_select", countries, label_visibility="collapsed")
        
        # Questions 2-8 - Single choice radio buttons
        questions_radio = [
            ("info_source", t["info_source"], t["info_options"]),
            ("gender", t["gender"], t["gender_options"]),
            ("age", t["age"], t["age_options"]),
            ("enjoyed", t["enjoyed"], t["enjoyed_options"]),
            ("satisfaction", t["satisfaction"], ["5 - Very satisfied", "4", "3", "2", "1 - Very dissatisfied"]),
            ("staff", t["staff"], ["5 - Excellent", "4", "3", "2", "1 - Poor"]),
            ("cleanliness", t["cleanliness"], ["5 - Very clean", "4", "3", "2", "1 - Not clean"])
        ]
        
        for q_id, q_text, q_options in questions_radio:
            st.markdown(f'<div class="question">{q_text}</div>', unsafe_allow_html=True)
            st.radio(f"{q_id}_radio", q_options, key=q_id, label_visibility="collapsed")
        
        # Questions 9-10 - Multiple choice checkboxes
        questions_checkbox = [
            ("purchase_factors", t["purchase_factors"], t["purchase_options"]),
            ("association", t["association"], t["association_options"])
        ]
        
        for q_id, q_text, q_options in questions_checkbox:
            st.markdown(f'<div class="question">{q_text}</div>', unsafe_allow_html=True)
            for option in q_options:
                st.checkbox(option, key=f"{q_id}_{option}")
        
        # Question 11 - Text input
        st.markdown(f'<div class="question">{t["improvement"]}</div>', unsafe_allow_html=True)
        improvement = st.text_area("improvement_text", label_visibility="collapsed", max_chars=600)
        
        submit = st.form_submit_button(t["submit"])

        if submit:
            # Prepare response data
            response = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "language": lang,
                "country": country,
            }
            
            # Add radio button responses
            for q_id, _, _ in questions_radio:
                response[q_id] = st.session_state.get(q_id)
            
            # Add checkbox responses
            for q_id, _, q_options in questions_checkbox:
                selected = [opt for opt in q_options if st.session_state.get(f"{q_id}_{opt}")]
                response[q_id] = ", ".join(selected) if selected else "None"
            
            # Add text response
            response["improvement"] = improvement
            
            # Save to CSV
            file_exists = os.path.isfile("visitor_data.csv")
            df = pd.DataFrame([response])
            df.to_csv("visitor_data.csv", mode='a', header=not file_exists, index=False)
            
            st.session_state.form_submitted = True
            st.rerun()
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