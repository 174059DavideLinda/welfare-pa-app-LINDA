import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib
import time

st.set_page_config(
    page_title="Admin - Sistema Welfare PA",
    layout="wide",
    page_icon="⚙️",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');

    /* FIX: Rimosso 'span' e 'div' per evitare sovrapposizione icone (keyare_row_right) */
    html, body, .stMarkdown, p, label, h1, h2, h3, h4, h5, h6, li, a {
        font-family: 'Source Sans 3', sans-serif !important;
    }

    /* ========================
       TESTI GLOBALI — chiari
       su sfondo scuro
    ======================== */
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
        font-family: 'Source Sans 3', sans-serif !important;
    }
    p, span, li {
        color: #cbd5e1;
    }
    /* Testi Streamlit nativi (caption, info, ecc.) */
    .stMarkdown p, .stMarkdown li {
        color: #cbd5e1 !important;
    }
    /* Titoli dentro form */
    [data-testid="stForm"] h3,
    [data-testid="stForm"] h4,
    [data-testid="stVerticalBlock"] h3,
    [data-testid="stVerticalBlock"] h4 {
        color: #e2e8f0 !important;
    }

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

    /* Card login */
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
       HEADER ADMIN
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
        font-size: 1.8rem !important;
        color: #ffffff !important;
        margin: 0 !important;
    }
    .main-header p {
        color: rgba(226,232,240,0.85) !important;
        margin: 0.3rem 0 0 0;
        font-size: 1rem;
    }

    /* ========================
       TITOLI SEZIONE NEI FORM
    ======================== */
    .form-section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #e2e8f0;
        padding: 0.6rem 1rem;
        background: #1a3040;
        border-left: 4px solid #0d9488;
        border-radius: 0 6px 6px 0;
        margin: 1.2rem 0 0.8rem 0;
    }
    .form-subsection {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #2dd4bf;
        margin-bottom: 0.5rem;
    }

    /* ========================
       INFO BOX CATEGORIA
    ======================== */
    .categoria-info {
        background: #162533;
        border: 1px solid #1e4a5e;
        border-left: 4px solid #0d9488;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .categoria-info h3 {
        color: #2dd4bf !important;
        font-size: 1.1rem !important;
        margin: 0 0 0.3rem 0 !important;
        font-weight: 700 !important;
    }
    .categoria-info p {
        color: #94a3b8 !important;
        margin: 0;
        font-size: 0.9rem;
    }

    /* ========================
       SIDEBAR
    ======================== */
    section[data-testid="stSidebar"] { background: #1a2e3b !important; }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stSelectbox > div > div { color: #1a2e3b !important; }
    section[data-testid="stSidebar"] .stMetric label {
        color: #94a3b8 !important;
        font-size: 0.78rem;
    }
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-size: 1.4rem !important;
    }

    .user-chip {
        background: rgba(13,148,136,0.15);
        border: 1px solid rgba(13,148,136,0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0 1rem 0;
        text-align: center;
    }
    .user-chip .u-name    { font-weight: 700; font-size: 1rem; margin-bottom: 0.2rem; color: #e2e8f0; }
    .user-chip .u-handle { font-size: 0.82rem; color: #94a3b8; }
    .user-chip .u-role {
        display: inline-block;
        background: rgba(245,158,11,0.2);
        border: 1px solid rgba(245,158,11,0.45);
        border-radius: 12px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
        color: #fbbf24 !important;
    }

    /* ========================
       TABS DATABASE
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

    /* ========================
       FORM STYLING
    ======================== */
    [data-testid="stForm"] {
        background: #1a2e3b;
        border: 1px solid #2a4a5e;
        border-radius: 12px;
        padding: 1.5rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }

    /* Label input */
    .stTextInput label, .stTextArea label,
    .stSelectbox label, .stNumberInput label,
    .stSlider label, .stCheckbox label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ========================
       NORMATIVA / INFO BOX
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

    /* ========================
       VARIE
    ======================== */
    hr { margin: 1.5rem 0; opacity: 0.15; border-color: #2a4a5e; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTENTICAZIONE
# ==========================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_auth_db():
    conn = sqlite3.connect('welfare.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        nome_completo TEXT,
        ruolo TEXT DEFAULT 'admin',
        data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ultimo_accesso TIMESTAMP
    )''')
    
    c.execute("SELECT COUNT(*) FROM admin_users WHERE username = ?", ('mario.rossi',))
    if c.fetchone()[0] == 0:
        
        c.execute('''INSERT INTO admin_users (username, password_hash, nome_completo, ruolo)
                     VALUES (?, ?, ?, ?)''',
                  ('mario.rossi', hash_password('Welf@re_Admin2026!'), 'Mario Rossi — Amministratore Principale', 'superadmin'))
    conn.commit()
    conn.close()

def verifica_credenziali(username, password):
    conn = sqlite3.connect('welfare.db')
    c = conn.cursor()
    c.execute('''SELECT id, username, nome_completo, ruolo FROM admin_users
                 WHERE username = ? AND password_hash = ?''',
              (username, hash_password(password)))
    user = c.fetchone()
    if user:
        c.execute("UPDATE admin_users SET ultimo_accesso = CURRENT_TIMESTAMP WHERE id = ?", (user[0],))
        conn.commit()
    conn.close()
    return user

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ==========================================
# PAGINA LOGIN
# ==========================================

def pagina_login():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none; }
        .main .block-container { max-width: 700px; padding-top: 0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-hero">
        <div class="login-badge">⚙️ Pannello Riservato · Welfare PA</div>
        <h1>Sistema Welfare PA</h1>
        <p>Accesso amministratori — area riservata al personale autorizzato</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-top">
        <div class="card-title">🔐 Accesso Amministratori</div>
        <div class="card-sub">Inserisci le tue credenziali per accedere al pannello</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        col_u, col_p = st.columns(2)
        with col_u:
            username = st.text_input("👤 Nome Utente", placeholder="es. davide")
        with col_p:
            password = st.text_input("🔑 Password", type="password", placeholder="••••••••")

        st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 Accedi al Sistema", use_container_width=True, type="primary")

        if submitted:
            if not username or not password:
                st.error("⚠️ Inserisci sia username che password.")
            else:
                user = verifica_credenziali(username, password)
                if user:
                    st.session_state.logged_in       = True
                    st.session_state.user_id         = user[0]
                    st.session_state.username        = user[1]
                    st.session_state.nome_completo   = user[2]
                    st.session_state.ruolo           = user[3]
                    st.success(f"✅ Benvenuto, {user[2]}!")
                    st.rerun()
                else:
                    st.error("❌ Credenziali non valide. Riprova.")

    st.markdown("""
    <div class="login-bottom">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="normativa-box" style="margin-top:1.5rem;">
        🔒 Accesso protetto con crittografia SHA-256. I dati di sessione sono gestiti in modo sicuro.
        Solo il personale autorizzato può accedere a questa sezione del sistema.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:#aaa; font-size:0.8rem; padding:2rem 0 0.5rem 0;">
        Sistema Welfare PA · Progetto Universitario 2026 · Solo a scopo dimostrativo
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# ADMIN
# ==========================================

def mostra_sidebar(conn):
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
            <div style="font-size:2.5rem;">⚙️</div>
            <div style="font-family:'Lora',serif; font-size:1.15rem; font-weight:700; margin-top:0.3rem;">
                Welfare PA
            </div>
            <div style="font-size:0.78rem; opacity:0.5; margin-top:0.2rem;">Pannello Amministrativo</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"""
        <div class="user-chip">
            <div class="u-name">👤 {st.session_state.nome_completo}</div>
            <div class="u-handle">@{st.session_state.username}</div>
            <div class="u-role">{st.session_state.ruolo.upper()} 🔑</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            logout()

        st.markdown("---")

        st.markdown('<div style="font-size:0.78rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; opacity:0.6; margin-bottom:0.8rem;">📊 Statistiche</div>', unsafe_allow_html=True)

        tables = {
            'bonus_famiglia':   '👨‍👩‍👧‍👦 Famiglia',
            'bonus_istruzione': '🎓 Istruzione',
            'bonus_salute':     '🏥 Salute',
            'bonus_casa':       '🏠 Casa',
            'bonus_lavoro':     '💼 Lavoro',
            'bonus_generale':   '🚌 Trasporti',
        }
        totale = 0
        for table, label in tables.items():
            try:
                n = pd.read_sql_query(f"SELECT COUNT(*) as c FROM {table}", conn).iloc[0]['c']
                totale += n
                st.metric(label, n)
            except Exception:
                pass

        st.markdown("---")
        st.metric("🗂️ Totale Bonus", totale)

        st.markdown("---")
        st.markdown('<div style="opacity:0.4; font-size:0.75rem;">Sistema Welfare PA v2.0<br>Progetto Universitario 2026</div>', unsafe_allow_html=True)

def section_title(icon, text):
    st.markdown(f'<div class="form-section-title">{icon} {text}</div>', unsafe_allow_html=True)

def subsection(text):
    st.markdown(f'<div class="form-subsection">{text}</div>', unsafe_allow_html=True)

def categoria_info(emoji, titolo, descrizione):
    st.markdown(f"""
    <div class="categoria-info">
        <h3>{emoji} {titolo}</h3>
        <p>{descrizione}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATABASE
# ==========================================

LISTA_REGIONI = [
    "TUTTA ITALIA (Nazionale)",
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
    "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana",
    "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"
]

def init_db():
    conn = sqlite3.connect('welfare.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bonus_famiglia (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        inserito_da TEXT, regione TEXT, nome TEXT, ente TEXT, descrizione TEXT, link TEXT,
        importo TEXT, isee_min INTEGER, max_isee INTEGER, min_figli INTEGER, min_eta_figli INTEGER, max_eta_figli INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bonus_istruzione (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        inserito_da TEXT, regione TEXT, nome TEXT, ente TEXT, descrizione TEXT, link TEXT,
        importo TEXT, max_isee INTEGER, livello_studio TEXT, voto_minimo INTEGER, solo_fuori_sede BOOLEAN)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bonus_salute (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        inserito_da TEXT, regione TEXT, nome TEXT, ente TEXT, descrizione TEXT, link TEXT,
        importo TEXT, max_isee INTEGER, min_eta INTEGER, max_eta INTEGER, richiede_patologia BOOLEAN, richiede_invalidita BOOLEAN)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bonus_casa (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        inserito_da TEXT, regione TEXT, nome TEXT, ente TEXT, descrizione TEXT, link TEXT,
        importo TEXT, max_isee INTEGER, min_eta INTEGER, max_eta INTEGER, ambito TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bonus_lavoro (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        inserito_da TEXT, regione TEXT, nome TEXT, ente TEXT, descrizione TEXT, link TEXT,
        importo TEXT, max_isee INTEGER, min_eta INTEGER, max_eta INTEGER, stato_occupazionale TEXT, solo_donne BOOLEAN)''')
    # MODIFICA: Aggiunto campo 'tipo_mezzo'
    c.execute('''CREATE TABLE IF NOT EXISTS bonus_generale (
        id INTEGER PRIMARY KEY AUTOINCREMENT, data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        inserito_da TEXT, regione TEXT, categoria TEXT, tipo_mezzo TEXT, nome TEXT, ente TEXT, descrizione TEXT, link TEXT,
        importo TEXT, max_isee INTEGER, min_eta_cittadino INTEGER, max_eta_cittadino INTEGER)''')
    conn.commit()
    return conn

# ==========================================
# FORM INSERIMENTO
# ==========================================

def campi_generali():
    col1, col2 = st.columns(2)
    with col1:
        nome    = st.text_input("Nome Bonus *", placeholder="Es. Assegno Unico Universale")
        ente    = st.text_input("Ente Erogatore *", placeholder="Es. INPS")
        importo = st.text_input("Importo", placeholder="Es. Fino a 175€/mese")
    with col2:
        link        = st.text_input("Link Bando/Informazioni", placeholder="https://...")
        descrizione = st.text_area("Descrizione", placeholder="Descrivi il bonus, le finalità e le modalità di accesso...", height=120)
    return nome, ente, importo, link, descrizione

def campo_isee():
    subsection("Requisiti economici (ISEE)")
    c1, c2 = st.columns([1, 2])
    no_limit = c1.checkbox("Nessun limite ISEE")
    max_isee = 99999999 if no_limit else c2.number_input("ISEE Massimo (€)", 0, 200000, 30000, step=500)
    return max_isee

def salva_ok(nome, ente, regione):
    st.success(f"✅ **{nome}** salvato per *{regione}*!")


def form_famiglia(conn, regione):
    categoria_info("👨‍👩‍👧‍👦", "Bonus Famiglia",
                   "Assegno Unico, Bonus Nido, Sostegno alla Natalità e altri aiuti per nuclei familiari")

    with st.form("form_famiglia", clear_on_submit=True):
        section_title("📝", "Dati Generali")
        nome, ente, importo, link, descrizione = campi_generali()

        section_title("🎯", "Requisiti di Accesso")
        col1, col2, col3 = st.columns(3)

        with col1:
            subsection("ISEE")
            isee_min = st.number_input("ISEE Minimo (€)", 0, 200000, 0, step=500)
            no_limit = st.checkbox("Nessun limite ISEE massimo")
            max_isee = 99999999 if no_limit else st.number_input("ISEE Massimo (€)", 0, 200000, 40000, step=500)

        with col2:
            subsection("Composizione nucleo")
            min_figli    = st.number_input("N° Minimo Figli", 0, 10, 1)
            min_eta_fig  = st.number_input("Età Minima Figlio", 0, 30, 0)

        with col3:
            subsection("Limiti età figli")
            max_eta_fig = st.number_input("Età Massima Figlio", 0, 30, 18,
                                          help="Età massima del figlio per beneficiare del bonus")

        st.markdown("---")
        if st.form_submit_button("💾 Salva Bonus Famiglia", use_container_width=True, type="primary"):
            if not nome or not ente:
                st.error("⚠️ Nome e Ente sono obbligatori.")
                return
            conn.cursor().execute('''INSERT INTO bonus_famiglia
                (regione, nome, ente, descrizione, link, importo, isee_min, max_isee, min_figli, min_eta_figli, max_eta_figli, inserito_da)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (regione, nome, ente, descrizione, link, importo, isee_min, max_isee, min_figli, min_eta_fig, max_eta_fig, st.session_state.username))
            conn.commit()
            salva_ok(nome, ente, regione)


def form_istruzione(conn, regione):
    categoria_info("🎓", "Bonus Istruzione",
                   "Borse di studio, Libri scolastici, Mense, Trasporto, Diritto allo Studio universitario")

    with st.form("form_istruzione", clear_on_submit=True):
        section_title("📝", "Dati Generali")
        nome, ente, importo, link, descrizione = campi_generali()

        section_title("🎯", "Requisiti di Accesso")
        col1, col2, col3 = st.columns(3)

        with col1:
            subsection("Livello di studio")
            livello = st.selectbox("Destinatari", ["Tutti i livelli", "Asilo Nido", "Scuola Primaria",
                                                   "Scuola Secondaria I°", "Scuola Secondaria II°",
                                                   "Università", "Master/Dottorato"])
        with col2:
            max_isee = campo_isee()

        with col3:
            subsection("Requisiti di merito")
            voto      = st.slider("Voto/Media Minima", 60, 110, 60)
            fuori_sede = st.checkbox("Solo fuori sede")

        st.markdown("---")
        if st.form_submit_button("💾 Salva Bonus Istruzione", use_container_width=True, type="primary"):
            if not nome or not ente:
                st.error("⚠️ Nome e Ente sono obbligatori.")
                return
            conn.cursor().execute('''INSERT INTO bonus_istruzione
                (regione, nome, ente, descrizione, link, importo, max_isee, livello_studio, voto_minimo, solo_fuori_sede, inserito_da)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                (regione, nome, ente, descrizione, link, importo, max_isee, livello, voto, fuori_sede, st.session_state.username))
            conn.commit()
            salva_ok(nome, ente, regione)


def form_salute(conn, regione):
    categoria_info("🏥", "Bonus Salute",
                   "Ticket sanitari, Assistenza domiciliare, Farmaci, Protesi, Cure termali")

    with st.form("form_salute", clear_on_submit=True):
        section_title("📝", "Dati Generali")
        nome, ente, importo, link, descrizione = campi_generali()

        section_title("🎯", "Requisiti di Accesso")
        col1, col2, col3 = st.columns(3)

        with col1:
            max_isee = campo_isee()

        with col2:
            subsection("Limiti di età")
            min_eta = st.number_input("Età Minima", 0, 100, 0, help="0 = nessun limite")
            max_eta = st.number_input("Età Massima", 0, 100, 100, help="100 = nessun limite")

        with col3:
            subsection("Condizioni sanitarie richieste")
            patologia  = st.checkbox("Patologia cronica/rara certificata")
            invalidita = st.checkbox("Invalidità civile")

        st.markdown("---")
        if st.form_submit_button("💾 Salva Bonus Salute", use_container_width=True, type="primary"):
            if not nome or not ente:
                st.error("⚠️ Nome e Ente sono obbligatori.")
                return
            conn.cursor().execute('''INSERT INTO bonus_salute
                (regione, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, richiede_patologia, richiede_invalidita, inserito_da)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (regione, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, patologia, invalidita, st.session_state.username))
            conn.commit()
            salva_ok(nome, ente, regione)


def form_casa(conn, regione):
    categoria_info("🏠", "Bonus Casa",
                   "Affitto, Mutuo Prima Casa, Ristrutturazioni, Bollette, Efficienza Energetica")

    with st.form("form_casa", clear_on_submit=True):
        section_title("📝", "Dati Generali")
        col1, col2 = st.columns(2)
        with col1:
            nome    = st.text_input("Nome Bonus *", placeholder="Es. Contributo Affitto Giovani")
            ente    = st.text_input("Ente Erogatore *", placeholder="Es. Comune / Regione")
            importo = st.text_input("Importo", placeholder="Es. Fino a 2000€ annui")
        with col2:
            link   = st.text_input("Link Bando", placeholder="https://...")
            ambito = st.selectbox("Ambito Applicazione",
                                  ["Tutti", "Affitto", "Acquisto Prima Casa", "Ristrutturazione",
                                   "Bollette/Utenze", "Efficienza Energetica", "Mutuo"])
            descrizione = st.text_area("Descrizione", placeholder="Descrivi requisiti e modalità...", height=80)

        section_title("🎯", "Requisiti di Accesso")
        col1, col2 = st.columns(2)
        with col1:
            max_isee = campo_isee()
        with col2:
            subsection("Limiti di età richiedente")
            min_eta = st.number_input("Età Minima", 0, 100, 18)
            max_eta = st.number_input("Età Massima", 0, 100, 100, help="100 = nessun limite")

        st.markdown("---")
        if st.form_submit_button("💾 Salva Bonus Casa", use_container_width=True, type="primary"):
            if not nome or not ente:
                st.error("⚠️ Nome e Ente sono obbligatori.")
                return
            conn.cursor().execute('''INSERT INTO bonus_casa
                (regione, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, ambito, inserito_da)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                (regione, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, ambito, st.session_state.username))
            conn.commit()
            salva_ok(nome, ente, regione)


def form_lavoro(conn, regione):
    categoria_info("💼", "Bonus Lavoro",
                   "Disoccupazione, Incentivi assunzioni, Formazione, Supporto Partite IVA, Garanzia Giovani")

    with st.form("form_lavoro", clear_on_submit=True):
        section_title("📝", "Dati Generali")
        nome, ente, importo, link, descrizione = campi_generali()

        section_title("🎯", "Requisiti di Accesso")
        col1, col2, col3 = st.columns(3)

        with col1:
            subsection("Target destinatari")
            stato       = st.selectbox("Rivolto a", ["Tutti", "Disoccupati/Inoccupati",
                                                     "Lavoratori Dipendenti", "Partite IVA/Autonomi",
                                                     "Studenti/Tirocinanti"])
            solo_donne = st.checkbox("Riservato alle Donne", help="Bonus Donna / incentivi occupazione femminile")

        with col2:
            max_isee = campo_isee()

        with col3:
            subsection("Limiti di età lavoratore")
            min_eta = st.number_input("Età Minima", 0, 100, 18)
            max_eta = st.number_input("Età Massima", 0, 100, 100, help="100 = nessun limite")

        st.markdown("---")
        if st.form_submit_button("💾 Salva Bonus Lavoro", use_container_width=True, type="primary"):
            if not nome or not ente:
                st.error("⚠️ Nome e Ente sono obbligatori.")
                return
            conn.cursor().execute('''INSERT INTO bonus_lavoro
                (regione, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, stato_occupazionale, solo_donne, inserito_da)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (regione, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, stato, solo_donne, st.session_state.username))
            conn.commit()
            salva_ok(nome, ente, regione)


def form_trasporti(conn, regione):
    categoria_info("🚌", "Bonus Trasporti",
                   "Abbonamenti TPL, Bonus Mobilità, Agevolazioni trasporto studenti e lavoratori")

    with st.form("form_trasporti", clear_on_submit=True):
        section_title("📝", "Dati Generali")
        nome, ente, importo, link, descrizione = campi_generali()
        
        col_cat, col_dummy = st.columns(2)
        with col_cat:
            tipo_mezzo = st.selectbox("Tipo Agevolazione (Sottocategoria)", 
                                      ["Tutti", "Abbonamento TPL", "Bici/Monopattino", "Carburante", "Treni/Aerei"])

        section_title("🎯", "Requisiti di Accesso")
        col1, col2 = st.columns(2)
        with col1:
            max_isee = campo_isee()
        with col2:
            subsection("Limiti di età")
            min_eta = st.number_input("Età Minima", 0, 100, 0)
            max_eta = st.number_input("Età Massima", 0, 100, 100)

        st.markdown("---")
        if st.form_submit_button("💾 Salva Bonus Trasporti", use_container_width=True, type="primary"):
            if not nome or not ente:
                st.error("⚠️ Nome e Ente sono obbligatori.")
                return
            conn.cursor().execute('''INSERT INTO bonus_generale
                (regione, categoria, tipo_mezzo, nome, ente, descrizione, link, importo, max_isee, min_eta_cittadino, max_eta_cittadino, inserito_da)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (regione, "TRASPORTI", tipo_mezzo, nome, ente, descrizione, link, importo, max_isee, min_eta, max_eta, st.session_state.username))
            conn.commit()
            salva_ok(nome, ente, regione)


# ==========================================
# SEZIONE DATABASE
# ==========================================

def sezione_database(conn):
    st.markdown("---")
    st.markdown("## 🗄️ Gestione Database")
    st.caption("Visualizza ed elimina i record inseriti.")

    tabs = st.tabs(["👨‍👩‍👧‍👦 Famiglia", "🎓 Istruzione", "🏥 Salute", "🏠 Casa", "💼 Lavoro", "🚌 Trasporti"])

    # Configurazione: (Nome Tabella, Oggetto Tab, Messaggio Vuoto)
    config_tabelle = [
        ("bonus_famiglia", tabs[0], "Nessun bonus famiglia inserito"),
        ("bonus_istruzione", tabs[1], "Nessun bonus istruzione inserito"),
        ("bonus_salute", tabs[2], "Nessun bonus salute inserito"),
        ("bonus_casa", tabs[3], "Nessun bonus casa inserito"),
        ("bonus_lavoro", tabs[4], "Nessun bonus lavoro inserito"),
        ("bonus_generale", tabs[5], "Nessun bonus trasporti inserito"),
    ]

    for tabella, tab, msg_vuoto in config_tabelle:
        with tab:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {tabella} ORDER BY id DESC", conn)
                
                if len(df) > 0:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.markdown("---")
                    with st.expander(f"🗑️ Elimina record da {tabella}", expanded=False):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            id_to_del = st.selectbox(
                                "Seleziona l'ID del bonus da eliminare", 
                                df['id'].tolist(), 
                                key=f"sel_{tabella}"
                            )
                        with c2:
                            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                            if st.button(f"❌ Elimina ID {id_to_del}", key=f"del_{tabella}", type="primary"):
                                cursor = conn.cursor()
                                cursor.execute(f"DELETE FROM {tabella} WHERE id = ?", (id_to_del,))
                                conn.commit()
                                st.warning(f"Record {id_to_del} eliminato definitivamente.")
                                time.sleep(1) 
                                st.rerun() 
                else:
                    st.info(msg_vuoto)

            except Exception as e:
                st.error(f"Errore gestione DB: {e}")


# ==========================================
# MAIN
# ==========================================

def main():
    init_auth_db()

    # autenticazione
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        pagina_login()
        return

    conn = init_db()

    # Sidebar
    mostra_sidebar(conn)

    # Header
    st.markdown("""
    <div class="main-header">
        <div style="font-size:3rem; line-height:1; flex-shrink:0;">⚙️</div>
        <div>
            <h1>Pannello Amministrativo — Welfare PA</h1>
            <p>Gestione centralizzata delle agevolazioni nazionali e regionali</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📋 Inserimento Nuovo Bonus")
    col1, col2 = st.columns([2, 1])
    with col1:
        categoria = st.selectbox(
            "Categoria di Agevolazione",
            ["👨‍👩‍👧‍👦 Famiglia", "🎓 Istruzione", "🏥 Salute", "🏠 Casa", "💼 Lavoro", "🚌 Trasporti"],
            help="Scegli la categoria più appropriata"
        )
    with col2:
        regione = st.selectbox("Ambito Territoriale", LISTA_REGIONI)

    st.markdown("---")

    if "Famiglia"   in categoria: form_famiglia(conn, regione)
    elif "Istruzione" in categoria: form_istruzione(conn, regione)
    elif "Salute"     in categoria: form_salute(conn, regione)
    elif "Casa"       in categoria: form_casa(conn, regione)
    elif "Lavoro"     in categoria: form_lavoro(conn, regione)
    elif "Trasporti"  in categoria: form_trasporti(conn, regione)

    # Database
    sezione_database(conn)

    st.markdown(f"""
    <div style="text-align:center; color:#aaa; font-size:0.8rem; padding:2rem 0 0.5rem 0;">
        Sistema Welfare PA · Progetto Universitario 2026<br>
        Sessione attiva: <strong style="color:#888;">{st.session_state.nome_completo}</strong>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
