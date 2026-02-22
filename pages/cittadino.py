import streamlit as st
import sqlite3
import pandas as pd
import time

# ==========================================
# CONFIGURAZIONE PAGINA
# ==========================================
st.set_page_config(
    page_title="Portale del Cittadino - Welfare PA",
    layout="wide",
    page_icon="🇮🇹",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');

    /* * FIX: Applico il font solo agli elementi di testo specifici 
     * ed escludo 'span' e 'div' generici per non rompere le icone di Streamlit 
     * (es. keyboard_arrow_right degli expander).
     */
    html, body, .stMarkdown, p, label, h1, h2, h3, h4, h5, h6, li, a {
        font-family: 'Source Sans 3', sans-serif !important;
    }

    /* ========================
       TESTI GLOBALI
    ======================== */
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
        font-family: 'Source Sans 3', sans-serif !important;
    }
    p, li { color: #cbd5e1; }
    .stMarkdown p, .stMarkdown li { color: #cbd5e1 !important; }

    /* ========================
       LOGIN HERO
    ======================== */
    .login-hero {
        background: linear-gradient(135deg, #0f2027 0%, #134e4a 50%, #0d9488 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 32px 32px;
        color: #e2e8f0;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .login-hero h1 {
        font-family: 'Lora', serif !important;
        font-size: 2.2rem !important;
        color: #ffffff !important;
        margin: 0.5rem 0 !important;
        letter-spacing: -0.02em;
    }
    .login-hero p { opacity: 0.85; font-size: 1.05rem; margin: 0; color: #e2e8f0; }
    .login-badge {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 0.3rem 1.2rem;
        font-size: 0.8rem;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    /* Card login — grigio navy */
    .login-top {
        background: #1e2d3d;
        border-radius: 16px 16px 0 0;
        padding: 2rem 2.5rem 1rem 2.5rem;
        border: 1px solid #2a4a5e;
        border-bottom: none;
    }
    .login-top .card-title {
        font-family: 'Lora', serif;
        font-size: 1.35rem;
        color: #e2e8f0;
        font-weight: 700;
        margin: 0 0 0.2rem 0;
    }
    .login-top .card-sub { color: #94a3b8; font-size: 0.88rem; margin: 0; }
    .login-bottom {
        background: #1e2d3d;
        border-radius: 0 0 16px 16px;
        padding: 0.5rem 2.5rem 2rem 2.5rem;
        border: 1px solid #2a4a5e;
        border-top: none;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }

    /* ========================
       NORMATIVA BOX
    ======================== */
    .normativa-box {
        background: #162533;
        border-left: 3px solid #0d9488;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 1rem;
        line-height: 1.7;
    }
    .normativa-box strong { color: #2dd4bf; }

    /* ========================
       TABS (SPID/CIE + categorie)
    ======================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #162533;
        padding: 4px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 8px 14px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: #1e3a4a !important;
        color: #2dd4bf !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    /* Label input */
    .stTextInput label, .stTextArea label, 
    .stSelectbox label, .stNumberInput label, 
    .stSlider label, .stCheckbox label, .stRadio label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ========================
       HEADER PRINCIPALE APP
    ======================== */
    .main-header {
        background: linear-gradient(135deg, #0f2027 0%, #134e4a 50%, #0d9488 100%);
        padding: 2rem 2.5rem;
        border-radius: 14px;
        color: #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 6px 24px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .main-header h1 {
        font-family: 'Lora', serif !important;
        font-size: 2rem !important;
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.2;
    }
    .main-header p {
        color: rgba(226,232,240,0.85) !important;
        margin: 0.4rem 0 0 0;
        font-size: 1.05rem;
    }

    /* ========================
       STEP INDICATOR
    ======================== */
    .step-bar {
        display: flex;
        align-items: center;
        margin: 1.5rem 0 2rem 0;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        color: #475569;
        font-weight: 500;
        white-space: nowrap;
    }
    .step.active { color: #2dd4bf; font-weight: 700; }
    .step.done    { color: #0d9488; font-weight: 600; }
    .step-num {
        width: 28px; height: 28px;
        border-radius: 50%;
        background: #1e2d3d;
        border: 2px solid #2a4a5e;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.78rem; font-weight: 700; color: #475569;
        flex-shrink: 0;
    }
    .step.active .step-num {
        background: #0d9488;
        border-color: #0d9488;
        color: white;
    }
    .step.done .step-num {
        background: #134e4a;
        border-color: #0d9488;
        color: #2dd4bf;
    }
    .step-line { flex: 1; height: 2px; background: #2a4a5e; margin: 0 0.6rem; }
    .step-line.done { background: #0d9488; }

    /* ========================
       BONUS CARD
    ======================== */
    .bonus-card {
        background: #1e2d3d;
        border: 1px solid #2a4a5e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        transition: border-color 0.2s;
    }
    .bonus-card:hover { border-color: #0d9488; }
    .bonus-card-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.8rem;
    }
    .bonus-title {
        font-family: 'Lora', serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0 0 0.2rem 0;
    }
    .bonus-ente { font-size: 0.85rem; color: #94a3b8; margin: 0; }
    .bonus-ente strong { color: #cbd5e1; }

    /* Badge regione */
    .badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        white-space: nowrap;
        flex-shrink: 0;
    }
    .badge-naz {
        background: rgba(13,148,136,0.18);
        color: #2dd4bf;
        border: 1px solid rgba(13,148,136,0.35);
    }
    .badge-reg {
        background: rgba(245,158,11,0.15);
        color: #fbbf24;
        border: 1px solid rgba(245,158,11,0.35);
    }

    /* Importo */
    .importo-box {
        background: linear-gradient(135deg, #162533, #1a3040);
        border: 1px solid #1e4a5e;
        border-left: 3px solid #0d9488;
        border-radius: 8px;
        padding: 0.65rem 1rem;
        margin: 0.8rem 0;
        font-weight: 700;
        color: #2dd4bf;
        font-size: 0.95rem;
    }

    .desc-text { color: #94a3b8; font-size: 0.93rem; line-height: 1.6; margin: 0.4rem 0; }

    a.link-bando {
        color: #2dd4bf;
        font-weight: 600;
        font-size: 0.88rem;
        text-decoration: none;
        border-bottom: 1px solid rgba(45,212,191,0.4);
    }
    a.link-bando:hover { border-bottom-color: #2dd4bf; }

    /* Stato documenti */
    .doc-ok {
        background: rgba(13,148,136,0.12);
        border: 1px solid rgba(13,148,136,0.3);
        border-radius: 8px;
        padding: 0.55rem 1rem;
        color: #2dd4bf;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    .doc-missing {
        background: rgba(245,158,11,0.1);
        border: 1px solid rgba(245,158,11,0.3);
        border-radius: 8px;
        padding: 0.55rem 1rem;
        color: #fbbf24;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }

    /* Risultati header */
    .risultati-header {
        background: linear-gradient(135deg, #134e4a, #1e3a4a);
        border: 1px solid #1e4a5e;
        border-left: 4px solid #0d9488;
        color: #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1.2rem 0;
        font-size: 1rem;
    }
    .risultati-header strong { color: #2dd4bf; }

    /* Nessun risultato */
    .no-risultati {
        text-align: center;
        padding: 3rem;
        color: #475569;
        background: #162533;
        border-radius: 12px;
        border: 1px dashed #2a4a5e;
    }
    .no-risultati strong { color: #94a3b8; }

    /* Section label */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #2dd4bf;
        margin-bottom: 0.5rem;
        display: block;
    }

    /* ========================
       SIDEBAR
    ======================== */
    section[data-testid="stSidebar"] { background: #1a2e3b !important; }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stSelectbox > div > div { color: #1a2e3b !important; }

    /* Chip utente sidebar */
    .user-chip {
        background: rgba(13,148,136,0.15);
        border: 1px solid rgba(13,148,136,0.3);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0 1rem 0;
    }
    .user-chip .name {
        font-weight: 700;
        font-size: 1rem;
        color: #e2e8f0;
    }
    .user-chip .method {
        display: inline-block;
        background: rgba(245,158,11,0.2);
        border: 1px solid rgba(245,158,11,0.45);
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin-top: 0.3rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: #fbbf24 !important;
    }

    /* ========================
       VARIE
    ======================== */
    hr { margin: 1.5rem 0; opacity: 0.15; border-color: #2a4a5e; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)


LISTA_REGIONI = [
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
    "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana",
    "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"
]

CATEGORIE = {
    "👨‍👩‍👧‍👦 Famiglia":   {"label": "Famiglia"},
    "🎓 Istruzione": {"label": "Istruzione"},
    "🏥 Salute":     {"label": "Salute"},
    "🏠 Casa":       {"label": "Casa"},
    "💼 Lavoro":     {"label": "Lavoro"},
    "🚌 Trasporti":  {"label": "Trasporti"},
}

SPID_PROVIDERS = [
    ("🟠", "PosteID",     "Poste Italiane"),
    ("🔵", "Aruba ID",    "Aruba S.p.A."),
    ("🟢", "InfoCert ID", "InfoCert S.p.A."),
    ("🔴", "SielteID",    "Sielte S.p.A."),
    ("🟣", "Namirial ID", "Namirial S.p.A."),
    ("⚫", "TIM ID",      "Telecom Italia"),
]



def get_db_connection():
    try:
        conn = sqlite3.connect('file:welfare.db?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError:
        return None

def check_regione(bonus_regione, utente_regione):
    if bonus_regione == "TUTTA ITALIA (Nazionale)":
        return True
    return bonus_regione == utente_regione

def badge_html(regione):
    if regione == "TUTTA ITALIA (Nazionale)":
        return '<span class="badge badge-naz">🇮🇹 NAZIONALE</span>'
    return f'<span class="badge badge-reg">📍 {regione.upper()}</span>'

def step_indicator(step_attivo):
    steps = [("1", "Profilo"), ("2", "Documenti"), ("3", "Risultati")]
    html = '<div class="step-bar">'
    for i, (num, label) in enumerate(steps):
        done    = (i + 1) < step_attivo
        active = (i + 1) == step_attivo
        css     = "step done" if done else ("step active" if active else "step")
        icon    = "✓" if done else num
        html   += f'<div class="{css}"><div class="step-num">{icon}</div>{label}</div>'
        if i < len(steps) - 1:
            html += f'<div class="step-line {"done" if done else ""}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ==========================================
# LOGIN PAGE
# ==========================================
def login_page():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none; }
        .main .block-container { max-width: 900px; padding-top: 0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-hero">
        <div class="login-badge">🏛️ Repubblica Italiana · Portale Pubblico</div>
        <h1>Portale Unico del Cittadino</h1>
        <p>Accedi in sicurezza per scoprire le agevolazioni a cui hai diritto</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-top">
        <div class="card-title">🔐 Accedi con Identità Digitale</div>
        <div class="card-sub">Scegli il metodo di accesso certificato</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: #1e2d3d;
        padding: 0 2.5rem;
        border-left: 1px solid #2a4a5e;
        border-right: 1px solid #2a4a5e;
    ">
    """, unsafe_allow_html=True)

    tab_spid, tab_cie = st.tabs(["🔵 SPID", "💳 CIE"])

    # ---- TAB SPID ----
    with tab_spid:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Seleziona il tuo Identity Provider SPID:**")

        provider_scelto = st.selectbox(
            "Provider",
            [f"{dot} {nome} — {desc}" for dot, nome, desc in SPID_PROVIDERS],
            label_visibility="collapsed"
        )
        provider_nome = provider_scelto.split(" — ")[0].strip()[2:].strip()

        col_u, col_p = st.columns(2)
        with col_u:
            username_spid = st.text_input("Nome Utente", placeholder="es. mario.rossi", key="spid_user")
        with col_p:
            password_spid = st.text_input("Password", type="password", key="spid_pass")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Entra con SPID", type="primary", use_container_width=True, key="btn_spid"):
            if not username_spid or not password_spid:
                st.error("⚠️ Inserisci nome utente e password per procedere.")
            else:
                with st.spinner(f"Autenticazione in corso con {provider_nome}..."):
                    time.sleep(1.8)
                _set_session("Mario Rossi", f"SPID L2 · {provider_nome}")

        st.markdown("""
        <div class="normativa-box">
            🔒 <strong>SPID</strong> è il Sistema Pubblico di Identità Digitale.<br>
            La tua password non viene trasmessa a questo portale.<br>
            L'autenticazione avviene direttamente sul server del tuo provider.
        </div>
        <br>
        """, unsafe_allow_html=True)

    # ---- TAB CIE ----
    with tab_cie:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💳 Usa la tua **Carta d'Identità Elettronica** (CIE 3.0) per accedere in modo sicuro tramite il chip NFC.")

        numero_cie = st.text_input(
            "Numero Carta d'Identità",
            placeholder="es. CA00000AA",
            max_chars=9,
            help="Il numero si trova sul retro della carta, in alto a destra"
        )

        col_m, col_g = st.columns(2)
        with col_m:
            pin_cie = st.text_input("PIN CIE (prime 4 cifre)", type="password", max_chars=4, key="cie_pin")
        with col_g:
            st.markdown("<div style='padding-top:1.8rem;'>", unsafe_allow_html=True)
            lettore = st.checkbox("Lettore NFC collegato")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔐 Entra con CIE", type="primary", use_container_width=True, key="btn_cie"):
            if not numero_cie or not pin_cie:
                st.error("⚠️ Inserisci numero carta e PIN per procedere.")
            elif len(pin_cie) < 4:
                st.error("⚠️ Il PIN deve essere di 4 cifre.")
            else:
                with st.spinner("Verifica certificato digitale CIE in corso..."):
                    time.sleep(2.0)
                _set_session("Mario Rossi", "CIE 3.0")

        st.markdown("""
        <div class="normativa-box">
            💳 <strong>CIE</strong> è la Carta d'Identità Elettronica italiana.<br>
            Il chip NFC contiene un certificato digitale riconosciuto a livello europeo (eIDAS).<br>
            Il PIN non viene mai trasmesso a questo portale.
        </div>
        <br>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="login-bottom"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:#475569; font-size:0.8rem; padding: 1.5rem 0 0.5rem 0;">
        Accesso conforme al <strong style="color:#94a3b8;">D.Lgs. 82/2005 (CAD)</strong>
        e al regolamento <strong style="color:#94a3b8;">eIDAS (UE 910/2014)</strong><br>
        Dati trattati in conformità al <strong style="color:#94a3b8;">GDPR – Reg. UE 2016/679</strong><br><br>
        Sistema Welfare PA · Progetto Universitario 2026 · Solo a scopo dimostrativo
    </div>
    """, unsafe_allow_html=True)


def _set_session(nome, metodo):
    st.session_state['authenticated'] = True
    st.session_state['user_name']     = nome
    st.session_state['auth_method']   = metodo
    st.rerun()


# ==========================================
# SIDEBAR AUTENTICATA
# ==========================================
def mostra_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
            <div style="font-size: 2.8rem;">🇮🇹</div>
            <div style="font-family:'Lora',serif; font-size:1.2rem; font-weight:700; margin-top:0.4rem; color:#e2e8f0;">
                Welfare PA
            </div>
            <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.2rem;">Portale del Cittadino</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"""
        <div class="user-chip">
            <div class="name">👤 {st.session_state['user_name']}</div>
            <div class="method">{st.session_state['auth_method']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Regione
        st.markdown('<span class="section-label" style="color:#94a3b8!important;">📍 Regione di residenza</span>', unsafe_allow_html=True)
        regione = st.selectbox("Regione", LISTA_REGIONI, index=8, label_visibility="collapsed")

        st.markdown("---")

        # funzionamento
        st.markdown("""
        <div style="color:#94a3b8; font-size:0.82rem; line-height:2;">
            <strong style="color:#e2e8f0;">📋 Come funziona</strong><br>
            ① Scegli la categoria<br>
            ② Inserisci i tuoi dati<br>
            ③ Carica i documenti<br>
            ④ Invia la domanda
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.button("🚪 Esci (Logout)", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        st.markdown('<div style="color:#475569; font-size:0.75rem; margin-top:1rem;">Sistema Welfare PA v2.0<br>Progetto Universitario 2026</div>', unsafe_allow_html=True)

    return regione


def _mostra_risultati_smart(trovati, check_docs_fn, key_prefix, icona):
    if not trovati:
        st.markdown("""
        <div class="no-risultati">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">🔍</div>
            <strong>Nessun bonus trovato</strong><br>
            <span style="font-size:0.9rem; color:#475569;">
                Prova a modificare i parametri di ricerca o verifica la regione selezionata.
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="risultati-header">
        {icona} Trovate <strong>{len(trovati)} opportunità</strong> compatibili con il tuo profilo
    </div>
    """, unsafe_allow_html=True)

    for b in trovati:
        missing = check_docs_fn(b)
        doc_ok  = len(missing) == 0

        nome        = b.get('nome', '—')
        ente        = b.get('ente', '—')
        descrizione = b.get('descrizione', '')
        importo     = b.get('importo', '—')
        link        = b.get('link', '')
        bid         = b.get('id', key_prefix)
        regione     = b.get('regione', '')

        link_html = f'<a class="link-bando" href="{link}" target="_blank">📎 Consulta il bando ufficiale →</a>' if link else ''

        st.markdown(f"""
        <div class="bonus-card">
            <div class="bonus-card-header">
                <div>
                    <p class="bonus-title">{nome}</p>
                    <p class="bonus-ente">Ente erogatore: <strong>{ente}</strong></p>
                </div>
                {badge_html(regione)}
            </div>
            <p class="desc-text">{descrizione or '<em>Nessuna descrizione disponibile.</em>'}</p>
            <div class="importo-box">💰 {importo}</div>
            {link_html}
        </div>
        """, unsafe_allow_html=True)

        if doc_ok:
            st.markdown('<div class="doc-ok">✅ Documenti completi — puoi inviare la domanda</div>', unsafe_allow_html=True)
            if st.button(f"🚀 Invia Domanda", key=f"btn_{bid}_{key_prefix}", type="primary", use_container_width=True):
                st.balloons()
                st.success(f"✅ Domanda per **{nome}** inviata con successo!")
        else:
            st.markdown(f'<div class="doc-missing">📄 Per richiedere carica: <strong>{", ".join(missing)}</strong></div>', unsafe_allow_html=True)
            st.button("Carica i documenti per richiedere", key=f"btn_dis_{bid}_{key_prefix}", disabled=True, use_container_width=True)

        st.markdown("---")


# ==========================================
# SEZIONI CATEGORIE
# ==========================================

def sezione_famiglia(conn, regione_utente):
    st.markdown('<span class="section-label">Passo 1 — I tuoi dati</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        isee = st.number_input("💶 ISEE (€)", 0, 100000, 15000, step=500)
    with col2:
        num_figli = st.number_input("👶 Figli a carico", 0, 10, 1)
    with col3:
        eta_figlio = st.number_input("🎂 Età figlio più giovane", 0, 25, 2) if num_figli > 0 else 0

    st.markdown('<span class="section-label" style="margin-top:1.5rem; display:block;">Passo 2 — Documenti (opzionale per cercare, obbligatorio per richiedere)</span>', unsafe_allow_html=True)
    with st.expander("📂 Area Documenti — clicca per espandere", expanded=False):
        st.info("Carica i documenti per abilitare l'invio della domanda. Puoi cercare anche senza.")
        doc_isee = st.file_uploader("📄 ISEE / DSU", type=['pdf', 'jpg', 'png'], key="doc_fam_isee")

    if st.button("🔍 Cerca Bonus Disponibili", type="primary", use_container_width=True, key="cerca_fam"):
        step_indicator(3)
        df = pd.read_sql_query("SELECT * FROM bonus_famiglia", conn)
        trovati = []
        for _, row in df.iterrows():
            b = row.to_dict()
            if not check_regione(b['regione'], regione_utente): continue
            if isee < b.get('isee_min', 0) or isee > b.get('max_isee', 99999999): continue
            if num_figli < b.get('min_figli', 0): continue
            if b.get('max_eta_figli', 0) > 0 and eta_figlio > b['max_eta_figli']: continue
            trovati.append(b)
        _mostra_risultati_smart(trovati, lambda b: [] if doc_isee else ["ISEE / DSU"], "fam", "👨‍👩‍👧‍👦")


def sezione_istruzione(conn, regione_utente):
    st.markdown('<span class="section-label">Passo 1 — I tuoi dati</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        livello    = st.selectbox("📚 Livello di istruzione", ["Scuola Primaria", "Scuola Secondaria I°", "Scuola Secondaria II°", "Università", "Master/Dottorato"])
        fuori_sede = st.checkbox("🏠 Studente fuori sede")
    with col2:
        isee = st.number_input("💶 ISEE (€)", 0, 100000, 20000, step=500)
    with col3:
        voto = st.slider("📊 Voto Maturità / Voto laurea", 60, 110, 80)

    st.markdown('<span class="section-label" style="margin-top:1.5rem; display:block;">Passo 2 — Documenti</span>', unsafe_allow_html=True)
    with st.expander("📂 Area Documenti", expanded=False):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            doc_isee = st.file_uploader("📄 ISEE", type=['pdf'], key="doc_istr_isee")
        with col_d2:
            doc_iscrizione = st.file_uploader("📄 Certificato iscrizione / Ricevuta tasse", type=['pdf'], key="doc_istr_iscr")
        doc_voto = st.file_uploader("🏆 Certificato voti (per borse merito ≥90)", type=['pdf'], key="doc_istr_voto") if voto >= 90 else None

    if st.button("🔍 Cerca Bonus Disponibili", type="primary", use_container_width=True, key="cerca_istr"):
        step_indicator(3)
        df = pd.read_sql_query("SELECT * FROM bonus_istruzione", conn)
        trovati = []
        for _, row in df.iterrows():
            b = row.to_dict()
            if not check_regione(b['regione'], regione_utente): continue
            if isee > b.get('max_isee', 99999999): continue
            ldb = b.get('livello_studio', 'Tutti i livelli')
            if ldb != 'Tutti i livelli' and ldb not in livello: continue
            if voto < b.get('voto_minimo', 0): continue
            if b.get('solo_fuori_sede') and not fuori_sede: continue
            trovati.append(b)

        def _check(b):
            m = []
            if b.get('max_isee', 99999999) < 99999999 and not doc_isee: m.append("ISEE")
            if "Università" in b.get('livello_studio', '') and not doc_iscrizione: m.append("Certificato iscrizione")
            if b.get('voto_minimo', 0) >= 90 and not doc_voto: m.append("Certificato voti")
            return m
        _mostra_risultati_smart(trovati, _check, "istr", "🎓")


def sezione_salute(conn, regione_utente):
    st.markdown('<span class="section-label">Passo 1 — I tuoi dati</span>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        eta  = st.number_input("🎂 Età", 0, 100, 35)
        isee = st.number_input("💶 ISEE (€)", 0, 100000, 15000, step=500)
    with col2:
        st.markdown("**Condizioni sanitarie richieste:**")
        st.caption("⚠️ *(SPUNTANDO UNA DELLE DUE CASELLE SEI OBBLIGATO AD INSERIRE UN CERTIFICATO CHE LO ATTESTA)*")
        patologia  = st.checkbox("🩺 Patologia cronica o rara certificata")
        invalidita = st.checkbox("♿ Invalidità civile (Legge 104/1992)")

    st.markdown('<span class="section-label" style="margin-top:1.5rem; display:block;">Passo 2 — Documenti</span>', unsafe_allow_html=True)
    with st.expander("📂 Area Documenti", expanded=False):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            doc_isee = st.file_uploader("📄 ISEE", type=['pdf'], key="doc_sal_isee")
        with col_d2:
            doc_medico  = st.file_uploader("📄 Certificato medico", type=['pdf'], key="doc_sal_pat") if patologia else None
            doc_verbale = st.file_uploader("📄 Verbale invalidità INPS", type=['pdf'], key="doc_sal_inv") if invalidita else None

    if st.button("🔍 Cerca Bonus Disponibili", type="primary", use_container_width=True, key="cerca_sal"):
        step_indicator(3)
        df = pd.read_sql_query("SELECT * FROM bonus_salute", conn)
        trovati = []
        for _, row in df.iterrows():
            b = row.to_dict()
            if not check_regione(b['regione'], regione_utente): continue
            if isee > b.get('max_isee', 99999999): continue
            if not (b.get('min_eta', 0) <= eta <= b.get('max_eta', 100)): continue
            if b.get('richiede_patologia') and not patologia: continue
            if b.get('richiede_invalidita') and not invalidita: continue
            trovati.append(b)

        def _check(b):
            m = []
            if b.get('max_isee', 99999999) < 99999999 and not doc_isee: m.append("ISEE")
            if b.get('richiede_patologia') and not doc_medico: m.append("Certificato medico")
            if b.get('richiede_invalidita') and not doc_verbale: m.append("Verbale invalidità INPS")
            return m
        _mostra_risultati_smart(trovati, _check, "sal", "🏥")


def sezione_casa(conn, regione_utente):
    st.markdown('<span class="section-label">Passo 1 — I tuoi dati</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        isee = st.number_input("💶 ISEE (€)", 0, 100000, 20000, step=500)
    with col2:
        eta  = st.number_input("🎂 Età", 18, 100, 30)
    with col3:
        tipo = st.selectbox("🏠 Tipo di richiesta", ["Affitto", "Acquisto Prima Casa", "Ristrutturazione", "Bollette/Utenze", "Efficienza Energetica"])

    label_doc = {
        "Affitto":              "Contratto d'affitto",
        "Acquisto Prima Casa":  "Rogito notarile / Compromesso",
        "Ristrutturazione":     "Preventivo / Fattura lavori",
        "Bollette/Utenze":      "Bolletta (luce/gas/acqua)",
        "Efficienza Energetica":"APE / Fattura impianti"
    }.get(tipo, "Documento specifico")

    st.markdown('<span class="section-label" style="margin-top:1.5rem; display:block;">Passo 2 — Documenti</span>', unsafe_allow_html=True)
    with st.expander("📂 Area Documenti", expanded=False):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            doc_isee = st.file_uploader("📄 ISEE", type=['pdf'], key="doc_casa_isee")
        with col_d2:
            doc_specifico = st.file_uploader(f"📄 {label_doc}", type=['pdf'], key="doc_casa_spec")

    if st.button("🔍 Cerca Bonus Disponibili", type="primary", use_container_width=True, key="cerca_casa"):
        step_indicator(3)
        df = pd.read_sql_query("SELECT * FROM bonus_casa", conn)
        trovati = []
        for _, row in df.iterrows():
            b = row.to_dict()
            if not check_regione(b['regione'], regione_utente): continue
            if isee > b.get('max_isee', 99999999): continue
            if not (b.get('min_eta', 0) <= eta <= b.get('max_eta', 100)): continue
            db_ambito = b.get('ambito', 'Tutti')
            if "Tutti" not in db_ambito:
                match = False
                if "Affitto" in tipo and "Affitto" in db_ambito: match = True
                elif "Acquisto" in tipo and "Acquisto" in db_ambito: match = True
                elif "Ristrutturaz" in tipo and "Ristrutturaz" in db_ambito: match = True
                elif "Bollette" in tipo and "Bollette" in db_ambito: match = True
                elif "Efficienza" in tipo and "Efficienza" in db_ambito: match = True
                if not match: continue
            trovati.append(b)

        def _check(b):
            m = []
            if b.get('max_isee', 99999999) < 99999999 and not doc_isee: m.append("ISEE")
            if "Tutti" not in b.get('ambito', 'Tutti') and not doc_specifico: m.append(label_doc)
            return m
        _mostra_risultati_smart(trovati, _check, "casa", "🏠")


def sezione_lavoro(conn, regione_utente):
    st.markdown('<span class="section-label">Passo 1 — I tuoi dati</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        stato  = st.selectbox("💼 Stato occupazionale", ["Disoccupato/Inoccupato", "Lavoratore Dipendente", "Partita IVA/Autonomo", "Studente/Tirocinante"])
        genere = st.radio("👤 Genere", ["Uomo", "Donna"], horizontal=True)
    with col2:
        isee = st.number_input("💶 ISEE (€)", 0, 100000, 15000, step=500)
    with col3:
        eta = st.number_input("🎂 Età", 18, 70, 28)

    label_lav = {
        "Disoccupato/Inoccupato":   "DID (Dichiarazione Disponibilità)",
        "Lavoratore Dipendente":    "Ultima busta paga",
        "Partita IVA/Autonomo":     "Visura camerale / Dichiarazione redditi",
        "Studente/Tirocinante":     "Contratto tirocinio / Certificato iscrizione"
    }.get(stato, "Documento occupazionale")

    st.markdown('<span class="section-label" style="margin-top:1.5rem; display:block;">Passo 2 — Documenti</span>', unsafe_allow_html=True)
    with st.expander("📂 Area Documenti", expanded=False):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            doc_isee = st.file_uploader("📄 ISEE", type=['pdf'], key="doc_lav_isee")
        with col_d2:
            doc_lavoro = st.file_uploader(f"📄 {label_lav}", type=['pdf'], key="doc_lav_spec")

    if st.button("🔍 Cerca Bonus Disponibili", type="primary", use_container_width=True, key="cerca_lav"):
        step_indicator(3)
        df = pd.read_sql_query("SELECT * FROM bonus_lavoro", conn)
        trovati = []
        for _, row in df.iterrows():
            b = row.to_dict()
            if not check_regione(b['regione'], regione_utente): continue
            if isee > b.get('max_isee', 99999999): continue
            if not (b.get('min_eta', 0) <= eta <= b.get('max_eta', 100)): continue
            if b.get('solo_donne') and genere == "Uomo": continue
            db_stato = b.get('stato_occupazionale', 'Tutti')
            if "Tutti" not in db_stato:
                match = False
                if "Disoccupati" in db_stato and "Disoccupato" in stato: match = True
                elif "Dipendenti" in db_stato and "Dipendente" in stato: match = True
                elif "Partite IVA" in db_stato and "Partita IVA" in stato: match = True
                elif "Studenti" in db_stato and "Studente" in stato: match = True
                if not match: continue
            trovati.append(b)

        def _check(b):
            m = []
            if b.get('max_isee', 99999999) < 99999999 and not doc_isee: m.append("ISEE")
            if "Tutti" not in b.get('stato_occupazionale', 'Tutti') and not doc_lavoro: m.append(label_lav)
            return m
        _mostra_risultati_smart(trovati, _check, "lav", "💼")


def sezione_trasporti(conn, regione_utente):
    st.markdown('<span class="section-label">Passo 1 — I tuoi dati</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo = st.selectbox("🚌 Tipo di agevolazione", ["Abbonamento TPL", "Bicicletta/Monopattino", "Carburante"])
    with col2:
        eta  = st.number_input("🎂 Età", 10, 100, 28)
    with col3:
        isee = st.number_input("💶 ISEE (€)", 0, 100000, 20000, step=500)

    st.markdown('<span class="section-label" style="margin-top:1.5rem; display:block;">Passo 2 — Documenti</span>', unsafe_allow_html=True)
    with st.expander("📂 Area Documenti", expanded=False):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            doc_isee = st.file_uploader("📄 ISEE", type=['pdf'], key="doc_tra_isee")
        with col_d2:
            doc_ricevuta = st.file_uploader("📄 Ricevuta / Fattura acquisto", type=['pdf'], key="doc_tra_fatt") if "Carburante" not in tipo else None

    if st.button("🔍 Cerca Bonus Disponibili", type="primary", use_container_width=True, key="cerca_tra"):
        step_indicator(3)
        try:
            df = pd.read_sql_query("SELECT * FROM bonus_generale WHERE categoria='TRASPORTI'", conn)
        except Exception:
            try:
                df = pd.read_sql_query("SELECT * FROM bonus_trasporti", conn)
            except:
                df = pd.DataFrame()

        trovati = []
        for _, row in df.iterrows():
            b = row.to_dict()
            if not check_regione(b['regione'], regione_utente): continue
            if isee > b.get('max_isee', 99999999): continue
            min_e = b.get('min_eta_cittadino', b.get('min_eta', 0))
            max_e = b.get('max_eta_cittadino', b.get('max_eta', 100))
            if not (min_e <= eta <= max_e): continue
            trovati.append(b)

        def _check(b):
            m = []
            if b.get('max_isee', 99999999) < 99999999 and not doc_isee: m.append("ISEE")
            if "Carburante" not in tipo and not doc_ricevuta: m.append("Ricevuta acquisto")
            return m
        _mostra_risultati_smart(trovati, _check, "tra", "🚌")


# ==========================================
# APP PRINCIPALE (post-login)
# ==========================================
def app_cittadino():
    regione_utente = mostra_sidebar()

    st.markdown("""
    <div class="main-header">
        <div style="font-size:3.2rem; line-height:1; flex-shrink:0;">🏛️</div>
        <div>
            <h1>Portale Unico del Cittadino</h1>
            <p>Scopri i bonus e le agevolazioni a cui hai diritto — in pochi minuti</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    step_indicator(1)

    st.markdown("### Di che tipo di supporto hai bisogno?")
    st.caption("Seleziona la categoria più adatta alla tua situazione.")

    categoria = st.radio("Categoria", list(CATEGORIE.keys()), horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    conn = get_db_connection()
    if conn is None:
        st.error("⚠️ **Database non disponibile.** Assicurati che `welfare.db` esista e che il pannello amministrativo sia stato avviato almeno una volta.")
        st.stop()

    step_indicator(2)

    label = CATEGORIE[categoria]["label"]
    if label == "Famiglia":     sezione_famiglia(conn, regione_utente)
    elif label == "Istruzione": sezione_istruzione(conn, regione_utente)
    elif label == "Salute":     sezione_salute(conn, regione_utente)
    elif label == "Casa":       sezione_casa(conn, regione_utente)
    elif label == "Lavoro":     sezione_lavoro(conn, regione_utente)
    elif label == "Trasporti":  sezione_trasporti(conn, regione_utente)

    conn.close()

    st.markdown("""
    <div style="text-align:center; color:#475569; font-size:0.8rem; padding: 3rem 0 0.5rem 0;">
        Sistema Welfare PA — Progetto Universitario 2026<br>
        Dati trattati in conformità con il GDPR – Reg. UE 2016/679
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# ENTRY POINT
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login_page()
else:
    app_cittadino()