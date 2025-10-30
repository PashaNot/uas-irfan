"""
Aplikasi Hitung Nilai Mahasiswa
Universitas Nurdin Hamzah
UAS Pemrograman Berbasis Platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
import os
from datetime import datetime

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="Aplikasi Hitung Nilai Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KONEKSI SUPABASE ====================
@st.cache_resource
def init_supabase() -> Client:
    """
    Inisialisasi koneksi ke Supabase
    Menggunakan st.secrets untuk deployment di Streamlit Cloud
    """
    try:
        # Untuk Streamlit Cloud, gunakan st.secrets
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"Gagal koneksi ke Supabase: {e}")
        st.info("Pastikan SUPABASE_URL dan SUPABASE_KEY sudah diset di Streamlit Secrets")
        return None

supabase = init_supabase()

# ==================== FUNGSI UTILITY ====================
def hitung_nilai_akhir(tugas: float, uts: float, uas: float) -> float:
    """
    Menghitung nilai akhir berdasarkan bobot:
    - Tugas: 30%
    - UTS: 30%
    - UAS: 40%
    """
    return (0.3 * tugas) + (0.3 * uts) + (0.4 * uas)

def konversi_nilai_huruf(nilai_akhir: float) -> tuple:
    """
    Konversi nilai angka ke huruf dan predikat
    Returns: (huruf, predikat)
    """
    if nilai_akhir >= 85:
        return ("A", "Sangat Baik")
    elif nilai_akhir >= 70:
        return ("B", "Baik")
    elif nilai_akhir >= 60:
        return ("C", "Cukup")
    elif nilai_akhir >= 50:
        return ("D", "Kurang")
    else:
        return ("E", "Gagal")

def simpan_data_mahasiswa(data: dict) -> bool:
    """
    Menyimpan data mahasiswa ke Supabase
    """
    try:
        response = supabase.table("nilai_mahasiswa").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")
        return False

def ambil_semua_data() -> pd.DataFrame:
    """
    Mengambil semua data dari Supabase
    """
    try:
        response = supabase.table("nilai_mahasiswa").select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

def hapus_data(id_data: int) -> bool:
    """
    Menghapus data berdasarkan ID
    """
    try:
        response = supabase.table("nilai_mahasiswa").delete().eq("id", id_data).execute()
        return True
    except Exception as e:
        st.error(f"Gagal menghapus data: {e}")
        return False

# ==================== STYLING CSS ====================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
st.sidebar.title("🎓 Navigation")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Pilih Menu:",
    ["🏠 HOME", "📝 INPUT NILAI", "📊 REKAPITULASI NILAI", "📈 STATISTIK NILAI"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Universitas Nurdin Hamzah**  
UAS Pemrograman Berbasis Platform  
Tahun 2025
""")

# ==================== HALAMAN HOME ====================
if menu == "🏠 HOME":
    st.markdown("""
    <div class="main-header">
        <h1>🎓 APLIKASI HITUNG NILAI MAHASISWA</h1>
        <p style="font-size: 1.2rem;">Universitas Nurdin Hamzah</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Selamat Datang! 👋")
    st.markdown("""
    Aplikasi ini dirancang untuk memudahkan pengelolaan dan perhitungan nilai mahasiswa 
    secara otomatis dengan fitur lengkap dan terintegrasi dengan database cloud.
    """)
    
    # Fitur Utama
    st.markdown("### ✨ Fitur Utama")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>📝 Input Nilai Mahasiswa</h4>
            <p>Input data mahasiswa lengkap dengan NIM, Program Studi, Semester, 
            dan nilai Tugas, UTS, UAS dengan validasi otomatis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🧮 Perhitungan Otomatis</h4>
            <p>Sistem menghitung nilai akhir dengan bobot: Tugas (30%), UTS (30%), 
            UAS (40%) dan konversi ke nilai huruf (A-E) beserta predikat.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>📊 Rekapitulasi Data</h4>
            <p>Tampilkan semua data mahasiswa dalam tabel interaktif dengan fitur 
            ekspor ke CSV dan hapus data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>📈 Statistik & Grafik</h4>
            <p>Analisis rata-rata nilai per Program Studi dengan visualisasi 
            grafik yang interaktif dan informatif.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Informasi Teknis
    st.markdown("---")
    st.markdown("### 🔧 Teknologi yang Digunakan")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Framework**  \n🐍 Python Streamlit")
    with col2:
        st.info("**Database**  \n☁️ Supabase Cloud")
    with col3:
        st.info("**Hosting**  \n🚀 Streamlit.io")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            <strong>Dibuat oleh: [M. Irfan Rahman] </strong>
        </p>
        <p style="color: #6c757d;">
            NIM: [24111007] | Program Studi: [Sistem Informasi]
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== HALAMAN INPUT NILAI ====================
elif menu == "📝 INPUT NILAI":
    st.markdown("""
    <div class="main-header">
        <h1>📝 INPUT NILAI MAHASISWA</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if supabase is None:
        st.error("⚠️ Koneksi database tidak tersedia. Periksa konfigurasi Supabase.")
        st.stop()
    
    # Form Input
    with st.form("form_input_nilai", clear_on_submit=True):
        st.subheader("Data Mahasiswa")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Mahasiswa *", placeholder="Contoh: Budi Santoso")
            nim = st.text_input("NIM *", placeholder="Contoh: 2021001")
            prodi = st.selectbox("Program Studi *", ["SI", "TI", "Teknosi"])
        
        with col2:
            semester = st.selectbox("Semester *", list(range(1, 9)))
            st.write("")  # Spacer
            st.write("")  # Spacer
        
        st.markdown("---")
        st.subheader("Input Nilai")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nilai_tugas = st.number_input("Nilai Tugas (0-100) *", 
                                         min_value=0.0, max_value=100.0, 
                                         value=0.0, step=0.5)
        with col2:
            nilai_uts = st.number_input("Nilai UTS (0-100) *", 
                                       min_value=0.0, max_value=100.0, 
                                       value=0.0, step=0.5)
        with col3:
            nilai_uas = st.number_input("Nilai UAS (0-100) *", 
                                       min_value=0.0, max_value=100.0, 
                                       value=0.0, step=0.5)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("🧮 Hitung & Simpan", use_container_width=True, type="primary")
        with col2:
            reset = st.form_submit_button("🔄 Reset", use_container_width=True)
    
    # Proses Submit
    if submit:
        # Validasi
        if not nama or not nim:
            st.error("❌ Nama dan NIM wajib diisi!")
        elif nilai_tugas == 0 and nilai_uts == 0 and nilai_uas == 0:
            st.warning("⚠️ Minimal satu nilai harus diisi!")
        else:
            # Hitung nilai akhir
            nilai_akhir = hitung_nilai_akhir(nilai_tugas, nilai_uts, nilai_uas)
            nilai_huruf, predikat = konversi_nilai_huruf(nilai_akhir)
            
            # Tampilkan hasil perhitungan
            st.markdown("### 🎯 Hasil Perhitungan")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <h3 style="color: #667eea;">{nilai_akhir:.2f}</h3>
                    <p>Nilai Akhir</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <h3 style="color: #764ba2;">{nilai_huruf}</h3>
                    <p>Nilai Huruf</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <h3 style="color: #28a745;">{predikat}</h3>
                    <p>Predikat</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <h3 style="color: #ffc107;">{prodi}</h3>
                    <p>Program Studi</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Simpan ke database
            data_mahasiswa = {
                "nama": nama,
                "nim": nim,
                "prodi": prodi,
                "semester": semester,
                "nilai_tugas": nilai_tugas,
                "nilai_uts": nilai_uts,
                "nilai_uas": nilai_uas,
                "nilai_akhir": round(nilai_akhir, 2),
                "nilai_huruf": nilai_huruf,
                "predikat": predikat,
                "tanggal_input": datetime.now().isoformat()
            }
            
            with st.spinner("Menyimpan data ke database..."):
                if simpan_data_mahasiswa(data_mahasiswa):
                    st.markdown("""
                    <div class="success-box">
                        <h4>✅ Data Berhasil Disimpan!</h4>
                        <p>Data mahasiswa telah tersimpan ke database Supabase.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()

# ==================== HALAMAN REKAPITULASI NILAI ====================
elif menu == "📊 REKAPITULASI NILAI":
    st.markdown("""
    <div class="main-header">
        <h1>📊 REKAPITULASI NILAI MAHASISWA</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if supabase is None:
        st.error("⚠️ Koneksi database tidak tersedia. Periksa konfigurasi Supabase.")
        st.stop()
    
    # Ambil data
    with st.spinner("Memuat data dari database..."):
        df = ambil_semua_data()
    
    if df.empty:
        st.info("📭 Belum ada data mahasiswa. Silakan input data terlebih dahulu.")
    else:
        # Statistik Ringkas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Mahasiswa", len(df))
        with col2:
            st.metric("📚 Rata-rata Nilai", f"{df['nilai_akhir'].mean():.2f}")
        with col3:
            st.metric("⭐ Nilai Tertinggi", f"{df['nilai_akhir'].max():.2f}")
        with col4:
            st.metric("📉 Nilai Terendah", f"{df['nilai_akhir'].min():.2f}")
        
        st.markdown("---")
        
        # Filter
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_prodi = st.multiselect("Filter Program Studi", 
                                         options=df['prodi'].unique(),
                                         default=df['prodi'].unique())
        with col2:
            filter_semester = st.multiselect("Filter Semester",
                                            options=sorted(df['semester'].unique()),
                                            default=sorted(df['semester'].unique()))
        with col3:
            filter_predikat = st.multiselect("Filter Predikat",
                                            options=df['predikat'].unique(),
                                            default=df['predikat'].unique())
        
        # Apply filter
        df_filtered = df[
            (df['prodi'].isin(filter_prodi)) & 
            (df['semester'].isin(filter_semester)) &
            (df['predikat'].isin(filter_predikat))
        ]
        
        st.markdown(f"### 📋 Data Mahasiswa ({len(df_filtered)} dari {len(df)} data)")
        
        # Kolom yang ditampilkan
        columns_display = ['nama', 'nim', 'prodi', 'semester', 'nilai_tugas', 
                          'nilai_uts', 'nilai_uas', 'nilai_akhir', 'nilai_huruf', 'predikat']
        
        # Tampilkan tabel
        st.dataframe(
            df_filtered[columns_display],
            use_container_width=True,
            hide_index=True
        )
        
        # Aksi
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # Ekspor ke CSV
            csv = df_filtered[columns_display].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Ekspor ke CSV",
                data=csv,
                file_name=f"rekap_nilai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
        
        # Hapus data (admin only)
        with st.expander("⚠️ Hapus Data (Admin)"):
            st.warning("Fitur ini hanya untuk admin. Data yang dihapus tidak dapat dikembalikan!")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                id_hapus = st.number_input("Masukkan ID data yang akan dihapus", 
                                          min_value=1, step=1)
            with col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Hapus Data", type="secondary"):
                    if hapus_data(id_hapus):
                        st.success(f"✅ Data ID {id_hapus} berhasil dihapus!")
                        st.rerun()

# ==================== HALAMAN STATISTIK NILAI ====================
elif menu == "📈 STATISTIK NILAI":
    st.markdown("""
    <div class="main-header">
        <h1>📈 STATISTIK & ANALISIS NILAI</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if supabase is None:
        st.error("⚠️ Koneksi database tidak tersedia. Periksa konfigurasi Supabase.")
        st.stop()
    
    # Ambil data
    with st.spinner("Memuat data dari database..."):
        df = ambil_semua_data()
    
    if df.empty:
        st.info("📭 Belum ada data mahasiswa. Silakan input data terlebih dahulu.")
    else:
        # Tab untuk berbagai statistik
        tab1, tab2, tab3 = st.tabs(["📊 Per Program Studi", "📅 Per Semester", "🎯 Distribusi Nilai"])
        
        # TAB 1: Statistik Per Prodi
        with tab1:
            st.subheader("Rata-rata Nilai per Program Studi")
            
            # Hitung rata-rata per prodi
            avg_prodi = df.groupby('prodi')['nilai_akhir'].mean().reset_index()
            avg_prodi.columns = ['Program Studi', 'Rata-rata Nilai']
            avg_prodi = avg_prodi.sort_values('Rata-rata Nilai', ascending=False)
            
            # Tampilkan dalam card
            cols = st.columns(len(avg_prodi))
            for idx, (col, row) in enumerate(zip(cols, avg_prodi.itertuples())):
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                        <h2 style="color: #667eea;">{row[1]}</h2>
                        <h3>{row[2]:.2f}</h3>
                        <p>Rata-rata Nilai</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Grafik batang
            fig = px.bar(avg_prodi, x='Program Studi', y='Rata-rata Nilai',
                        title='Grafik Rata-rata Nilai per Program Studi',
                        color='Rata-rata Nilai',
                        color_continuous_scale='Viridis',
                        text='Rata-rata Nilai')
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabel detail
            st.markdown("### 📋 Detail Statistik per Program Studi")
            detail_prodi = df.groupby('prodi').agg({
                'nilai_akhir': ['count', 'mean', 'min', 'max', 'std']
            }).round(2)
            detail_prodi.columns = ['Jumlah Mahasiswa', 'Rata-rata', 'Min', 'Max', 'Std Deviasi']
            st.dataframe(detail_prodi, use_container_width=True)
        
        # TAB 2: Statistik Per Semester
        with tab2:
            st.subheader("Rata-rata Nilai per Semester")
            
            # Hitung rata-rata per semester
            avg_semester = df.groupby('semester')['nilai_akhir'].mean().reset_index()
            avg_semester.columns = ['Semester', 'Rata-rata Nilai']
            avg_semester = avg_semester.sort_values('Semester')
            
            # Grafik garis
            fig = px.line(avg_semester, x='Semester', y='Rata-rata Nilai',
                         title='Tren Rata-rata Nilai per Semester',
                         markers=True,
                         line_shape='spline')
            fig.update_traces(line_color='#667eea', line_width=3, 
                            marker=dict(size=10, color='#764ba2'))
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Heatmap prodi vs semester
            st.markdown("### 🔥 Heatmap: Program Studi vs Semester")
            pivot_data = df.pivot_table(values='nilai_akhir', 
                                       index='prodi', 
                                       columns='semester', 
                                       aggfunc='mean')
            fig = px.imshow(pivot_data, 
                           labels=dict(x="Semester", y="Program Studi", color="Nilai"),
                           color_continuous_scale='RdYlGn',
                           aspect="auto")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # TAB 3: Distribusi Nilai
        with tab3:
            st.subheader("Distribusi Nilai Huruf")
            
            # Hitung distribusi nilai huruf
            dist_huruf = df['nilai_huruf'].value_counts().sort_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig = px.pie(values=dist_huruf.values, 
                            names=dist_huruf.index,
                            title='Distribusi Nilai Huruf',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Bar chart
                fig = px.bar(x=dist_huruf.index, y=dist_huruf.values,
                            title='Jumlah Mahasiswa per Nilai Huruf',
                            labels={'x': 'Nilai Huruf', 'y': 'Jumlah Mahasiswa'},
                            color=dist_huruf.values,
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            
            # Histogram nilai akhir
            st.markdown("### 📊 Histogram Distribusi Nilai Akhir")
            fig = px.histogram(df, x='nilai_akhir', nbins=20,
                             title='Distribusi Nilai Akhir Mahasiswa',
                             labels={'nilai_akhir': 'Nilai Akhir', 'count': 'Frekuensi'},
                             color_discrete_sequence=['#667eea'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistik deskriptif
            st.markdown("### 📈 Statistik Deskriptif")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Nilai Akhir:**")
                st.dataframe(df['nilai_akhir'].describe().round(2), use_container_width=True)
            
            with col2:
                st.write("**Distribusi Predikat:**")
                dist_predikat = df['predikat'].value_counts()
                st.dataframe(dist_predikat, use_container_width=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>© 2025 Universitas Nurdin Hamzah | Aplikasi Hitung Nilai Mahasiswa v1.0</p>
    <p>Dibuat dengan ❤️ menggunakan Streamlit & Supabase</p>
</div>

""", unsafe_allow_html=True)
