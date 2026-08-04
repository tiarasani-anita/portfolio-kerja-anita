# 📊 Portfolio Interaktif — Anita Tiara Sani

**Admin Warehouse & Admin Umum | Data-Driven Portfolio**

Portfolio profesional modern berbasis **Python (Streamlit)** yang menampilkan keahlian administrasi, keuangan, logistik, dan pengolahan data secara interaktif. Dibuat untuk menonjol di mata HRD dengan dashboard data nyata, grafik interaktif, dan nilai kinerja yang terukur.

---

## ✨ Fitur Unggulan

| Halaman | Deskripsi |
|---------|-----------|
| 🏠 **Beranda / Profil** | Profil profesional, keahlian teknis, soft skills, sertifikasi, pengalaman kerja, pendidikan, dan kontak |
| 🏭 **Dashboard Admin Warehouse** | Manajemen inventaris 145+ item, transaksi barang masuk/keluar 5.000+ record, simulasi VLOOKUP, Pivot Table, dan nested IF |
| 💰 **Dashboard Admin Umum & Keuangan** | Jurnal umum, laporan laba rugi, neraca, arus kas, dan anggaran vs realisasi — semua dihitung otomatis |
| 🏆 **Hasil Kinerja** | KPI, pencapaian, nilai tambah, gauge chart, dan statistik pengelolaan data |

## 🚀 Cara Menjalankan

```bash
# 1. Masuk ke folder proyek
cd portfolio-anita-python

# 2. (Opsional) Buat virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka di browser: **http://localhost:8501**

## 🗂️ Struktur Proyek

```
portfolio-anita-python/
├── app.py                    # Aplikasi Streamlit utama (+ CSS styling)
├── requirements.txt          # Dependensi
├── README.md                 # Dokumentasi ini
├── data/
│   └── generate_data.py      # Generator dummy data realistis (seed konsisten)
└── utils/
    ├── formulas.py           # Formula aktif: VLOOKUP, pivot, keuangan, KPI
    └── charts.py             # Grafik interaktif Plotly (styling premium)
```

## 📊 Data yang Dihasilkan (Dummy Realistis)

| Dataset | Jumlah | Keterangan |
|---------|--------|------------|
| Inventaris | 145 item | Bahan baku, barang jadi, sparepart, ATK, peralatan |
| Transaksi inventaris | 5.000 record | Barang masuk & keluar 12 bulan |
| Jurnal keuangan | 800 record | 22 akun COA, pendapatan, beban, aset, liabilitas |
| Data karyawan | 50 orang | Penggajian & administrasi umum |
| KPI kinerja | 12 bulan | Akurasi, kepatuhan, efisiensi, transaksi |
| Anggaran | 10 kategori | Anggaran vs realisasi |

## 🎯 Nilai Kinerja Utama (untuk HRD)

- 📈 **Akurasi data entry 99,5%** (naik dari 85%)
- ⏱️ **Efisiensi proses 2,5x lebih cepat** (2,5 jam → 1 jam)
- 💰 **Penghematan biaya Rp 366 juta** dalam 12 bulan
- 📦 **Pengelolaan 5.000+ transaksi** & 1.000+ item/bulan
- 📊 **Kemampuan implementasi logika Excel** (VLOOKUP, Pivot Table, IF) dalam Python

---

© 2026 Anita Tiara Sani · Data untuk demonstrasi portfolio
