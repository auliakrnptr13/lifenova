LIFENOVA_CSS = """
<style>
/* ── Warna Utama Tema Life Nova ── */
:root {
    --pink-dark:   #993556;
    --pink-mid:    #D4537E;
    --pink-light:  #FBEAF0;
    --pink-border: #ED93B1;
    --green-dark:  #3B6D11;
    --green-mid:   #639922;
    --green-light: #EAF3DE;
    --green-border:#97C459;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

html, body, [data-testid="stWidgetLabel"] p {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.alert-success {
    background-color: var(--green-light);
    color: var(--green-dark);
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid var(--green-border);
    margin-bottom: 16px;
    font-size: 14px;
    font-weight: 500;
}
.alert-error {
    background-color: var(--pink-light);
    color: var(--pink-dark);
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid var(--pink-border);
    margin-bottom: 16px;
    font-size: 14px;
    font-weight: 500;
}

.lifenova-nav {
    background: linear-gradient(135deg, var(--green-dark), #2c520c);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.lifenova-nav .brand {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.5px;
}
.lifenova-nav .user-info {
    font-size: 13px;
    color: #EAF3DE;
    background: rgba(255,255,255,0.15);
    padding: 6px 12px;
    border-radius: 20px;
}

.welcome-banner {
    background: linear-gradient(135deg, var(--pink-dark), #7a2642);
    color: white;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 15px rgba(153, 53, 86, 0.2);
}
.welcome-banner .wb-name { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
.welcome-banner .wb-sub { font-size: 14px; opacity: 0.85; }

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #f0f0f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.04);
}
.stat-card .label { font-size: 12px; text-transform: uppercase; color: #777; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 6px; }
.stat-card .value { font-size: 28px; font-weight: 700; color: #1a1a1a; line-height: 1.2; }
.stat-card .delta-green { font-size: 12px; color: var(--green-mid); font-weight: 500; margin-top: 4px; }
.stat-card .delta-pink { font-size: 12px; color: var(--pink-mid); font-weight: 500; margin-top: 4px; }

.fitur-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #f0f0f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    height: 170px;
    margin-bottom: 10px;
}
.fitur-card .fc-icon {
    width: 36px; height: 36px;
    border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 18px; margin-bottom: 12px;
}
.fitur-card .fc-icon-p { background: var(--pink-light); }
.fitur-card .fc-icon-g { background: var(--green-light); }
.fitur-card h4 { margin: 0 0 6px 0; font-size: 15px; font-weight: 600; color: #1a1a1a; }
.fitur-card p { margin: 0; font-size: 12px; color: #666; line-height: 1.4; }

.rw-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 16px;
    background: white;
    border-radius: 10px;
    border: 1px solid #f3f3f3;
    margin-bottom: 8px;
}
.rw-item .rw-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.rw-item .rw-icon-p { background: var(--pink-light); }
.rw-item .rw-icon-g { background: var(--green-light); }
.rw-item .rw-info { flex: 1; margin-left: 12px; }
.rw-item .rw-name { font-size: 13px; font-weight: 600; color: #222; }
.rw-item .rw-date { font-size: 11px; color: #999; }
.rw-item .rw-val { font-size: 13px; font-weight: 700; color: var(--pink-dark); }

div.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    border-color: var(--green-mid) !important;
    color: var(--green-mid) !important;
}
</style>
"""
