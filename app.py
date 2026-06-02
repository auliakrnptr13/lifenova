import streamlit as st
from database import init_db, register_user, login_user, simpan_riwayat, ambil_riwayat
from styles import LIFENOVA_CSS

st.set_page_config(
    page_title="Life Nova - Platform Aktuaria Digital",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()
st.markdown(LIFENOVA_CSS, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "halaman_auth" not in st.session_state:
    st.session_state.halaman_auth = "login"
if "pesan_sukses_reg" not in st.session_state:
    st.session_state.pesan_sukses_reg = None

def navbar():
    user = st.session_state.user
    st.markdown(f"""
    <div class="lifenova-nav">
        <div class="brand">🌿 Life Nova</div>
        <div class="user-info">Halo, <strong>{user['nama']}</strong> &nbsp;·&nbsp; {user['email']}</div>
    </div>
    """, unsafe_allow_html=True)

def alert_sukses(pesan: str):
    st.markdown(f'<div class="alert-success">✓ &nbsp;{pesan}</div>', unsafe_allow_html=True)

def alert_error(pesan: str):
    st.markdown(f'<div class="alert-error">✕ &nbsp;{pesan}</div>', unsafe_allow_html=True)

def halaman_login():
    _, col_c, _ = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center; margin-top: 40px; margin-bottom:15px">
            <div style="width:60px;height:60px;border-radius:16px;background:#3B6D11;
                        display:inline-flex;align-items:center;justify-content:center;
                        font-size:32px;margin-bottom:12px;box-shadow: 0 4px 10px rgba(0,0,0,0.1)">🌿</div>
            <h2 style="margin:0;color:#3B6D11;font-size:26px;font-weight:700;">Life Nova</h2>
            <p style="margin:4px 0 0;color:#666;font-size:13px">Hitung premi & analisis survival aktuaria cerdas</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.pesan_sukses_reg:
            alert_sukses(st.session_state.pesan_sukses_reg)
            st.session_state.pesan_sukses_reg = None

        st.markdown("<h4 style='margin-bottom:15px;font-weight:600;'>Masuk ke Akun Anda</h4>", unsafe_allow_html=True)
        email_atau_username = st.text_input("Email atau Username", placeholder="Masukkan email atau username", key="login_id")
        password = st.text_input("Kata Sandi", type="password", placeholder="Masukkan kata sandi", key="login_pw")

        if st.button("Masuk Sekarang", key="btn_login", use_container_width=True):
            if not email_atau_username or not password:
                alert_error("Kolom email/username dan kata sandi tidak boleh kosong.")
            else:
                hasil = login_user(email_atau_username, password)
                if hasil["ok"]:
                    st.session_state.user = hasil["user"]
                    st.rerun()
                else:
                    alert_error(hasil["pesan"])

        st.markdown("<p style='text-align:center;margin-top:25px;margin-bottom:5px;font-size:13px;color:#666;'>Belum memiliki akun?</p>", unsafe_allow_html=True)
        if st.button("Daftar Akun Gratis →", key="ke_register", use_container_width=True):
            st.session_state.halaman_auth = "register"
            st.rerun()

def halaman_register():
    _, col_c, _ = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center; margin-top: 30px; margin-bottom:15px">
            <div style="width:60px;height:60px;border-radius:16px;background:#3B6D11;
                        display:inline-flex;align-items:center;justify-content:center;
                        font-size:32px;margin-bottom:12px;box-shadow: 0 4px 10px rgba(0,0,0,0.1)">🌿</div>
            <h2 style="margin:0;color:#3B6D11;font-size:26px;font-weight:700;">Life Nova</h2>
            <p style="margin:4px 0 0;color:#666;font-size:13px">Gabung sekarang untuk mulai simulasi kalkulasi</p>
        </div>
        """, unsafe_allow_html=True)

        nama = st.text_input("Nama Lengkap", placeholder="Contoh: Siti Aminah", key="reg_name")
        email = st.text_input("Alamat Email", placeholder="contoh@email.com", key="reg_mail")
        username = st.text_input("Username (Tanpa Spasi)", placeholder="sitiaminah", key="reg_user")
        password = st.text_input("Kata Sandi (Min 6 Karakter)", type="password", placeholder="Buat kata sandi", key="reg_pw")
        konfirmasi = st.text_input("Konfirmasi Kata Sandi", type="password", placeholder="Ulangi kata sandi", key="reg_cpw")

        if st.button("Daftar Sekarang", key="btn_register", use_container_width=True):
            if not all([nama, email, username, password, konfirmasi]):
                alert_error("Seluruh data pendaftaran wajib diisi.")
            elif " " in username:
                alert_error("Username tidak boleh mengandung spasi.")
            elif password != konfirmasi:
                alert_error("Konfirmasi kata sandi tidak cocok dengan kata sandi.")
            else:
                hasil = register_user(nama, email, username, password)
                if hasil["ok"]:
                    st.session_state.pesan_sukses_reg = f"Akun berhasil dibuat! Silakan masuk, {hasil['nama']}."
                    st.session_state.halaman_auth = "login"
                    st.rerun()
                else:
                    alert_error(hasil["pesan"])

        st.markdown("<p style='text-align:center;margin-top:25px;margin-bottom:5px;font-size:13px;color:#666;'>Sudah punya akun?</p>", unsafe_allow_html=True)
        if st.button("← Kembali ke Login", key="ke_login", use_container_width=True):
            st.session_state.halaman_auth = "login"
            st.rerun()

def halaman_dashboard():
    user = st.session_state.user
    navbar()

    st.markdown(f"""
    <div class="welcome-banner">
        <div class="wb-name">Selamat datang kembali di Life Nova, {user['nama']} 👋</div>
        <div class="wb-sub">ID Pengguna: @{user['username']} &nbsp;·&nbsp; Data terenkripsi aman</div>
    </div>
    """, unsafe_allow_html=True)

    col_space, col_logout = st.columns([5, 1])
    with col_logout:
        if st.button("Log Out ↩", key="btn_logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.halaman_auth = "login"
            st.rerun()

    riwayat = ambil_riwayat(user["id"], limit=50)
    total = len(riwayat)
    premi = sum(1 for r in riwayat if r["fitur"] == "Simulasi Premi")
    bandin = sum(1 for r in riwayat if r["fitur"] == "Bandingkan")
    peluang = sum(1 for r in riwayat if r["fitur"] == "Peluang Hidup")

    c1, c2, c3, c4 = st.columns(4)
    metric_data = [
        (c1, "TOTAL PERHITUNGAN", total, "Riwayat aman tersimpan", "delta-green"),
        (c2, "SIMULASI PREMI", premi, "Modul endowment", "delta-pink"),
        (c3, "PERBANDINGAN ASURANSI", bandin, "Diskrit vs Kontinu", "delta-green"),
        (c4, "ANALISIS SURVIVAL", peluang, "Peluang Hidup", "delta-green"),
    ]
    for col, label, val, delta, warna in metric_data:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">{label}</div>
                <div class="value">{val}</div>
                <div class="{warna}">● {delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><h3>Modul Aplikasi & Kalkulator Aktuaria</h3>", unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    fitur_list = [
        (fc1, "fc-icon-p", "🪙", "Simulasi Premi Tabungan", "Hitung besaran premi sekaligus untuk asuransi dwi guna berjangka.", "btn_fitur_premi"),
        (fc2, "fc-icon-g", "⚖️", "Bandingkan Produk", "Bandingkan anuitas hidup & kalkulasi premi kontinu versus diskrit.", "btn_fitur_bandin"),
        (fc3, "fc-icon-p", "💓", "Analisis Peluang Hidup", "Estimasi probabilitas survival seseorang berdasarkan Tabel Mortalitas.", "btn_fitur_peluang"),
        (fc4, "fc-icon-g", "📋", "Unduh Laporan PDF", "Ekspor lembar hasil simulasi perhitungan ke dalam dokumen PDF.", "btn_fitur_pdf"),
    ]
    for col, icon_cls, icon, judul, deskripsi, key in fitur_list:
        with col:
            st.markdown(f"""
            <div class="fitur-card">
                <div class="fc-icon {icon_cls}">{icon}</div>
                <h4>{judul}</h4>
                <p>{deskripsi}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Buka Modul", key=key, use_container_width=True)

    st.markdown("<br><h3>Aktivitas Perhitungan Terakhir</h3>", unsafe_allow_html=True)
    riwayat_tampil = ambil_riwayat(user["id"], limit=5)
    if not riwayat_tampil:
        st.markdown('<div style="text-align:center;padding:40px;color:#888;background:#fdfdfd;border-radius:12px;border:1px dashed #ddd;">Belum ada kalkulasi dilakukan.</div>', unsafe_allow_html=True)
    else:
        icon_map = {"Simulasi Premi": ("🪙", "rw-icon-p"), "Bandingkan": ("⚖️", "rw-icon-g"), "Peluang Hidup": ("💓", "rw-icon-p")}
        for r in riwayat_tampil:
            ikon, ikon_cls = icon_map.get(r["fitur"], ("📌", "rw-icon-g"))
            st.markdown(f"""
            <div class="rw-item">
                <div class="rw-icon {ikon_cls}">{ikon}</div>
                <div class="rw-info">
                    <div class="rw-name">{r['deskripsi']}</div>
                    <div class="rw-date">Waktu input: {r['created_at'][:16]}</div>
                </div>
                <div class="rw-val">{r['hasil']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🧪 Sandbox Uji Coba Pengembang"):
        if st.button("Injeksikan Contoh Data Riwayat"):
            simpan_riwayat(user["id"], "Simulasi Premi", "Premi Tunggal Netto Endowment Usia 25 tahun, n=20 tahun", "Rp 42.500.000")
            simpan_riwayat(user["id"], "Bandingkan", "Kalkulasi Selisih Anuitas Diskrit vs Kontinu (i=5%)", "Selisih Efisiensi 3.25%")
            simpan_riwayat(user["id"], "Peluang Hidup", "Analisis Probabilitas Survival mencapai umur 80 tahun", "Peluang: 68.4%")
            st.success("Sampel riwayat data berhasil dimasukkan!")
            st.rerun()

if st.session_state.user is None:
    if st.session_state.halaman_auth == "register": halaman_register()
    else: halaman_login()
else: halaman_dashboard()
