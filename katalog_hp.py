import streamlit as st
import pandas as pd

# 1. CONFIG & BRANDING
st.set_page_config(page_title="Thea Theo Digital", layout="centered", page_icon="📝")

# CSS UNTUK TAMPILAN MEWAH (GLASSMORPHISM)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main { background-color: #fcfcfc; }

    /* Header Gradasi */
    .header-text {
        background: linear-gradient(135deg, #1C448E 0%, #FF4B4B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Kartu Produk Modern */
    .product-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.08);
    }

    .category-badge {
        background: #f1f5f9;
        color: #64748b;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .price-text {
        color: #1C448E;
        font-weight: 800;
        font-size: 1.3rem;
        margin-top: 10px;
    }

    .unit-label {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 400;
    }

    /* Tombol melengkung */
    .stButton>button {
        border-radius: 12px;
        border: none;
        background: #1C448E;
        color: white;
        transition: 0.3s;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LOAD DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("database_katalog.xlsx")
        return df
    except Exception as e:
        st.error(f"File database_katalog.xlsx tidak ditemukan. Error: {e}")
        return pd.DataFrame()

df = load_data()

# 3. SIDEBAR & KERANJANG
if 'cart' not in st.session_state:
    st.session_state.cart = []

# HEADER
st.markdown('<h1 class="header-text">THEA & THEO</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Premium Stationary Catalog</p>", unsafe_allow_html=True)

# 4. SEARCH & FILTER (Dibuat ramping)
col_search, col_filter = st.columns([2, 1])
with col_search:
    search_query = st.text_input("🔍 Cari Barang", placeholder="Tulis nama barang...", label_visibility="collapsed")
with col_filter:
    if not df.empty and 'Kategori' in df.columns:
        cats = ["Semua"] + sorted(list(df['Kategori'].dropna().unique()))
        selected_cat = st.selectbox("Kategori", cats, label_visibility="collapsed")
    else:
        selected_cat = "Semua"

# FILTER LOGIC
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['Nama Barang'].str.contains(search_query, case=False, na=False)]
if selected_cat != "Semua":
    filtered_df = filtered_df[filtered_df['Kategori'] == selected_cat]

st.write("")

# 5. DISPLAY PRODUK
if filtered_df.empty:
    st.info("Produk tidak ditemukan.")
else:
    for i, row in filtered_df.iterrows():
        harga_raw = row['Harga']
        harga_fmt = f"Rp {harga_raw:,.0f}".replace(',', '.')
        
        with st.container():
            st.markdown(f"""
            <div class="product-card">
                <span class="category-badge">{row['Kategori']}</span>
                <div style="font-size: 1.15rem; font-weight: 700; margin-top: 8px; color: #1e293b;">{row['Nama Barang']}</div>
                <div class="price-text">{harga_fmt} <span class="unit-label">/ {row['Satuan']}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tombol interaktif
            if st.button(f"➕ Masukkan Daftar Penawaran", key=f"add_{i}"):
                item = {"nama": row['Nama Barang'], "harga": harga_fmt, "satuan": row['Satuan']}
                st.session_state.cart.append(item)
                st.toast(f"✅ {row['Nama Barang']} ditambah!")

# 6. FLOATING SUMMARY (KERANJANG)
if st.session_state.cart:
    st.markdown("---")
    with st.expander(f"📋 Daftar Penawaran ({len(st.session_state.cart)} Item)", expanded=True):
        pesan_wa = "Halo PT Thea Theo, saya tertarik dengan daftar produk ini:\n\n"
        for idx, item in enumerate(st.session_state.cart):
            st.write(f"{idx+1}. **{item['nama']}** ({item['harga']}/{item['satuan']})")
            pesan_wa += f"{idx+1}. {item['nama']} ({item['harga']}/{item['satuan']})\n"
        
        pesan_wa += "\nMohon info ketersediaan stoknya. Terima kasih!"
        link_wa = f"https://wa.me/?text={pesan_wa.replace(' ', '%20').replace('\n', '%0A')}"
        
        col_wa, col_del = st.columns([3, 1])
        with col_wa:
            st.markdown(f"""<a href="{link_wa}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer;">
                    🚀 KIRIM DAFTAR KE WHATSAPP
                </button></a>""", unsafe_allow_html=True)
        with col_del:
            if st.button("🗑️ Reset"):
                st.session_state.cart = []
                st.rerun()

# FOOTER
st.markdown("<br><p style='text-align: center; font-size: 0.8rem; color: #94a3b8;'>E-Catalog by Asin | PT Thea Theo Stationary</p>", unsafe_allow_html=True)
