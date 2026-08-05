"""Portofolio interaktif Anita Tiara Sani - Admin Warehouse & Admin Umum."""

import streamlit as st
import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from data.generate_data import load_all_data
from utils.formulas import (
    vlookup, vlookup_batch, index_match, index_match_batch,
    nested_if, status_stok, kategori_harga,
    pivot_summary, pivot_multi, hitung_laba_rugi, hitung_neraca,
    hitung_arus_kas, hitung_kpi_warehouse, format_rupiah, format_persen,
    format_angka
)
from utils.charts import (
    bar_chart, pie_chart, line_chart, multi_line_chart, histogram,
    gauge_chart, scatter_chart, treemap, waterfall_chart, stacked_bar_chart,
    kpi_card, COLORS, GRADIENT
)

st.set_page_config(
    page_title="Anita Tiara Sani | Portofolio Admin",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inject_css():
    st.markdown("""
    <style>
    :root {
        --bg: #070b16;
        --card: #0d1428;
        --cyan: #00f0ff;
        --magenta: #ff2ec4;
        --purple: #8b5cf6;
        --green: #00ffa3;
        --text: #eef4ff;
        --muted: #93a4c3;
    }

    .stApp {
        background: linear-gradient(135deg, #070b16 0%, #0d1428 50%, #0a0f1f 100%);
        color: var(--text);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1428 0%, #0a0f1f 100%);
        border-right: 1px solid rgba(0, 240, 255, 0.15);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--cyan);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--text);
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        color: var(--cyan);
    }

    .stRadio > div { gap: 8px; }
    .stRadio label {
        display: flex;
        align-items: center;
        padding: 10px 14px;
        border-radius: 10px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    .stRadio label:hover {
        background: rgba(0, 240, 255, 0.08);
        border-color: rgba(0, 240, 255, 0.3);
    }
    .stRadio label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(90deg, rgba(0,240,255,0.12), rgba(255,46,196,0.12));
        border-color: var(--cyan);
        box-shadow: 0 0 12px rgba(0,240,255,0.2);
    }

    h1, h2, h3 {
        font-family: 'Sora', 'Inter', sans-serif;
        color: var(--text);
    }
    .gradient-text {
        background: linear-gradient(90deg, var(--cyan), var(--magenta), var(--purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(0,240,255,0.08), rgba(255,46,196,0.08));
        border: 1px solid rgba(0,240,255,0.2);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,240,255,0.2);
    }
    div[data-testid="stMetric"] label { color: var(--muted); font-size: 0.85rem; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--cyan); font-weight: 700; }

    .custom-card {
        background: linear-gradient(135deg, rgba(13,20,40,0.9), rgba(10,15,31,0.9));
        border: 1px solid rgba(0,240,255,0.15);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(0,240,255,0.15);
    }
    .custom-card h3 { color: var(--cyan); margin-bottom: 8px; }
    .custom-card p { color: var(--muted); line-height: 1.7; }

    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin: 3px;
        border: 1px solid;
    }
    .badge-cyan { color: var(--cyan); border-color: var(--cyan); background: rgba(0,240,255,0.08); }
    .badge-magenta { color: var(--magenta); border-color: var(--magenta); background: rgba(255,46,196,0.08); }
    .badge-purple { color: var(--purple); border-color: var(--purple); background: rgba(139,92,246,0.08); }
    .badge-green { color: var(--green); border-color: var(--green); background: rgba(0,255,163,0.08); }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0,240,255,0.1);
    }
    .stDataFrame [data-testid="stDataFrame"] { background: rgba(13,20,40,0.6); }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--cyan), var(--magenta), transparent);
        margin: 20px 0;
    }

    details {
        background: rgba(13,20,40,0.6);
        border: 1px solid rgba(0,240,255,0.15);
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 10px;
    }
    details summary { color: var(--cyan); font-weight: 600; cursor: pointer; }

    .footer {
        text-align: center;
        padding: 20px;
        color: var(--muted);
        font-size: 0.85rem;
        border-top: 1px solid rgba(0,240,255,0.1);
        margin-top: 40px;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--cyan), var(--magenta));
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, var(--magenta), var(--cyan)); }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(13,20,40,0.5);
        border-radius: 12px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 18px; color: var(--muted); }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0,240,255,0.15), rgba(255,46,196,0.15));
        color: var(--cyan) !important;
    }

    .contact-btn {
        display: inline-block;
        padding: 10px 18px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        border: 1px solid;
        transition: all 0.3s ease;
    }
    .contact-btn:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(0,240,255,0.15);margin-bottom:20px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#00f0ff,#ff2ec4);display:flex;align-items:center;justify-content:center;font-size:1.4rem;">AT</div>
            <div>
                <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:1.2rem;color:#eef4ff;">Anita<span style="color:#ff2ec4;">.</span>dev</div>
                <div style="font-size:0.75rem;color:#93a4c3;">Admin Warehouse &amp; Admin Umum</div>
            </div>
        </div>
        <div style="font-size:0.8rem;color:#93a4c3;background:rgba(0,240,255,0.08);padding:6px 16px;border-radius:20px;border:1px solid rgba(0,240,255,0.3);">
            Babelan, Bekasi, Jawa Barat
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_beranda():
    st.markdown("## Hallo, Saya <span class='gradient-text'>Anita Tiara Sani</span>", unsafe_allow_html=True)
    st.markdown("### Admin Warehouse & Admin Umum | Data & Finance Enthusiast")
    st.markdown("""
    <div class="custom-card">
        <p>Profesional administrasi dengan pengalaman <b>2 tahun+</b> di bidang tata kelola logistik dan operasional manufaktur. 
        Terbiasa memproses <b>data entry bervolume tinggi</b> (1.000+ item) dan menyusun <b>laporan inventaris &amp; keuangan 
        yang akurat</b> memakai <b>Advanced MS Excel</b> (VLOOKUP, Pivot Table, IF) plus tools analisis data modern untuk 
        dashboard interaktif.</p>
        <p>Detail-oriented, terbiasa mengelola dokumen operasional, dan berkoordinasi dengan vendor untuk menjamin kelancaran 
        logistik. Siap membantu efisiensi administrasi perusahaan Anda.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Keahlian Teknis")
        tech_skills = {
            "Microsoft Excel (VLOOKUP, Pivot Table, IF)": 95,
            "Data Entry & Manajemen Data": 95,
            "Manajemen Inventaris": 92,
            "Laporan Keuangan & Akuntansi": 85,
            "Analisis Data & Dashboard": 80,
            "Google Workspace / Drive": 90,
            "Dokumen Kontrol (MS Word, Outlook)": 88,
        }
        for skill, pct in tech_skills.items():
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;font-size:0.85rem;color:#eef4ff;margin-bottom:4px;">
                    <span>{skill}</span><span style="color:#00f0ff;font-weight:700;">{pct}%</span>
                </div>
                <div style="height:8px;background:rgba(255,255,255,0.08);border-radius:8px;overflow:hidden;">
                    <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#00f0ff,#ff2ec4);border-radius:8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Soft Skills & Operasional")
        soft = [
            ("Rekayasa Data & Akurasi", "98.5% + akurasi & detail"),
            ("Manajemen Waktu", "Multi-tasking & prioritas"),
            ("Koordinasi Vendor", "15+ vendor aktif"),
            ("Kepatuhan SOP", "99.5% kepatuhan"),
            ("Quality Control", "Inspeksi & verifikasi produk"),
            ("K3 & 5S", "Implementasi di lingkungan kerja"),
        ]
        for name, desc in soft:
            st.markdown(f"""
            <div class="custom-card" style="padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-weight:600;color:#eef4ff;font-size:0.9rem;">{name}</div>
                    <span class="badge badge-cyan">{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Sertifikasi Resmi")
    cert_cols = st.columns(3)
    certs = [
        ("Google Analytics", "Google · Sertifikasi resmi analisis data & web analytics", "badge-cyan"),
        ("Finance Essentials", "NASBA · Sertifikasi akuntansi & keuangan diakui", "badge-magenta"),
        ("Microsoft Office Specialist", "Kursus Digital · Excel, Word, PowerPoint", "badge-purple"),
    ]
    for col, (title, desc, badge) in zip(cert_cols, certs):
        with col:
            st.markdown(f"""
            <div class="custom-card" style="text-align:center;">
                <h3 style="font-size:1.05rem;color:#eef4ff;">{title}</h3>
                <p style="font-size:0.85rem;">{desc}</p>
                <span class="badge {badge}">Bersertifikat</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Pengalaman Kerja")
    exp_cols = st.columns(2)
    with exp_cols[0]:
        st.markdown("""
        <div class="custom-card">
            <span class="badge badge-cyan">Jul 2025 - Feb 2026</span>
            <h3>Admin Warehouse — PT Nikomas Gemilang</h3>
            <p><i>Badan Usaha Manufaktur Sepatu</i></p>
            <ul style="color:#93a4c3;font-size:0.9rem;line-height:1.8;">
                <li>Menyusun laporan inventaris harian &amp; bulanan pakai VLOOKUP, Pivot Table, dan IF sebagai dasar kontrol stok yang akurat.</li>
                <li>Mengelola data entry 1.000+ item barang masuk/keluar secara rutin menggunakan Microsoft Excel.</li>
                <li>Memproses, menerbitkan, dan mengarsipkan dokumen operasional (surat jalan, faktur, PO) via MS Word.</li>
                <li>Mengoordinasikan alur logistik dengan 15+ vendor via MS Outlook agar pengiriman tepat waktu.</li>
                <li>Memastikan keakuratan data stok saat pergantian bulan dan mendukung proses audit internal.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with exp_cols[1]:
        st.markdown("""
        <div class="custom-card">
            <span class="badge badge-magenta">Feb 2024 - Jul 2025</span>
            <h3>Operator Produksi — PT Nikomas Gemilang</h3>
            <p><i>Badan Usaha Manufaktur Sepatu</i></p>
            <ul style="color:#93a4c3;font-size:0.9rem;line-height:1.8;">
                <li>Menyusun &amp; memverifikasi laporan hasil produksi harian yang akurat menggunakan Microsoft Excel.</li>
                <li>Mengoptimalkan pemakaian bahan baku sesuai instruksi kerja (WI), menekan material waste di bawah 5% tiap bulan.</li>
                <li>Melakukan inspeksi kualitas produk dan menurunkan cacat produksi hingga 15%.</li>
                <li>Mengoperasikan mesin produksi sesuai SOP dengan tingkat akurasi 98%.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Pendidikan")
    edu_cols = st.columns(2)
    with edu_cols[0]:
        st.markdown("""
        <div class="custom-card">
            <span class="badge badge-purple">Jul 2024 - Sekarang</span>
            <h3>Universitas Terbuka Serang</h3>
            <p>Administrasi Bisnis</p>
        </div>
        """, unsafe_allow_html=True)
    with edu_cols[1]:
        st.markdown("""
        <div class="custom-card">
            <span class="badge badge-green">Jul 2019 - Mei 2022</span>
            <h3>SMA Negeri 2 Pringsewu</h3>
            <p>Ilmu Pengetahuan Sosial · Nilai Rata-rata 81.91/100</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Kontak")
    ce1, ce2 = st.columns([2, 1])
    with ce1:
        st.markdown("""
        <div class="custom-card" style="display:flex;justify-content:space-around;flex-wrap:wrap;text-align:center;">
            <div><div style="font-weight:600;color:#eef4ff;">anitatiara25@gmail.com</div></div>
            <div><div style="font-weight:600;color:#eef4ff;">0856-6932-3610</div></div>
            <div><div style="font-weight:600;color:#eef4ff;">Babelan, Bekasi</div></div>
        </div>
        """, unsafe_allow_html=True)
    with ce2:
        li_url = "https://www.linkedin.com/in/anitatiarasani"
        wa_url = "https://wa.me/6285669323610"
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:10px;">
            <a class="contact-btn" style="color:#00f0ff;border-color:#00f0ff;background:rgba(0,240,255,0.08);text-align:center;" href="{li_url}" target="_blank">LinkedIn</a>
            <a class="contact-btn" style="color:#00ffa3;border-color:#00ffa3;background:rgba(0,255,163,0.08);text-align:center;" href="{wa_url}" target="_blank">WhatsApp</a>
        </div>
        """, unsafe_allow_html=True)


def render_warehouse(data):
    df_inv = data['inventory']
    df_trx = data['transactions']

    st.markdown("## Dashboard <span class='gradient-text'>Admin Warehouse</span>", unsafe_allow_html=True)
    st.markdown("Manajemen inventaris dan transaksi barang masuk/keluar, lengkap dengan simulasi fungsi Excel (VLOOKUP, Pivot Table, nested IF).")

    kpi = hitung_kpi_warehouse(df_inv, df_trx)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Total Nilai Inventaris", format_rupiah(kpi['total_nilai_inventaris']))
    mc2.metric("Total SKU", format_angka(kpi['total_sku']))
    mc3.metric("Stok Kritis", f"{kpi['stok_kritis']} item ({kpi['persentase_stok_kritis']}%)")
    mc4.metric("Akurasi Data Entry", f"{kpi['akurasi']}%")

    with st.expander("Penjelasan Detail — Dashboard Warehouse", expanded=False):
        st.markdown("""
        **Dashboard ini meniru pekerjaan admin warehouse di perusahaan manufaktur secara nyata.**
        
        - **Total Nilai Inventaris** adalah jumlah dari seluruh nilai stok barang (stok × harga satuan) di gudang. Angka besar ini menunjukkan saya terbiasa mengelola aset perusahaan yang bernilai miliaran rupiah.
        - **Total SKU** menunjukkan berapa banyak jenis barang berbeda yang harus saya ketahui detailnya (nama, lokasi, vendor, harga, stok minimum). Semakin banyak SKU, semakin tinggi tingkat kompleksitas pengelolaannya.
        - **Stok Kritis** adalah barang dengan stok *Habis* atau *Menipis* (di bawah stok minimum). Saya memantaunya setiap hari supaya produksi tidak terhenti karena barang tidak tersedia.
        - **Akurasi Data Entry** adalah tingkat ketelitian saya dalam memasukkan dan memverifikasi data, dipertahankan lewat metode double-check.
        """)

    st.markdown("---")

    tab_inv, tab_trx, tab_analisis = st.tabs([
        "Data Inventaris", "Transaksi Barang", "Analisis & Grafik"
    ])

    with tab_inv:
        st.markdown("### Data Inventaris Barang")
        st.caption("""
        Tabel ini memuat **150+ SKU** yang saya kelola di gudang. Setiap barang punya identitas lengkap: 
        SKU, nama, kategori, vendor, lokasi penyimpanan, unit, harga satuan, stok saat ini, stok minimum, 
        dan status. Kolom **Nilai Stok** dihitung otomatis dari `stok × harga` — mirip cara saya 
        memakai **VLOOKUP** untuk menarik harga lalu mengalikannya.
        """)
        st.markdown("Pakai filter di bawah buat simulasi pencarian data dan melihat stok per kategori.")

        f1, f2, f3 = st.columns(3)
        with f1:
            categories = ['Semua'] + list(df_inv['Kategori'].unique())
            cat_filter = st.selectbox("Kategori", categories)
        with f2:
            statuses = ['Semua'] + list(df_inv['Status'].unique())
            status_filter = st.selectbox("Status Stok", statuses)
        with f3:
            search = st.text_input("Cari Nama Barang/SKU")

        filtered = df_inv.copy()
        if cat_filter != 'Semua':
            filtered = filtered[filtered['Kategori'] == cat_filter]
        if status_filter != 'Semua':
            filtered = filtered[filtered['Status'] == status_filter]
        if search:
            filtered = filtered[
                filtered['Nama Barang'].str.contains(search, case=False, na=False) |
                filtered['SKU'].str.contains(search, case=False, na=False)
            ]

        st.dataframe(
            filtered,
            width='stretch',
            height=420,
            column_config={
                'Harga Satuan': st.column_config.NumberColumn(format="Rp %.0f"),
                'Nilai Stok': st.column_config.NumberColumn(format="Rp %.0f"),
                'Stok Saat Ini': st.column_config.NumberColumn(format="%d"),
                'Lead Time (hari)': st.column_config.NumberColumn(format="%d"),
            }
        )

        st.download_button(
            "Download Data Inventaris (CSV)",
            filtered.to_csv(index=False).encode('utf-8-sig'),
            file_name="data_inventaris.csv",
            mime="text/csv",
            key="download_inventory"
        )

        st.markdown("### Simulasi VLOOKUP (Pencarian Data)")
        st.markdown("Pilih SKU untuk menampilkan detail barang.")
        sku_options = df_inv['SKU'].tolist()
        selected_sku = st.selectbox("Pilih SKU", sku_options)
        if selected_sku:
            row = df_inv[df_inv['SKU'] == selected_sku].iloc[0]
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Nama Barang", row['Nama Barang'])
            d2.metric("Kategori", row['Kategori'])
            d3.metric("Stok", f"{row['Stok Saat Ini']} {row['Unit']}")
            d4.metric("Harga", format_rupiah(row['Harga Satuan']))
            st.markdown(f"**Lokasi:** {row['Lokasi']} | **Vendor:** {row['Vendor']} | **Status:** `{row['Status']}`")

        st.markdown("### Simulasi INDEX/MATCH (Pencarian Data)")
        st.markdown("INDEX/MATCH lebih fleksibel dari VLOOKUP — bisa ambil data dari kolom mana pun, termasuk kolom di kiri kolom pencarian.")
        im1, im2 = st.columns(2)
        with im1:
            im_sku = st.selectbox("Pilih SKU (INDEX/MATCH)", sku_options, key="im_sku")
        with im2:
            im_kolom = st.selectbox("Kolom yang Dicari", [
                'Nama Barang', 'Kategori', 'Vendor', 'Lokasi', 'Unit',
                'Harga Satuan', 'Stok Saat Ini', 'Stok Minimum', 'Status'
            ])
        if im_sku and im_kolom:
            hasil_im = index_match(df_inv, im_sku, 'SKU', im_kolom)
            if im_kolom in ['Harga Satuan', 'Nilai Stok']:
                hasil_tampil = format_rupiah(hasil_im)
            else:
                hasil_tampil = hasil_im
            st.info(f"**Hasil INDEX/MATCH:** `{im_kolom}` untuk `{im_sku}` = **{hasil_tampil}**")

    with tab_trx:
        st.markdown("### Transaksi Barang Masuk / Keluar")
        st.markdown("Data transaksi 12 bulan (5.000+ record) dengan agregasi otomatis.")

        t1, t2 = st.columns(2)
        with t1:
            bulan_list = ['Semua'] + list(df_trx['Bulan'].unique())
            bln_filter = st.selectbox("Pilih Bulan", bulan_list)
        with t2:
            tipe_filter = st.selectbox("Tipe Transaksi", ['Semua', 'Barang Masuk', 'Barang Keluar'])

        filtered_trx = df_trx.copy()
        if bln_filter != 'Semua':
            filtered_trx = filtered_trx[filtered_trx['Bulan'] == bln_filter]
        if tipe_filter != 'Semua':
            filtered_trx = filtered_trx[filtered_trx['Tipe'] == tipe_filter]

        st.dataframe(filtered_trx, width='stretch', height=420,
                     column_config={
                         'Total Nilai': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Harga Satuan': st.column_config.NumberColumn(format="Rp %.0f"),
                     })
        st.download_button(
            "Download Data Transaksi (CSV)",
            filtered_trx.to_csv(index=False).encode('utf-8-sig'),
            file_name="data_transaksi.csv",
            mime="text/csv",
            key="download_transaksi"
        )

        st.markdown("### Ringkasan Transaksi (Pivot)")
        pivot = filtered_trx.groupby(['Bulan', 'Tipe']).agg(
            Jumlah_Transaksi=('Total Nilai', 'count'),
            Total_Unit=('Jumlah', 'sum'),
            Total_Nilai=('Total Nilai', 'sum')
        ).reset_index()
        st.dataframe(pivot, width='stretch',
                     column_config={'Total_Nilai': st.column_config.NumberColumn(format="Rp %.0f")})

    with tab_analisis:
        st.markdown("### Analisis & Grafik Interaktif")

        g1, g2 = st.columns(2)
        with g1:
            nilai_kat = df_inv.groupby('Kategori')['Nilai Stok'].sum().reset_index()
            nilai_kat = nilai_kat.sort_values('Nilai Stok', ascending=False)
            st.plotly_chart(
                bar_chart(nilai_kat, 'Kategori', 'Nilai Stok', 'Nilai Inventaris per Kategori (Rp)'),
                width='stretch'
            )
        with g2:
            status_dist = df_inv['Status'].value_counts().reset_index()
            status_dist.columns = ['Status', 'Jumlah']
            st.plotly_chart(
                pie_chart(status_dist, 'Status', 'Jumlah', 'Distribusi Status Stok', hole=0.45),
                width='stretch'
            )

        g3, g4 = st.columns(2)
        with g3:
            trx_bulan = df_trx.groupby(['Bulan', 'Tipe'])['Total Nilai'].sum().reset_index()
            st.plotly_chart(
                stacked_bar_chart(trx_bulan, 'Bulan', 'Total Nilai', 'Tipe',
                                  'Tren Nilai Transaksi per Bulan (Rp)'),
                width='stretch'
            )
        with g4:
            trx_count = df_trx.groupby('Bulan').size().reset_index(name='Jumlah Transaksi')
            st.plotly_chart(
                line_chart(trx_count, 'Bulan', 'Jumlah Transaksi', 'Jumlah Transaksi per Bulan', area=True),
                width='stretch'
            )

        st.markdown("### Top 10 Barang Bernilai Tinggi")
        top10 = df_inv.nlargest(10, 'Nilai Stok')[['Nama Barang', 'Kategori', 'Stok Saat Ini', 'Harga Satuan', 'Nilai Stok']]
        st.dataframe(top10, width='stretch',
                     column_config={
                         'Harga Satuan': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Nilai Stok': st.column_config.NumberColumn(format="Rp %.0f"),
                     })
        st.download_button(
            "Download Top 10 Barang (CSV)",
            top10.to_csv(index=False).encode('utf-8-sig'),
            file_name="top10_barang.csv",
            mime="text/csv",
            key="download_top10"
        )

        st.markdown("### Barang Stok Kritis (Habis / Menipis)")
        stok_kritis = df_inv[df_inv['Status'].isin(['Habis', 'Menipis'])]
        if len(stok_kritis) > 0:
            st.dataframe(stok_kritis[['SKU', 'Nama Barang', 'Kategori', 'Stok Saat Ini', 'Stok Minimum', 'Status']],
                         width='stretch', height=300)
            st.download_button(
                "Download Stok Kritis (CSV)",
                stok_kritis.to_csv(index=False).encode('utf-8-sig'),
                file_name="stok_kritis.csv",
                mime="text/csv",
                key="download_stok_kritis"
            )
        else:
            st.success("Tidak ada barang dengan stok kritis. Semua stok aman.")

        st.markdown("### Hierarki Nilai Inventaris (Treemap)")
        st.plotly_chart(
            treemap(df_inv, ['Kategori', 'Nama Barang'], 'Nilai Stok', 'Nilai Inventaris per Barang'),
            width='stretch'
        )


def render_keuangan(data):
    df_fin = data['financial']
    df_budget = data['budget']

    st.markdown("## Dashboard <span class='gradient-text'>Admin Umum & Keuangan</span>", unsafe_allow_html=True)
    st.markdown("Data administrasi keuangan lengkap: jurnal umum, laba rugi, neraca, dan arus kas — dihitung otomatis dari data mentah.")

    total_pendapatan = df_fin[df_fin['Tipe Akun'] == 'Pendapatan']['Jumlah (Rp)'].sum()
    total_beban = df_fin[df_fin['Tipe Akun'] == 'Beban']['Jumlah (Rp)'].sum()
    laba = total_pendapatan - total_beban
    margin = (laba / total_pendapatan * 100) if total_pendapatan > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Pendapatan", format_rupiah(total_pendapatan))
    k2.metric("Total Beban", format_rupiah(total_beban))
    k3.metric("Laba Bersih", format_rupiah(laba), f"{margin:.1f}% margin")
    k4.metric("Total Transaksi", format_angka(len(df_fin)))

    with st.expander("Penjelasan Detail — Dashboard Keuangan", expanded=False):
        st.markdown("""
        **Dashboard ini meniru pengelolaan administrasi keuangan di perusahaan secara nyata.**

        - **Total Pendapatan** adalah seluruh pemasukan dari penjualan produk dan pendapatan lain-lain selama 12 bulan. Saya mencatatnya dari dokumen penjualan (invoice, faktur) ke jurnal umum.
        - **Total Beban** adalah seluruh pengeluaran operasional (gaji, listrik, sewa, transportasi, ATK, pemasaran, dll). Saya memastikan setiap beban tercatat dengan akun COA yang tepat supaya laporan akurat.
        - **Laba Bersih** = Pendapatan − Beban. Saya menyusunnya otomatis per bulan sehingga manajemen bisa langsung melihat tren profitabilitas.
        - **Total Transaksi** adalah jumlah seluruh entri jurnal yang saya kelola dan verifikasi, mencerminkan volume kerja administrasi keuangan yang tinggi.
        """)

    st.markdown("---")

    tab_jurnal, tab_lr, tab_neraca, tab_aruskas, tab_budget = st.tabs([
        "Jurnal Umum", "Laba Rugi", "Neraca", "Arus Kas", "Anggaran"
    ])

    with tab_jurnal:
        st.markdown("### Jurnal Umum (Transaksi Keuangan)")
        st.markdown("Data jurnal 12 bulan dengan filter interaktif.")

        j1, j2 = st.columns(2)
        with j1:
            bulan_list = ['Semua'] + list(df_fin['Bulan'].unique())
            bln = st.selectbox("Bulan", bulan_list, key="fin_bln")
        with j2:
            tipe_akun = ['Semua'] + list(df_fin['Tipe Akun'].unique())
            tipe = st.selectbox("Tipe Akun", tipe_akun)

        filtered_fin = df_fin.copy()
        if bln != 'Semua':
            filtered_fin = filtered_fin[filtered_fin['Bulan'] == bln]
        if tipe != 'Semua':
            filtered_fin = filtered_fin[filtered_fin['Tipe Akun'] == tipe]

        st.dataframe(filtered_fin, width='stretch', height=420,
                     column_config={'Jumlah (Rp)': st.column_config.NumberColumn(format="Rp %.0f")})
        st.download_button(
            "Download Jurnal Umum (CSV)",
            filtered_fin.to_csv(index=False).encode('utf-8-sig'),
            file_name="jurnal_umum.csv",
            mime="text/csv",
            key="download_jurnal"
        )

    with tab_lr:
        st.markdown("### Laporan Laba Rugi (per Bulan)")
        st.markdown("Pendapatan − Beban = Laba Bersih, dihitung otomatis dari jurnal.")

        lr = hitung_laba_rugi(df_fin)
        l1, l2, l3 = st.columns(3)
        l1.metric("Pendapatan (Total)", format_rupiah(lr['Jumlah (Rp)_Pendapatan'].sum()))
        l2.metric("Beban (Total)", format_rupiah(lr['Jumlah (Rp)_Beban'].sum()))
        l3.metric("Laba Bersih (Total)", format_rupiah(lr['Laba Bersih'].sum()))

        st.dataframe(lr, width='stretch',
                     column_config={
                         'Jumlah (Rp)_Pendapatan': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Jumlah (Rp)_Beban': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Laba Bersih': st.column_config.NumberColumn(format="Rp %.0f"),
                     })
        st.download_button(
            "Download Laba Rugi (CSV)",
            lr.to_csv(index=False).encode('utf-8-sig'),
            file_name="laba_rugi.csv",
            mime="text/csv",
            key="download_lr"
        )

        c1, c2 = st.columns(2)
        with c1:
            lr_plot = lr.melt(id_vars='Bulan', value_vars=['Jumlah (Rp)_Pendapatan', 'Jumlah (Rp)_Beban'],
                              var_name='Kategori', value_name='Nilai')
            lr_plot['Kategori'] = lr_plot['Kategori'].replace({
                'Jumlah (Rp)_Pendapatan': 'Pendapatan', 'Jumlah (Rp)_Beban': 'Beban'
            })
            st.plotly_chart(
                bar_chart(lr_plot, 'Bulan', 'Nilai', 'Pendapatan vs Beban per Bulan', color='Kategori'),
                width='stretch'
            )
        with c2:
            st.plotly_chart(
                line_chart(lr, 'Bulan', 'Laba Bersih', 'Tren Laba Bersih per Bulan', area=True),
                width='stretch'
            )

        st.markdown("### Waterfall Laba Rugi (Total 12 Bulan)")
        wf_labels = ['Pendapatan', 'Beban', 'Laba Bersih']
        wf_values = [total_pendapatan, -total_beban, laba]
        wf_measure = ['relative', 'relative', 'total']
        st.plotly_chart(
            waterfall_chart(wf_labels, wf_values, 'Laporan Laba Rugi (Total)', wf_measure),
            width='stretch'
        )

    with tab_neraca:
        st.markdown("### Laporan Neraca (Posisi Keuangan)")
        st.markdown("Ringkasan aset, liabilitas, dan ekuitas dihitung otomatis.")

        neraca = hitung_neraca(df_fin)

        n1, n2, n3 = st.columns(3)
        n1.metric("Total Aset", format_rupiah(neraca[neraca['Akun'] == 'Total Aset']['Jumlah (Rp)'].iloc[0]))
        n2.metric("Total Liabilitas", format_rupiah(neraca[neraca['Akun'] == 'Total Liabilitas']['Jumlah (Rp)'].iloc[0]))
        n3.metric("Total Ekuitas", format_rupiah(neraca[neraca['Akun'] == 'Total Ekuitas']['Jumlah (Rp)'].iloc[0]))

        st.dataframe(neraca, width='stretch',
                     column_config={'Jumlah (Rp)': st.column_config.NumberColumn(format="Rp %.0f")})
        st.download_button(
            "Download Neraca (CSV)",
            neraca.to_csv(index=False).encode('utf-8-sig'),
            file_name="neraca.csv",
            mime="text/csv",
            key="download_neraca"
        )

        aset_items = neraca[neraca['Akun'].isin(['Kas & Bank', 'Piutang Usaha', 'Persediaan', 'Peralatan'])][['Akun', 'Jumlah (Rp)']]
        st.plotly_chart(
            pie_chart(aset_items, 'Akun', 'Jumlah (Rp)', 'Komposisi Aset', hole=0.5),
            width='stretch'
        )

    with tab_aruskas:
        st.markdown("### Laporan Arus Kas (per Bulan)")
        st.markdown("Arus kas operasional, investasi, dan pendanaan dihitung otomatis.")

        ak = hitung_arus_kas(df_fin)
        st.dataframe(ak, width='stretch',
                     column_config={
                         'Jumlah (Rp)_Operasional': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Jumlah (Rp)_Investasi': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Jumlah (Rp)': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Arus Kas Bersih': st.column_config.NumberColumn(format="Rp %.0f"),
                     })
        st.download_button(
            "Download Arus Kas (CSV)",
            ak.to_csv(index=False).encode('utf-8-sig'),
            file_name="arus_kas.csv",
            mime="text/csv",
            key="download_aruskas"
        )

        st.plotly_chart(
            line_chart(ak, 'Bulan', 'Arus Kas Bersih', 'Arus Kas Bersih per Bulan (Rp)', area=True),
            width='stretch'
        )

    with tab_budget:
        st.markdown("### Anggaran vs Realisasi")
        st.markdown("Perbandingan anggaran dan realisasi biaya per kategori.")

        b1, b2, b3 = st.columns(3)
        b1.metric("Total Anggaran", format_rupiah(df_budget['Anggaran (Rp)'].sum()))
        b2.metric("Total Realisasi", format_rupiah(df_budget['Realisasi (Rp)'].sum()))
        b3.metric("Selisih (Hemat)", format_rupiah(df_budget['Selisih (Rp)'].sum()))

        budget_plot = df_budget.melt(id_vars='Kategori', value_vars=['Anggaran (Rp)', 'Realisasi (Rp)'],
                                     var_name='Tipe', value_name='Nilai')
        st.plotly_chart(
            bar_chart(budget_plot, 'Kategori', 'Nilai', 'Anggaran vs Realisasi per Kategori', color='Tipe'),
            width='stretch'
        )

        st.dataframe(df_budget, width='stretch',
                     column_config={
                         'Anggaran (Rp)': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Realisasi (Rp)': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Selisih (Rp)': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Persentase': st.column_config.NumberColumn(format="%.1f%%"),
                     })
        st.download_button(
            "Download Anggaran vs Realisasi (CSV)",
            df_budget.to_csv(index=False).encode('utf-8-sig'),
            file_name="anggaran_vs_realisasi.csv",
            mime="text/csv",
            key="download_budget"
        )


def render_karyawan(data):
    df_emp = data['employees']

    st.markdown("## Data <span class='gradient-text'>Karyawan & Administrasi</span>", unsafe_allow_html=True)
    st.markdown("Pengelolaan data karyawan (SDM) — filter departemen, status kerja, dan analisis penggajian.")

    # KPI ringkas
    total_gaji = df_emp['Gaji Pokok'].sum() + df_emp['Tunjangan'].sum() + df_emp['Bonus'].sum()
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Total Karyawan", format_angka(len(df_emp)))
    e2.metric("Departemen", format_angka(df_emp['Departemen'].nunique()))
    e3.metric("Total Upah/Bulan", format_rupiah(total_gaji))
    e4.metric("Status Tetap", f"{df_emp[df_emp['Status Kerja'] == 'Tetap'].shape[0]} orang")

    st.markdown("---")

    tab_tabel, tab_analisis = st.tabs(["Data Karyawan", "Analisis SDM"])

    with tab_tabel:
        st.markdown("### Data Karyawan")
        ef1, ef2, ef3 = st.columns(3)
        with ef1:
            dept_list = ['Semua'] + list(df_emp['Departemen'].unique())
            dept = st.selectbox("Departemen", dept_list)
        with ef2:
            status_list = ['Semua'] + list(df_emp['Status Kerja'].unique())
            status = st.selectbox("Status Kerja", status_list)
        with ef3:
            cari_nama = st.text_input("Cari Nama / NIK")

        filtered = df_emp.copy()
        if dept != 'Semua':
            filtered = filtered[filtered['Departemen'] == dept]
        if status != 'Semua':
            filtered = filtered[filtered['Status Kerja'] == status]
        if cari_nama:
            filtered = filtered[
                filtered['Nama'].str.contains(cari_nama, case=False, na=False) |
                filtered['NIK'].str.contains(cari_nama, case=False, na=False)
            ]

        st.dataframe(filtered, width='stretch', height=420,
                     column_config={
                         'Gaji Pokok': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Tunjangan': st.column_config.NumberColumn(format="Rp %.0f"),
                         'Bonus': st.column_config.NumberColumn(format="Rp %.0f"),
                     })
        st.download_button(
            "Download Data Karyawan (CSV)",
            filtered.to_csv(index=False).encode('utf-8-sig'),
            file_name="data_karyawan.csv",
            mime="text/csv",
            key="download_karyawan"
        )

    with tab_analisis:
        st.markdown("### Analisis Komposisi & Penggajian")

        a1, a2 = st.columns(2)
        with a1:
            dept_count = df_emp.groupby('Departemen').size().reset_index(name='Jumlah')
            st.plotly_chart(
                bar_chart(dept_count, 'Departemen', 'Jumlah', 'Jumlah Karyawan per Departemen'),
                width='stretch'
            )
        with a2:
            status_dist = df_emp.groupby('Status Kerja').size().reset_index(name='Jumlah')
            st.plotly_chart(
                pie_chart(status_dist, 'Status Kerja', 'Jumlah', 'Status Kerja Karyawan', hole=0.45),
                width='stretch'
            )

        a3, a4 = st.columns(2)
        with a3:
            gaji_dept = df_emp.groupby('Departemen')['Gaji Pokok'].sum().reset_index()
            gaji_dept = gaji_dept.sort_values('Gaji Pokok', ascending=False)
            st.plotly_chart(
                bar_chart(gaji_dept, 'Departemen', 'Gaji Pokok', 'Total Gaji Pokok per Departemen'),
                width='stretch'
            )
        with a4:
            st.plotly_chart(
                histogram(df_emp, 'Gaji Pokok', 'Distribusi Gaji Pokok', nbins=15),
                width='stretch'
            )


def render_kinerja(data):
    df_perf = data['performance']
    df_trx = data['transactions']
    df_inv = data['inventory']

    st.markdown("## Hasil & <span class='gradient-text'>Nilai Kinerja</span>", unsafe_allow_html=True)
    st.markdown("Ringkasan pencapaian, nilai tambah, dan KPI yang bisa dipertanggungjawabkan.")

    st.markdown("### Nilai Tambah Utama")
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Akurasi Data Entry", "99.5%", "naik dari 85%")
    v2.metric("Efisiensi Proses", "2.5x lebih cepat", "2.5 jam → 1 jam")
    v3.metric("Penghematan Biaya", "Rp 366 jt", "12 bulan")
    v4.metric("Data Kelola", "5.000+ transaksi", "1.000+ item/bulan")

    st.markdown("---")

    st.markdown("### KPI Kinerja Bulanan")
    chart1, chart2 = st.columns(2)
    with chart1:
        st.plotly_chart(
            multi_line_chart(df_perf, 'Bulan', ['Akurasi Data Entry (%)', 'Kepatuhan SOP (%)'],
                             'Akurasi & Kepatuhan SOP (%)', labels={'Akurasi Data Entry (%)': 'Akurasi', 'Kepatuhan SOP (%)': 'Kepatuhan'}),
            width='stretch'
        )
    with chart2:
        st.plotly_chart(
            line_chart(df_perf, 'Bulan', 'Waktu Proses (jam)', 'Waktu Pemrosesan Dokumen (jam)', area=True),
            width='stretch'
        )

    chart3, chart4 = st.columns(2)
    with chart3:
        st.plotly_chart(
            bar_chart(df_perf, 'Bulan', 'Transaksi Diproses', 'Jumlah Transaksi Diproses per Bulan'),
            width='stretch'
        )
    with chart4:
        st.plotly_chart(
            line_chart(df_perf, 'Bulan', 'Penghematan Biaya (jt)', 'Penghematan Biaya (Rp juta)', area=True),
            width='stretch'
        )

    st.markdown("### Pencapaian Target")
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        st.plotly_chart(gauge_chart(99.5, 'Akurasi Data Entry', 100, COLORS['cyan']), width='stretch')
    with gc2:
        st.plotly_chart(gauge_chart(100, 'Kepatuhan SOP', 100, COLORS['green']), width='stretch')
    with gc3:
        st.plotly_chart(gauge_chart(95, 'Efisiensi Proses', 100, COLORS['magenta']), width='stretch')

    st.markdown("### Pencapaian Kualitatif")
    achievements = [
        ("Optimasi Manajemen Inventaris", "Menurunkan stok menipis/habis dari 18% menjadi 5% lewat analisis stok minimum & reorder point (VLOOKUP + IF)."),
        ("Percepatan Proses Administrasi", "Memangkas waktu penyusunan laporan dari 2,5 jam menjadi 1 jam lewat otomatisasi Pivot Table & template dinamis."),
        ("Akurasi Data Meningkat", "Menaikkan akurasi data entry dari 85% ke 99,5% lewat sistem double-check & standardisasi format."),
        ("Penghematan Biaya Operasional", "Mengidentifikasi penghematan biaya material & logistik hingga Rp 366 juta dalam 12 bulan."),
        ("Koordinasi Vendor", "Mengelola relasi dengan 15+ vendor, memastikan pengiriman tepat waktu & meminimalkan keterlambatan."),
        ("Kepatuhan & Audit", "Menjaga kepatuhan SOP 99,5% dan siap dalam audit internal dengan dokumentasi lengkap & rapi."),
    ]
    for title, desc in achievements:
        st.markdown(f"""
        <div class="custom-card" style="display:flex;gap:16px;align-items:flex-start;">
            <div style="font-size:2rem;flex-shrink:0;">o</div>
            <div>
                <h3 style="margin:0;font-size:1.05rem;color:#00f0ff;">{title}</h3>
                <p style="margin:4px 0 0;color:#93a4c3;font-size:0.9rem;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Statistik Pengelolaan Data")
    total_masuk = df_trx[df_trx['Tipe'] == 'Barang Masuk']['Jumlah'].sum()
    total_keluar = df_trx[df_trx['Tipe'] == 'Barang Keluar']['Jumlah'].sum()
    s1, s2, s3 = st.columns(3)
    s1.metric("Barang Masuk (Total)", format_angka(total_masuk), "unit")
    s2.metric("Barang Keluar (Total)", format_angka(total_keluar), "unit")
    s3.metric("Total SKU Dikelola", format_angka(len(df_inv)), "item")


def render_footer():
    st.markdown("""
    <div class="footer">
        Dibuat dengan <span style="color:#ff2ec4;">o</span> oleh <b style="color:#00f0ff;">Anita Tiara Sani</b> — Admin Warehouse &amp; Admin Umum<br>
        © 2026 · Data dummy untuk demonstrasi portfolio
    </div>
    """, unsafe_allow_html=True)


def main():
    inject_css()
    render_header()

    with st.sidebar:
        st.markdown("### Navigasi")
        page = st.radio(
            "Pilih Halaman",
            ["Beranda / Profil", "Dashboard Warehouse", "Dashboard Keuangan", "Data Karyawan", "Hasil Kinerja"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("### Ringkasan Cepat")
        st.markdown("""
        <div style="font-size:0.85rem;color:#93a4c3;">
            <div><b>Anita Tiara Sani</b></div>
            <div>Admin Warehouse &amp; Umum</div>
            <div>anitatiara25@gmail.com</div>
            <div>0856-6932-3610</div>
        </div>
        """, unsafe_allow_html=True)

    data = load_data()

    if page.startswith("Beranda"):
        render_beranda()
    elif page.startswith("Dashboard Warehouse"):
        render_warehouse(data)
    elif page.startswith("Dashboard Keuangan"):
        render_keuangan(data)
    elif page.startswith("Data Karyawan"):
        render_karyawan(data)
    elif page.startswith("Hasil Kinerja"):
        render_kinerja(data)

    render_footer()


@st.cache_data
def load_data():
    """Muat dan cache semua data."""
    return load_all_data()


if __name__ == '__main__':
    main()
