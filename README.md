# Portfolio Anita Tiara Sani — Admin Warehouse & Admin Umum

Portfolio profesional berbasis data, dibangun dengan **Streamlit + Python**. Semua angka di dashboard dihitung dari data dummy yang realistis (inventaris 150+ item, transaksi 5.000+, jurnal keuangan 800 entri, data karyawan, KPI 12 bulan, dan anggaran).

## Halaman

| Halaman | Isi |
|---------|-----|
| 🏠 **Beranda / Profil** | Ringkasan profil, keahlian, sertifikasi, pengalaman, pendidikan, kontak |
| 🏭 **Dashboard Warehouse** | Inventaris 150+ SKU, transaksi masuk/keluar, simulasi VLOOKUP, pivot, grafik analisis |
| 💰 **Dashboard Keuangan** | Jurnal umum, laba rugi, neraca, arus kas, anggaran vs realisasi |
| 👥 **Data Karyawan** | Data SDM, filter departemen & status, analisis penggajian dan komposisi karyawan |
| 🏆 **Hasil Kinerja** | KPI bulanan, pencapaian kualitatif, gauge chart, statistik pengelolaan data |

## Cara menjalankan

```bash
cd portfolio-anita-python

# (opsional) buat virtual environment
python -m venv venv
venv\Scripts\activate

# install dependensi
pip install -r requirements.txt

# jalankan
streamlit run app.py
```

Lalu buka http://localhost:8501 di browser.

## Struktur

```
portfolio-anita-python/
├── app.py                # Aplikasi utama + styling CSS
├── api/
│   └── index.py          # Endpoint sederhana untuk platform Vercel
├── data/
│   └── generate_data.py  # Generator data dummy realistis (seed tetap)
├── utils/
│   ├── formulas.py       # Logika VLOOKUP, pivot, perhitungan keuangan, KPI
│   └── charts.py         # Fungsi grafik Plotly sesuai tema
├── .streamlit/
│   └── config.toml       # Konfigurasi tema & server
├── vercel.json
└── requirements.txt
```

## Deploy

Opsi termudah: deploy melalui **Streamlit Community Cloud** — tinggal hubungkan repo ini ke app.streamlit.io.

Untuk deploy ke Vercel, struktur `api/` dan `vercel.json` sudah disiapkan, tetapi perlu server ASGI (`api/index.py`) untuk benar-benar menghosting aplikasi. Rekomendasi: pakai **Streamlit Community Cloud** supaya lebih stabil, gratis, dan otomatis tersambung ke repo.

## Catatan

Semua data bersifat dummy dan dibuat ulang setiap kali aplikasi dijalankan (seed konsisten), jadi angka bisa berubah-ubah sedikit tapi tetap realistis. Data ini ditujukan untuk demonstrasi kemampuan, bukan data produksi.

© 2026 Anita Tiara Sani

