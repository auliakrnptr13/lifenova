import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, register_user, login_user, simpan_riwayat, ambil_riwayat
from styles import LIFENOVA_CSS

st.set_page_config(
    page_title="Life Nova - Platform Aktuaria Digital",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
st.markdown(LIFENOVA_CSS, unsafe_allow_html=True)

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
    /* Guntingan kartu biar lebih estetik & modern */
    .premium-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #eaeaea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .welcome-text {
        font-size: 24px;
        font-weight: 700;
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

def halaman_login():
    _, col_c, _ = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center; margin-top: 50px;">
            <div style="width:60px;height:60px;border-radius:16px;background:#993556;
                        display:inline-flex;align-items:center;justify-content:center;font-size:32px;margin-bottom:12px;color:white;">🌿</div>
            <h2 style="margin:0;color:#993556;font-size:26px;font-weight:700;">Life Nova</h2>
            <p style="color:#666;font-size:13px">Hitung premi & analisis survival aktuaria cerdas</p>
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

def aplikasi_utama():
    user = st.session_state.user
    
    # ── SIDEBAR KIRI (Navigasi Menu Sesuai Draf Gambar image_a9fcde.png) ──
    with st.sidebar:
        st.markdown("<h2 style='color:#993556; margin-bottom:0; font-weight:800;'>🌿 Life Nova</h2>", unsafe_allow_html=True)
        st.caption("Actuarial Intelligence Platform")
        st.markdown("---")
        
        st.markdown('<div class="menu-header">MENU UTAMA</div>', unsafe_allow_html=True)
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.menu_aktif = "Dashboard"
        if st.button("🧮 Endowment", use_container_width=True):
            st.session_state.menu_aktif = "Endowment"
        if st.button("📈 Asuransi Kontinu", use_container_width=True):
            st.sidebar.toast("Modul Kontinu sedang disiapkan!")
        if st.button("⚖️ Diskrit vs Kontinu", use_container_width=True):
            st.sidebar.toast("Modul Komparasi sedang disiapkan!")
        if st.button("💓 Survival Analysis", use_container_width=True):
            st.sidebar.toast("Modul Survival sedang disiapkan!")
            
        st.markdown('<div class="menu-header">TOOLS</div>', unsafe_allow_html=True)
        if st.button("📋 Tabel Mortalitas", use_container_width=True):
            st.info("Tabel Mortalitas TMI IV aktif.")
        if st.button("📥 Export PDF", use_container_width=True):
            st.success("Fitur ekspor PDF siap jalan.")
            
        st.markdown('<div class="menu-header">AKUN</div>', unsafe_allow_html=True)
        if st.button("🚪 Keluar", use_container_width=True):
            st.session_state.user = None
            st.session_state.menu_aktif = "Dashboard"
            st.rerun()

    col_header_kiri, col_header_kanan = st.columns([3, 1])
    with col_header_kiri:
        st.markdown(f'<h1 class="welcome-text">Selamat datang, {user["nama"]} ✨</h1>', unsafe_allow_html=True)
        st.markdown("<p style='color:#666; margin: 2px 0 15px 0; font-size:14px;'>Platform Perhitungan Aktual Digital Anda</p>", unsafe_allow_html=True)
        
    with col_header_kanan:
        st.markdown("<div style='margin-top:5px;'></div>", unsafe_allow_html=True)
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("📥 Export PDF", key="top_pdf", use_container_width=True):
                st.toast("Mempersiapkan dokumen PDF...")
        with c_btn2:
            if st.button("➕ Kalkulasi Baru", key="top_new", use_container_width=True):
                st.session_state.menu_aktif = "Endowment"
                st.toast("Kalkulator diaktifkan!")

    riwayat_all = ambil_riwayat(user["id"], limit=100)
    total_hitung = len(riwayat_all)
    total_endowment = sum(1 for r in riwayat_all if "Endowment" in r["fitur"])

    # 2. Grid Kartu Metrik Ringkasan Atas
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-card"><div class="label">Total Kalkulasi</div><div class="value">{total_hitung}</div><div class="delta-green">▲ +3 minggu ini</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="stat-card"><div class="label">🧮 Endowment</div><div class="value">{total_endowment}</div><div class="delta-pink">Modul terbanyak</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-card"><div class="label">📈 Kontinu</div><div class="value">9</div><div class="delta-green">3 dibanding diskrit</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-card"><div class="label">📋 PDF Diekspor</div><div class="value">5</div><div class="delta-green">Siap dikumpul</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. AREA TENGAH: AREA KALKULATOR & GRAFIK (Berdampingan Presisi)
    col_kalkulator, col_grafik = st.columns([1.1, 1])

    with col_kalkulator:
        st.markdown("""
        <div class="premium-card">
            <span style="background-color:#993556; color:white; padding:3px 9px; border-radius:6px; font-size:11px; font-weight:600;">Pertemuan 11</span>
            <h4 style="margin-top:10px; margin-bottom:15px; color:#1a1a1a; font-weight:700;">🧮 Kalkulator Endowment</h4>
        </div>
        """, unsafe_allow_html=True)
   
        ci1, ci2 = st.columns(2)
        with ci1:
            usia_x = st.number_input("Usia (x)", min_value=1, max_value=95, value=35, key="inp_x")
        with ci2:
            jangka_n = st.number_input("Jangka Waktu (n)", min_value=1, max_value=50, value=20, key="inp_n")
            
        ci3, ci4 = st.columns(2)
        with ci3:
            bunga_i = st.number_input("Tingkat Bunga (i %)", min_value=0.0, max_value=100.0, value=6.0, step=0.5, format="%.1f", key="inp_i")
        with ci4:
            manfaat_r = st.number_input("Manfaat / Uang Pertanggungan (Rp)", min_value=100000, value=200000000, step=10000000, key="inp_r")

        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        hitung_klik = st.button("Hitung Premi Bersih Tunggal", use_container_width=True, type="primary", key="btn_execute")

        # Kalkulasi Aktuaria Konsep Hukum De Moivre
        omega = 100
        v = 1 / (1 + (bunga_i / 100))
        
        if usia_x + jangka_n >= omega:
            st.error("Batas umur kombinasi melebihi tabel simulasi De Moivre (100 tahun).")
            ax_berjangka, nex_murni, premi_bersih = 0.0, 0.0, 0.0
        else:
            # Pure Endowment (nE_x)
            n_p_x = (omega - usia_x - jangka_n) / (omega - usia_x)
            nex_murni = (v ** jangka_n) * n_p_x
            
            # Asuransi Jiwa Berjangka (A^1_x:n|)
            ax_berjangka = 0.0
            for t in range(int(jangka_n)):
                t_p_x = (omega - usia_x - t) / (omega - usia_x)
                q_x_plus_t = 1 / (omega - usia_x - t)
                ax_berjangka += (v ** (t + 1)) * t_p_x * q_x_plus_t
                
            premi_bersih = manfaat_r * (ax_berjangka + nex_murni)

        if hitung_klik:
            simpan_riwayat(user["id"], "Endowment", f"Dwiguna Murni thn - x={usia_x}", f"Rp {premi_bersih:,.0f}")
            st.toast("Kalkulasi sukses disimpan!", icon="✨")

        # Tampilan 2 Komponen (Warna Merah Muda & Hijau Daun Estetik)
        co1, co2 = st.columns(2)
        with co1:
            st.markdown(f"""
            <div style="text-align:center; background-color:#FBEAF0; border:1px solid #ED93B1; padding:12px; border-radius:10px;">
                <small style="color:#993556; font-weight:600; font-size:12px;">A<sup>1</sup><sub>x:n|</sub> (Jiwa Berjangka)</small>
                <h4 style="margin:5px 0 0 0; color:#993556; font-size:18px; font-weight:700;">{ax_berjangka:.4f}</h4>
            </div>
            """, unsafe_allow_html=True)
        with co2:
            st.markdown(f"""
            <div style="text-align:center; background-color:#EAF3DE; border:1px solid #97C459; padding:12px; border-radius:10px;">
                <small style="color:#3B6D11; font-weight:600; font-size:12px;"><sub>n</sub>E<sub>x</sub> (Pure Endowment)</small>
                <h4 style="margin:5px 0 0 0; color:#3B6D11; font-size:18px; font-weight:700;">{nex_murni:.4f}</h4>
            </div>
            """, unsafe_allow_html=True)


        st.markdown(f"""
        <div style="text-align:center; background: linear-gradient(135deg, #993556, #802844); color:white; padding:16px; border-radius:10px; margin-top:12px; box-shadow: 0 4px 10px rgba(153,53,86,0.2);">
            <small style="opacity:0.9; font-weight:500; letter-spacing:0.3px;">TOTAL PREMI BERSIH TUNGGAL (A<sub>x:n|</sub>)</small>
            <h2 style="margin:5px 0 0 0; font-weight:700; font-size:26px;">Rp {premi_bersih:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col_grafik:
        st.markdown("""
        <div class="premium-card" style="height: 100%;">
            <span style="background-color:#3B6D11; color:white; padding:3px 9px; border-radius:6px; font-size:11px; font-weight:600;">Komparasi</span>
            <h4 style="margin-top:10px; margin-bottom:5px; color:#1a1a1a; font-weight:700;">⚖️ Diskrit vs Kontinu</h4>
            <p style="font-size:12px; color:#666; margin-bottom:15px;">Perbandingan tren premi berjangka 10 tahun per kelompok usia awal</p>
        """, unsafe_allow_html=True)
        
        # Generate Data Batang Horizontal Sesuai Draf Gambar Anda
        chart_data = pd.DataFrame({
            'Usia': ['Usia 30', 'Usia 30', 'Usia 45', 'Usia 45', 'Usia 60', 'Usia 60'],
            'Nilai Premi': [0.0156, 0.0163, 0.0324, 0.0341, 0.1457, 0.1489],
            'Metode': ['Diskrit', 'Kontinu', 'Diskrit', 'Kontinu', 'Diskrit', 'Kontinu']
        })
        
        fig = px.bar(
            chart_data, 
            y='Usia', 
            x='Nilai Premi', 
            color='Metode', 
            barmode='group',
            orientation='h',
            color_discrete_map={'Diskrit': '#D4537E', 'Kontinu': '#639922'},
            height=255
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            xaxis_title=None, yaxis_title=None,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. TABEL RIWAYAT DI BAGIAN BAWAH
    st.markdown("<h4 style='font-weight:700; color:#1a1a1a; margin-bottom:12px;'>Riwayat kalkulasi terbaru</h4>", unsafe_allow_html=True)
    riwayat_tampil = ambil_riwayat(user["id"], limit=3)

    if not riwayat_tampil:
        st.markdown(f"""
        <div class="rw-item">
            <div class="rw-icon rw-icon-p">🪙</div>
            <div class="rw-info"><div class="rw-name">Endowment Murni 15 tahun - x=30</div><div class="rw-date">Hari ini</div></div>
            <div class="rw-val">Rp 39.156.000</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for r in riwayat_tampil:
            st.markdown(f"""
            <div class="rw-item">
                <div class="rw-icon rw-icon-p">📊</div>
                <div class="rw-info">
                    <div class="rw-name">{r['deskripsi']}</div>
                    <div class="rw-date">Modul: {r['fitur']}</div>
                </div>
                <div class="rw-val" style="color:#993556; font-weight:700;">{r['hasil']}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CONTROL LOGIC GATEWAY
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:
    if st.session_state.halaman_auth == "register":
        halaman_register()
    else:
        halaman_login()
else:
    aplikasi_utama()
