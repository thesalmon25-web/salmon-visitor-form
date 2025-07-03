import streamlit as st
import pycountry
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Salmon Visitor Info", layout="centered")


lang = st.selectbox("Choose Language / Velg språk / Wählen Sie Sprache / Elegir idioma", ["English", "Norsk", "Deutsch", "Español"])


german_countries = ["Germany", "Austria", "Switzerland", "Liechtenstein", "Belgium", "Luxembourg"]
spanish_countries = [
    "Spain", "Mexico", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Nicaragua", "Panama",
    "Cuba", "Dominican Republic", "Puerto Rico", "Argentina", "Bolivia", "Chile", "Colombia", "Ecuador",
    "Paraguay", "Peru", "Uruguay", "Venezuela", "Equatorial Guinea"
]


countries = sorted([country.name for country in pycountry.countries])

if lang == "Deutsch":
    countries = german_countries
elif lang == "Español":
    countries = spanish_countries


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
    },
    "Deutsch": {
        "title": "🧭 Willkommen im Lachs-Wissenszentrum in Oslo!",
        "subheader": "Bitte beantworten Sie ein paar Fragen",
        "country": "Aus welchem Land kommen Sie?",
        "info_source": "Wie haben Sie vom Lachs erfahren?",
        "info_options": ["Freunde", "Internet", "Reisebüro", "Andere"],
        "group_size": "Wie viele Personen sind in Ihrer Gruppe?",
        "tasted_salmon": "Haben Sie schon einmal norwegischen Lachs probiert?",
        "can_buy": "Können Sie norwegischen Lachs in Ihrer Heimatstadt kaufen?",
        "first_time": "Ist dies Ihr erster Besuch in Norwegen?",
        "yes": "Ja",
        "no": "Nein",
        "submit": "Absenden",
        "thanks": "✅ Vielen Dank für Ihre Antwort!",
        "welcome": "### 🎉 Willkommen im Lachs-Wissenszentrum!",
        "enjoy": "Wir freuen uns, Ihnen eine Führung durch das Zentrum zu geben. Viel Spaß!",
        "refresh": "🔄 Ein neues Formular erscheint in 5 Sekunden..."
    },
    "Español": {
        "title": "🧭 ¡Bienvenido al Centro de Conocimiento del Salmón en Oslo!",
        "subheader": "Por favor responde algunas preguntas",
        "country": "¿De qué país vienes?",
        "info_source": "¿Cómo te enteraste del salmón?",
        "info_options": ["Amigos", "Internet", "Agencia de viajes", "Otro"],
        "group_size": "¿Cuántas personas hay en tu grupo?",
        "tasted_salmon": "¿Has probado el salmón noruego antes?",
        "can_buy": "¿Puedes comprar salmón noruego en tu ciudad?",
        "first_time": "¿Es esta tu primera visita a Noruega?",
        "yes": "Sí",
        "no": "No",
        "submit": "Enviar",
        "thanks": "✅ ¡Gracias por tu respuesta!",
        "welcome": "### 🎉 ¡Bienvenido al Centro de Conocimiento del Salmón!",
        "enjoy": "Estamos emocionados de llevarte en una visita guiada por este centro. ¡Disfruta tu experiencia!",
        "refresh": "🔄 Un nuevo formulario aparecerá en 5 segundos..."
    }
}


t = translations[lang]

st.title(t["title"])
st.subheader(t["subheader"])

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    with st.form("visitor_form"):
        if lang == "Norsk":
            farm_visited = st.radio(t["farm_visited"], [t["yes"], t["no"]])
            eat_regularly = st.radio(t["eat_regularly"], [t["yes"], t["no"]])
            association = st.radio(t["association"], t["association_options"])
            purchase_factor = st.radio(t["purchase_factor"], t["purchase_options"])
        else:
            country = st.selectbox(t["country"], countries)
            info_source = st.radio(t["info_source"], t["info_options"])
            group_size = st.number_input(t["group_size"], min_value=1, max_value=100)
            tasted_salmon = st.radio(t["tasted_salmon"], [t["yes"], t["no"]])
            can_buy = st.radio(t["can_buy"], [t["yes"], t["no"]])
            first_time = st.radio(t["first_time"], [t["yes"], t["no"]])

        submit = st.form_submit_button(t["submit"])

        if submit:
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")

            if lang == "Norsk":
                response = {
                    "Date": date_str,
                    "Time": time_str,
                    "Q1_FarmVisited": farm_visited,
                    "Q2_EatRegularly": eat_regularly,
                    "Q3_Association": association,
                    "Q4_PurchaseFactor": purchase_factor,
                    "Language": lang
                }
            else:
                response = {
                    "Date": date_str,
                    "Time": time_str,
                    "Q1_Country": country,
                    "Q2_InfoSource": info_source,
                    "Q3_GroupSize": group_size,
                    "Q4_TastedSalmon": tasted_salmon,
                    "Q5_CanBuy": can_buy,
                    "Q6_FirstTime": first_time,
                    "Language": lang
                }

            df = pd.DataFrame([response])
            file_exists = os.path.isfile("visitor_data.csv")
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