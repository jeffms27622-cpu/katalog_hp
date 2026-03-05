import streamlit as st
import pandas as pd

# Konfigurasi Tampilan Mobile
st.set_page_config(page_title="Katalog PT Thea Theo", layout="centered")

# Custom CSS untuk tampilan kartu di HP
st.markdown("""
    <style>
    .product-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #007bff;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .price-text {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2em;
        margin-top: 5px;
    }
    .unit-text {
        color: #6c757d;
        font-size: 0.8em;
        font-weight: normal;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Fungsi Load Data dengan Proteksi Error
@st.cache_data
def load_data():
    try:
        # Membaca langsung dari file Excel
        df = pd.read_excel("database_katalog.xlsx")
        return df
    except FileNotFoundError:
        st.error("Gagal: File 'database_katalog.xlsx' tidak ditemukan di GitHub.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca data: {e}")
        return pd.DataFrame()

df = load_data()

# --- HEADER ---
st.title("📱 Katalog Digital")
st.markdown("**PT Thea Theo Stationary**")

if not df.empty:
    st.caption(f"Menampilkan {len(df)} item produk")

    # --- FITUR PENCARIAN & FILTER ---
    search_query = st.text_input("🔍 Cari Nama Barang atau Merk...", placeholder="Ketik di sini...")

    # Ambil kategori unik untuk filter
    if 'Kategori' in df.columns:
        categories = ["Semua Kategori"] + sorted(list(df['Kategori'].dropna().unique()))
        selected_cat = st.selectbox("📁 Filter Kategori", categories)
    else:
        selected_cat = "Semua Kategori"

    # --- LOGIKA FILTER ---
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[filtered_df['Nama Barang'].astype(str).str.contains(search_query, case=False, na=False)]
    
    if selected_cat != "Semua Kategori":
        filtered_df = filtered_df[filtered_df['Kategori'] == selected_cat]

    st.divider()

    # --- TAMPILAN PRODUK ---
    if filtered_df.empty:
        st.warning("Produk tidak ditemukan. Coba kata kunci lain.")
    else:
        for _, row in filtered_df.iterrows():
            # Format Harga ke Rupiah
            try:
                harga_val = float(row['Harga'])
                harga_fmt = f"Rp {harga_val:,.0f}".replace(',', '.')
            except:
                harga_fmt = "Hubungi Sales"
            
            satuan = row['Satuan'] if 'Satuan' in row else "Unit"
            kategori = row['Kategori'] if 'Kategori' in row else "General"
            
            # Tampilan Kartu Produk
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <small style="color: #007bff; font-weight: bold;">{kategori}</small>
                    <div style="font-size: 1.1em; font-weight: 600; margin: 5px 0; color: #333;">{row['Nama Barang']}</div>
                    <div class="price-text">{harga_fmt} <span class="unit-text">/ {satuan}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tombol Share WhatsApp
                pesan_wa = (
                    f"Halo PT Thea Theo, saya tertarik dengan produk ini:\n\n"
                    f"*Barang:* {row['Nama Barang']}\n"
                    f"*Harga:* {harga_fmt} / {satuan}\n"
                    f"*Kategori:* {kategori}"
                )
                link_wa = f"https://wa.me/?text={pesan_wa.replace(' ', '%20').replace('\n', '%0A')}"
                
                st.markdown(f"[![Bagikan ke WA](https://img.shields.io/badge/Share_ke_WhatsApp-25D366?style=for-the-badge&logo=whatsapp)]({link_wa})")
                st.write("") # Spasi tambahan

else:
    st.info("Silakan upload file 'database_katalog.xlsx' ke repository GitHub Anda.")

# Footer
st.markdown("---")
st.caption("© 2026 PT Thea Theo Stationary | Sales Tool v1.2")
