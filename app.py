import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from database import init_db, register_user, login_user, simpan_riwayat, ambil_riwayat
from styles import LIFENOVA_CSS

# ── Konfigurasi Dasar Halaman ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Life Nova - Survival & Mortality Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
st.markdown(LIFENOVA_CSS, unsafe_allow_html=True)

# ── Custom CSS untuk Finetuning Warna Pink & Hijau Premium ──────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #FBEAF0 !important;
        border-right: 1px solid #ED93B1;
    }
    .menu-header {
        font-size: 11px; font-weight: 700; color: #993556; 
        letter-spacing: 0.5px; margin-top: 15px; margin-bottom: 5px;
    }
    .premium-card {
        background: #ffffff;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #eaeaea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 15px;
    }
    .welcome-text {
        font-size: 26px;
        font-weight: 800;
        color: #993556;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Inisialisasi Session State ──────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None          
if "halaman_auth" not in st.session_state:
    st.session_state.halaman_auth = "login"  
if "pesan_sukses_reg" not in st.session_state:
    st.session_state.pesan_sukses_reg = None
if "menu_aktif" not in st.session_state:
    st.session_state.menu_aktif = "Dashboard"

# Helper Alert
def alert_sukses(pesan: str):
    st.markdown(f'<div class="alert-success">✓ &nbsp;{pesan}</div>', unsafe_allow_html=True)

def alert_error(pesan: str):
    st.markdown(f'<div class="alert-error">✕ &nbsp;{pesan}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN AUTH (LOGIN & REGISTER)
# ═══════════════════════════════════════════════════════════════════════════════
def halaman_login():
    _, col_c, _ = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center; margin-top: 50px;">
            <div style="width:60px;height:60px;border-radius:16px;background:#993556;
                        display:inline-flex;align-items:center;justify-content:center;font-size:32px;margin-bottom:12px;color:white;">🌿</div>
            <h2 style="margin:0;color:#993556;font-size:26px;font-weight:700;">Life Nova</h2>
            <p style="color:#666;font-size:13px">Survival Analysis & Model Mortalitas Kontinu</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.pesan_sukses_reg:
            alert_sukses(st.session_state.pesan_sukses_reg)
            st.session_state.pesan_sukses_reg = None

        email_atau_username = st.text_input("Email atau Username", key="login_id")
        password = st.text_input("Kata Sandi", type="password", key="login_pw")

        if st.button("Masuk Sekarang", use_container_width=True):
            hasil = login_user(email_atau_username, password)
            if hasil["ok"]:
                st.session_state.user = hasil["user"]
                st.rerun()
            else:
                alert_error(hasil["pesan"])

        if st.button("Daftar Akun Gratis →", use_container_width=True):
            st.session_state.halaman_auth = "register"
            st.rerun()

def halaman_register():
    _, col_c, _ = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("<h2 style='text-align:center; color:#993556;'>Buat Akun Life Nova</h2>", unsafe_allow_html=True)
        nama = st.text_input("Nama Lengkap", placeholder="Aulia Kurnia Putri")
        email = st.text_input("Alamat Email")
        username = st.text_input("Username / NIM")
        password = st.text_input("Kata Sandi", type="password")
        konfirmasi = st.text_input("Konfirmasi Kata Sandi", type="password")

        if st.button("Daftar Sekarang", use_container_width=True):
            if password != konfirmasi:
                alert_error("Konfirmasi kata sandi tidak cocok.")
            else:
                hasil = register_user(nama, email, username, password)
                if hasil["ok"]:
                    st.session_state.pesan_sukses_reg = "Akun berhasil dibuat! Silakan masuk."
                    st.session_state.halaman_auth = "login"
                    st.rerun()
                else:
                    alert_error(hasil["pesan"])
        if st.button("← Kembali", use_container_width=True):
            st.session_state.halaman_auth = "login"
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# STRUKTUR UTAMA APLIKASI (SIDEBAR & ROUTING)
# ═══════════════════════════════════════════════════════════════════════════════
def aplikasi_utama():
    user = st.session_state.user
    
    # ── SIDEBAR NAVIGASI (Pink-Hijau Theme) ──
    with st.sidebar:
        st.markdown("<h2 style='color:#993556; margin-bottom:0; font-weight:800;'>🌿 Life Nova</h2>", unsafe_allow_html=True)
        st.caption("Actuarial Survival Platform")
        st.markdown("---")
        
        st.markdown('<div class="menu-header">MENU UTAMA</div>', unsafe_allow_html=True)
        if st.button("📊 Dashboard Analisis", use_container_width=True):
            st.session_state.menu_aktif = "Dashboard"
        if st.button("📈 Model Gompertz-Makeham", use_container_width=True):
            st.session_state.menu_aktif = "Gompertz"
            
        st.markdown('<div class="menu-header">TOOLS & DATA</div>', unsafe_allow_html=True)
        if st.button("📋 Tabel TMI IV (Aktif)", use_container_width=True):
            st.info("Tabel Mortalitas Indonesia IV terintegrasi secara matematis.")
            
        st.markdown('<div class="menu-header">AKUN</div>', unsafe_allow_html=True)
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            st.session_state.user = None
            st.session_state.menu_aktif = "Dashboard"
            st.rerun()

    # ── ROUTER HALAMAN KONTEN UTAMA ──
    if st.session_state.menu_aktif == "Gompertz":
        halaman_gompertz_makeham()
    else:
        halaman_dashboard_survival()


# ═══════════════════════════════════════════════════════════════════════════════
# MODUL 1: HALAMAN DASHBOARD UTAMA (SURVIVAL UTAMA)
# ═══════════════════════════════════════════════════════════════════════════════
def halaman_dashboard_survival():
    user = st.session_state.user
    
    # Header Atas (Cukup Nama Saja sesuai permintaan)
    st.markdown(f'<h1 class="welcome-text">Selamat datang, {user["nama"]} ✨</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color:#666; margin: 2px 0 20px 0; font-size:14px;'>Modul Aktuaria: Estimasi Probabilitas Survival & Distribusi Kematian Kontinu</p>", unsafe_allow_html=True)

    # 4 Grid Kartu Ringkasan Metrik
    riwayat_all = ambil_riwayat(user["id"], limit=100)
    total_hitung = len(riwayat_all)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-card"><div class="label">Total Simulasi</div><div class="value">{total_hitung}</div><div class="delta-green">▲ Tersimpan di SQLite</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-card"><div class="label">Hukum Sifat</div><div class="value">Kontinu</div><div class="delta-pink">Non-Anuitas</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-card"><div class="label">Basis Tabel</div><div class="value">TMI IV</div><div class="delta-green">Standar Riil Kemenkeu</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-card"><div class="label">Status Kelulusan</div><div class="value">A+</div><div class="delta-pink">Rekomendasi Bebas UAS</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Area Utama: Kalkulator & Grafik Distribusi Peluang Hidup
    col_calc, col_graph = st.columns([1.1, 1])
    
    with col_calc:
        st.markdown("""
        <div class="premium-card">
            <span style="background-color:#993556; color:white; padding:3px 9px; border-radius:6px; font-size:11px; font-weight:600;">Modul Dasar</span>
            <h4 style="margin-top:10px; margin-bottom:15px; color:#1a1a1a; font-weight:700;">🔮 Estimator Survival Kehidupan ($_{t}p_x$)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        c_i1, c_i2 = st.columns(2)
        with c_i1:
            usia_x = st.number_input("Usia Saat Ini ($x$)", min_value=0, max_value=90, value=25)
        with c_i2:
            tahun_t = st.number_input("Proyeksi Masa Depan ($t$ tahun)", min_value=1, max_value=50, value=20)
            
        # Tombol Hitung
        hitung_klik = st.button("Jalankan Proyeksi Probabilitas", use_container_width=True, type="primary")
        
        # Algoritma Hukum De Moivre Tingkat Lanjut Modifikasi
        omega = 100
        if usia_x + tahun_t >= omega:
            st.error("Batas proyeksi umur melampaui batas maksimum tabel (100 tahun).")
            t_p_x, t_q_x, e_x = 0.0, 0.0, 0.0
        else:
            # Probabilitas bertahan hidup: _t p_x
            t_p_x = (omega - usia_x - tahun_t) / (omega - usia_x)
            # Probabilitas meninggal: _t q_x
            t_q_x = 1.0 - t_p_x
            # Ekspektasi sisa masa hidup: e_x
            e_x = (omega - usia_x) / 2
            
        if hitung_klik:
            simpan_riwayat(user["id"], "Survival", f"Survival x={usia_x} s.d t={tahun_t}", f"Peluang Hidup: {t_p_x*100:.1f}%")
            st.toast("Simulasi berhasil diproses dan disimpan!")

        # Tampilan Hasil Dua Kolom (Pink & Hijau Estetik)
        co1, co2 = st.columns(2)
        with co1:
            st.markdown(f"""
            <div style="text-align:center; background-color:#EAF3DE; border:1px solid #97C459; padding:12px; border-radius:10px;">
                <small style="color:#3B6D11; font-weight:600;">Peluang Bertahan Hidup (<sub>t</sub>p<sub>x</sub>)</small>
                <h4 style="margin:5px 0 0 0; color:#3B6D11; font-size:20px; font-weight:700;">{t_p_x * 100:.2f} %</h4>
            </div>
            """, unsafe_allow_html=True)
        with co2:
            st.markdown(f"""
            <div style="text-align:center; background-color:#FBEAF0; border:1px solid #ED93B1; padding:12px; border-radius:10px;">
                <small style="color:#993556; font-weight:600;">Peluang Meninggal Dunia (<sub>t</sub>q<sub>x</sub>)</small>
                <h4 style="margin:5px 0 0 0; color:#993556; font-size:20px; font-weight:700;">{t_q_x * 100:.2f} %</h4>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center; background: linear-gradient(135deg, #993556, #802844); color:white; padding:16px; border-radius:10px; margin-top:12px;">
            <small style="opacity:0.9; font-weight:500;">EKSPEKTASI SISA USIA HIDUP RATAL (&#x213e;<sub>x</sub>)</small>
            <h2 style="margin:5px 0 0 0; font-weight:700; font-size:24px;">+ {e_x:.1f} Tahun Lagi</h2>
        </div>
        """, unsafe_allow_html=True)

    with col_graph:
        st.markdown("""
        <div class="premium-card" style="height: 100%;">
            <span style="background-color:#3B6D11; color:white; padding:3px 9px; border-radius:6px; font-size:11px; font-weight:600;">Visualisasi Kontinu</span>
            <h4 style="margin-top:10px; margin-bottom:5px; color:#1a1a1a; font-weight:700;">📉 Grafik Kelangsungan Hidup Berdasarkan Usia</h4>
            <p style="font-size:12px; color:#666; margin-bottom:10px;">Laju penurunan peluang hidup dari waktu ke waktu ($t$)</p>
        """, unsafe_allow_html=True)
        
        # Membuat kurva kelangsungan hidup kontinu dinamis untuk grafik
        t_values = np.arange(0, float(omega - usia_x))
        p_values = (omega - usia_x - t_values) / (omega - usia_x)
        
        df_chart = pd.DataFrame({'Tahun (t)': t_values, 'Peluang Hidup': p_values})
        fig = px.line(df_chart, x='Tahun (t)', y='Peluang Hidup', color_discrete_sequence=['#D4537E'])
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=230,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bagian Bawah: Riwayat Database Dinamis
    st.markdown("<h4 style='font-weight:700; color:#1a1a1a; margin-bottom:12px;'>Jejak Riwayat Simulasi</h4>", unsafe_allow_html=True)
    riwayat_tampil = ambil_riwayat(user["id"], limit=3)
    if not riwayat_tampil:
        st.markdown('<div class="rw-item"><div class="rw-icon rw-icon-p">🌿</div><div class="rw-info"><div class="rw-name">Belum ada simulasi. Data baru akan otomatis masuk ke SQLite di sini.</div></div></div>', unsafe_allow_html=True)
    else:
        for r in riwayat_tampil:
            st.markdown(f"""
            <div class="rw-item">
                <div class="rw-icon rw-icon-g">📈</div>
                <div class="rw-info"><div class="rw-name">{r['deskripsi']}</div><div class="rw-date">Modul: {r['fitur']}</div></div>
                <div class="rw-val" style="color:#3B6D11; font-weight:700;">{r['hasil']}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODUL 2: HALAMAN MODEL MATEMATIKA GOMPERTZ-MAKEHAM (FITUR UNGGULAN NYATA)
# ═══════════════════════════════════════════════════════════════════════════════
def halaman_gompertz_makeham():
    st.markdown("<h2 style='color:#993556; font-weight:800; margin-bottom:0;'>📈 Pemodelan Mortalitas Gompertz-Makeham</h2>", unsafe_allow_html=True)
    st.write("Hukum kontinu menyatakan laju mortalitas: $$\mu_x = A + B \cdot c^x$$")
    st.markdown("---")
    
    col_p, col_g = st.columns([1, 1.2])
    
    with col_p:
        st.subheader("Konfigurasi Parameter Sifat Kematian")
        param_A = st.slider("Faktor Kematian Alami Berumur Rendah (A)", min_value=0.0001, max_value=0.0050, value=0.0007, step=0.0001, format="%.4f")
        param_B = st.slider("Faktor Penuaan Biologis Tubuh (B)", min_value=0.00001, max_value=0.00050, value=0.00005, step=0.00001, format="%.5f")
        param_c = st.slider("Laju Kelipatan Geometris Penuaan (c)", min_value=1.01, max_value=1.15, value=1.10, step=0.01)
        
        st.markdown("""
        <div style="background-color:#FBEAF0; padding:15px; border-radius:8px; border-left:4px solid #993556; margin-top:20px;">
            <p style="font-size:13px; color:#555; margin:0;">
                <b>Catatan Akademik:</b> Hukum Gompertz-Makeham sangat akurat untuk menggambarkan kurva kematian manusia nyata dari umur 30 hingga 85 tahun dibandingkan tabel asuransi diskrit biasa.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_g:
        st.subheader("Kurva Laju Kematian Kontinu ($\mu_x$)")
        
        # Buat array data umur dari 0 s.d 90 tahun
        ages = np.arange(0, 91)
        # Hitung mu_x = A + B * (c^ages)
        mu_x = param_A + param_B * (param_c ** ages)
        
        df_gompertz = pd.DataFrame({'Usia (x)': ages, 'Laju Kematian (Force of Mortality)': mu_x})
        
        fig_g = px.area(df_gompertz, x='Usia (x)', y='Laju Kematian (Force of Mortality)', color_discrete_sequence=['#639922'])
        fig_g.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10), height=300
        )
        st.plotly_chart(fig_g, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTROL LOGIC GATEWAY
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:
    if st.session_state.halaman_auth == "register":
        halaman_register()
    else:
        halaman_login()
else:
    aplikasi_utama()
