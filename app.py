import streamlit as st

st.set_page_config(
    page_title="Hub - Sistema Welfare PA",
    page_icon="🇮🇹",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Source Sans 3', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #0d9488;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🇮🇹 Sistema Integrato Welfare PA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hub centralizzato per l\'erogazione e la gestione delle agevolazioni pubbliche</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### 👤 Portale Cittadino
    Area pubblica dedicata agli utenti. 
    
    Permette l'autenticazione tramite **SPID** o **CIE** e offre un motore di ricerca intelligente che incrocia i dati anagrafici e reddituali (ISEE) con i bandi attivi.
    """)

with col2:
    st.warning("""
    ### ⚙️ Portale Amministratore
    Area riservata (Back-office).
    
    Accesso protetto per il personale della PA. Permette di inserire nuovi bonus nel database centralizzato (SQLite/PDND) e gestire i requisiti di erogazione.
    """)

st.markdown("---")

st.success("👈 **Usa il menu laterale a sinistra per accedere alle due aree dell'applicazione.**")

st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.8rem; padding-top: 3rem;">
    Progetto Universitario 2026 · Simulazione Portale Servizi Pubblici<br>
    <em>Sviluppato secondo le linee guida AGID e i principi del GDPR</em>
</div>

""", unsafe_allow_html=True)
