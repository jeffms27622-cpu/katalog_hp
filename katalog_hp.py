import streamlit as st
import pandas as pd

# Konfigurasi Tampilan Mobile
st.set_page_config(page_title="Katalog PT Thea Theo", layout="centered")

# Custom CSS untuk tampilan kartu yang lebih modern di HP
st.markdown("""
    <style>
    .product-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin-bottom: 10px;
    }
    .price-text {
        color: #28a745;
        font-weight: bold;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Load Data
@st.cache_data
def load_data():
    # Mengacu pada file yang kamu unggah
    df = pd.read_csv("database_katalog.xlsx - Sheet1.csv")
    return df

df = load_data()

# --- HEADER ---
st.title("📦 Katalog Stationery")
st.caption(f"Menampilkan {len(df)} item produk")

# --- FITUR PENCARIAN & FILTER ---
search_query = st.text_input("🔍 Cari Produk...", placeholder="Contoh: Acco, Aqua, Joyko...")

# Filter Kategori (Otomatis dari data kamu)
categories = ["Semua Kategori"] + sorted(list(df['Kategori'].unique()))
selected_cat = st.selectbox("📁 Filter Kategori", categories)

# Logika Filter
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['Nama Barang'].str.contains(search_query, case=False, na=False)]
if selected_cat != "Semua Kategori":
    filtered_df = filtered_df[filtered_df['Kategori'] == selected_cat]

st.divider()

# --- TAMPILAN PRODUK ---
if filtered_df.empty:
    st.warning("Produk tidak ditemukan. Coba kata kunci lain.")
else:
    for _, row in filtered_df.iterrows():
        # Format Harga ke Rupiah
        harga_fmt = f"Rp {row['Harga']:,.0f}".replace(',', '.')
        
        # Tampilan Kartu Produk
        with st.container():
            st.markdown(f"""
            <div class="product-card">
                <small style="color: grey;">{row['Kategori']}</small>
                <div style="font-size: 1.1em; font-weight: bold; margin: 5px 0;">{row['Nama Barang']}</div>
                <div class="price-text">{harga_fmt} <span style="color: black; font-weight: normal; font-size: 0.8em;">/ {row['Satuan']}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tombol Share WhatsApp yang Praktis
            pesan_wa = f"Info Produk PT Thea Theo:\n\n*Nama:* {row['Nama Barang']}\n*Harga:* {harga_fmt} / {row['Satuan']}\n*Kategori:* {row['Kategori']}"
            link_wa = f"https://wa.me/?text={pesan_wa.replace(' ', '%20').replace('\n', '%0A')}"
            
            st.markdown(f"[![Bagikan ke WA](https://img.shields.io/badge/Kirim_Info_ke_WA-25D366?style=flat-square&logo=whatsapp)]({link_wa})")
            st.write("") # Spasi antar item

# Footer
st.markdown("---")
st.caption("Aplikasi Katalog Sales - PT Thea Theo Stationary")