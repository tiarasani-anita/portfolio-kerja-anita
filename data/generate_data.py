# Generator data dummy yang realistis buat portfolio Anita.
# Semua angka dibuat konsisten lewat seed biar gak berubah-ubah tiap run.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# Buat nama bulan dalam Bahasa Indonesia
BULAN_ID = {
    'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
    'April': 'April', 'May': 'Mei', 'June': 'Juni',
    'July': 'Juli', 'August': 'Agustus', 'September': 'September',
    'October': 'Oktober', 'November': 'November', 'December': 'Desember'
}


def _bulan_id(dt):
    return BULAN_ID[dt.strftime('%B')]


# ==== 1. Inventaris warehouse ====
def generate_inventory(n_items=150):
    # Kategori barang khas perusahaan manufaktur sepatu
    categories = {
        'Bahan Baku': ['Kulit Sintetis', 'Kain Kanvas', 'Karet Sol', 'Lem Perekat', 'Benang Jahit', 'Sponge', 'Karton Box', 'Plastik Packing'],
        'Barang Jadi': ['Sepatu Sneakers', 'Sepatu Formal', 'Sepatu Olahraga', 'Sepatu Sandal', 'Boots Safety'],
        'Sparepart': ['Mesin Jahit', 'Komponen Mesin', 'Roller Conveyor', 'Bearing', 'Motor Listrik'],
        'ATK': ['Kertas A4', 'Pulpen', 'Stapler', 'Map Folder', 'Tinta Printer', 'Amplop'],
        'Peralatan': ['Safety Gloves', 'Helm Safety', 'Mesin Cutting', 'Gunting Industri', 'Alat Ukur']
    }

    # Daftar nama barang
    item_names = []
    for cat, items in categories.items():
        for item in items:
            for i in range(1, 6):
                item_names.append(f"{item} {['Tipe A','Tipe B','Tipe C','Tipe D','Tipe E'][i-1]}")
    item_names = item_names[:n_items]

    vendors = [
        'PT Sinar Jaya Sentosa', 'CV Karya Utama', 'PT Berkah Abadi', 'PT Indo Makmur',
        'CV Sumber Rejeki', 'PT Global Teknik', 'PT Multi Sarana', 'CV Mitra Sejahtera',
        'PT Karya Mandiri', 'PT Surya Perkasa', 'CV Anugerah Jaya', 'PT Nusantara Sejahtera',
        'PT Prima Karya', 'CV Bintang Utara', 'PT Maju Bersama'
    ]
    locations = ['Gudang A1', 'Gudang A2', 'Gudang B1', 'Gudang B2', 'Gudang C1', 'Gudang C2']
    units = ['pcs', 'box', 'kg', 'liter', 'roll', 'pasang', 'unit', 'rim']

    price_ranges = {
        'Bahan Baku': (5000, 150000),
        'Barang Jadi': (150000, 1500000),
        'Sparepart': (25000, 500000),
        'ATK': (5000, 50000),
        'Peralatan': (50000, 800000)
    }

    data = []
    for i, name in enumerate(item_names):
        # Cari kategori dari nama barang
        category = 'Barang Jadi'
        for cat, items in categories.items():
            if any(item.split(' ')[0] in name for item in items):
                category = cat
                break

        min_price, max_price = price_ranges.get(category, (10000, 200000))
        unit_price = round(random.uniform(min_price, max_price), 2)

        current_stock = random.randint(0, 500)
        min_stock = random.randint(5, 30)
        max_stock = random.randint(100, 500)
        stock_value = round(current_stock * unit_price, 2)
        lead_time = random.randint(1, 14)

        if current_stock == 0:
            status = 'Habis'
        elif current_stock <= min_stock:
            status = 'Menipis'
        elif current_stock <= min_stock * 1.5:
            status = 'Perlu Order'
        else:
            status = 'Aman'

        data.append({
            'SKU': f'SKU-{1000+i}',
            'Nama Barang': name,
            'Kategori': category,
            'Vendor': random.choice(vendors),
            'Lokasi': random.choice(locations),
            'Unit': random.choice(units),
            'Harga Satuan': unit_price,
            'Stok Saat Ini': current_stock,
            'Stok Minimum': min_stock,
            'Stok Maksimum': max_stock,
            'Nilai Stok': stock_value,
            'Lead Time (hari)': lead_time,
            'Status': status
        })

    return pd.DataFrame(data)


# ==== 2. Transaksi barang masuk/keluar ====
def generate_inventory_transactions(inventory_df, n_transactions=5000):
    transactions = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    for _ in range(n_transactions):
        item = inventory_df.sample(1).iloc[0]
        tx_type = random.choice(['Barang Masuk', 'Barang Keluar'])
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        qty = random.randint(1, 100)
        price = item['Harga Satuan'] * random.uniform(0.9, 1.1)
        total = round(qty * price, 2)

        doc_type = random.choice(['PO', 'Surat Jalan', 'Faktur', 'Bon Keluar'])
        doc_number = f"{doc_type}-{date.strftime('%Y%m')}-{random.randint(100, 999)}"
        pic = random.choice(['Anita Tiara Sani', 'Budi Santoso', 'Siti Rahma', 'Dedi Kurniawan', 'Rina Marlina'])
        notes = random.choice([
            'Penerimaan dari vendor', 'Pengiriman ke produksi', 'Penyesuaian stok',
            'Retur barang', 'Pemakaian produksi', 'Pengiriman ke toko', 'Koreksi stok'
        ])

        transactions.append({
            'Tanggal': date.strftime('%Y-%m-%d'),
            'Bulan': _bulan_id(date),
            'Tahun': date.year,
            'No. Transaksi': f"TRX-{date.strftime('%Y%m')}-{random.randint(10000, 99999)}",
            'SKU': item['SKU'],
            'Nama Barang': item['Nama Barang'],
            'Kategori': item['Kategori'],
            'Tipe': tx_type,
            'Jumlah': qty,
            'Harga Satuan': round(price, 2),
            'Total Nilai': total,
            'Dokumen': doc_number,
            'PIC': pic,
            'Keterangan': notes
        })

    df = pd.DataFrame(transactions)
    return df.sort_values('Tanggal').reset_index(drop=True)


# ==== 3. Jurnal keuangan (COA) ====
def generate_financial_transactions(n_transactions=800):
    coa = {
        '1-1000': ('Kas', 'Aset'),
        '1-1100': ('Bank BCA', 'Aset'),
        '1-1200': ('Piutang Usaha', 'Aset'),
        '1-1300': ('Persediaan Bahan Baku', 'Aset'),
        '1-1400': ('Persediaan Barang Jadi', 'Aset'),
        '1-1500': ('Peralatan Kantor', 'Aset'),
        '1-1600': ('Akumulasi Penyusutan', 'Aset'),
        '2-1000': ('Hutang Usaha', 'Liabilitas'),
        '2-2000': ('Hutang Bank', 'Liabilitas'),
        '3-1000': ('Modal', 'Ekuitas'),
        '3-1100': ('Laba Ditahan', 'Ekuitas'),
        '4-1000': ('Pendapatan Penjualan', 'Pendapatan'),
        '4-2000': ('Pendapatan Lain-lain', 'Pendapatan'),
        '5-1000': ('HPP', 'Beban'),
        '5-2000': ('Beban Gaji', 'Beban'),
        '5-3000': ('Beban Listrik & Air', 'Beban'),
        '5-4000': ('Beban Sewa', 'Beban'),
        '5-5000': ('Beban Transportasi', 'Beban'),
        '5-6000': ('Beban ATK & Kantor', 'Beban'),
        '5-7000': ('Beban Pemeliharaan', 'Beban'),
        '5-8000': ('Beban Pemasaran', 'Beban'),
        '5-9000': ('Beban Lain-lain', 'Beban')
    }

    descriptions = {
        '4-1000': ['Penjualan produk sepatu', 'Penjualan tunai', 'Penjualan kredit', 'Penerimaan order'],
        '4-2000': ['Pendapatan bunga bank', 'Pendapatan sewa', 'Pendapatan lain-lain'],
        '5-1000': ['Pembelian bahan baku', 'HPP penjualan', 'Pemakaian bahan baku'],
        '5-2000': ['Pembayaran gaji karyawan', 'Gaji admin', 'Upah operator'],
        '5-3000': ['Pembayaran listrik & air', 'Tagihan listrik', 'Tagihan air'],
        '5-4000': ['Pembayaran sewa gudang', 'Sewa kantor', 'Sewa gedung'],
        '5-5000': ['Biaya transportasi', 'Pengiriman barang', 'Bensin operasional'],
        '5-6000': ['Pembelian ATK', 'Alat tulis kantor', 'Perlengkapan kantor'],
        '5-7000': ['Perbaikan mesin', 'Maintenance gedung', 'Servis peralatan'],
        '5-8000': ['Biaya iklan', 'Promosi produk', 'Marketing digital'],
        '5-9000': ['Biaya administrasi', 'Biaya bank', 'Biaya operasional lain']
    }

    transactions = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    methods = ['Tunai', 'Transfer Bank', 'Kartu Kredit', 'Debit']

    # Bobot biar komposisi akun realistis (banyak pendapatan & beban)
    weights = [0.25, 0.15, 0.08, 0.05, 0.04, 0.03, 0.02, 0.08, 0.02, 0.02, 0.01,
               0.15, 0.02, 0.08, 0.05, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]

    for _ in range(n_transactions):
        account = random.choices(list(coa.keys()), weights=weights, k=1)[0]
        account_name, account_type = coa[account]
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

        # Besaran nominal beda-beda tergantung jenis akun
        if account_type == 'Pendapatan':
            amount = round(random.uniform(500000, 50000000), 2)
        elif account_type == 'Beban':
            amount = round(random.uniform(100000, 25000000), 2)
        elif account_type == 'Aset':
            amount = round(random.uniform(500000, 30000000), 2)
        elif account_type == 'Liabilitas':
            amount = round(random.uniform(100000, 20000000), 2)
        else:
            amount = round(random.uniform(1000000, 50000000), 2)

        desc = random.choice(descriptions.get(account, ['Transaksi umum']))
        method = random.choice(methods)
        ref = f"BUK-{date.strftime('%Y%m')}-{random.randint(1000, 9999)}"

        transactions.append({
            'Tanggal': date.strftime('%Y-%m-%d'),
            'Bulan': _bulan_id(date),
            'Tahun': date.year,
            'No. Jurnal': f"JRN-{date.strftime('%Y%m')}-{random.randint(1000, 9999)}",
            'Kode Akun': account,
            'Nama Akun': account_name,
            'Tipe Akun': account_type,
            'Deskripsi': desc,
            'Jumlah (Rp)': amount,
            'Metode Pembayaran': method,
            'Referensi': ref,
            'PIC': random.choice(['Anita Tiara Sani', 'Budi Santoso', 'Siti Rahma'])
        })

    df = pd.DataFrame(transactions)
    return df.sort_values('Tanggal').reset_index(drop=True)


# ==== 4. Data karyawan ====
def generate_employee_data(n_employees=50):
    departments = ['Produksi', 'Warehouse', 'Administrasi', 'Keuangan', 'HRD', 'Marketing', 'Quality Control']
    positions = {
        'Produksi': ['Operator Produksi', 'SPV Produksi', 'Kepala Produksi'],
        'Warehouse': ['Admin Warehouse', 'Staff Gudang', 'Kepala Gudang'],
        'Administrasi': ['Admin Umum', 'Staff Administrasi', 'Kepala Administrasi'],
        'Keuangan': ['Staf Keuangan', 'Akuntan', 'Kepala Keuangan'],
        'HRD': ['Staff HRD', 'HRD Officer', 'Kepala HRD'],
        'Marketing': ['Staff Marketing', 'Marketing Executive', 'Kepala Marketing'],
        'Quality Control': ['QC Inspector', 'QC Supervisor', 'Kepala QC']
    }

    first_names = ['Anita', 'Budi', 'Siti', 'Dedi', 'Rina', 'Agus', 'Dewi', 'Joko', 'Sri', 'Eko',
                   'Andi', 'Maria', 'Benny', 'Citra', 'Dani', 'Eka', 'Fitri', 'Gunawan', 'Hendra',
                   'Indah', 'Kurnia', 'Lina', 'Maya', 'Nanda', 'Oscar', 'Putri', 'Rudi', 'Sari',
                   'Tono', 'Umi', 'Vina', 'Wawan', 'Yuni', 'Zainal', 'Ahmad', 'Bella', 'Candra', 'Dina']
    last_names = ['Santoso', 'Rahman', 'Wijaya', 'Kusuma', 'Saputra', 'Hidayat', 'Pratama', 'Nugroho',
                  'Ramadhan', 'Setiawan', 'Wibowo', 'Lestari', 'Anggraini', 'Utami', 'Handayani', 'Suryani',
                  'Mulyani', 'Hartono', 'Susanto', 'Supriyadi']

    religions = ['Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha']
    statuses = ['Kontrak', 'Tetap', 'Magang']
    genders = ['Laki-laki', 'Perempuan']

    data = []
    for i in range(n_employees):
        dept = random.choice(departments)
        pos = random.choice(positions[dept])

        # Gaji menyesuaikan jabatan
        if 'Kepala' in pos or 'Manager' in pos:
            salary = random.randint(8000000, 15000000)
        elif 'SPV' in pos or 'Supervisor' in pos:
            salary = random.randint(6000000, 9000000)
        elif 'Admin' in pos or 'Staff' in pos or 'Operator' in pos:
            salary = random.randint(3500000, 5500000)
        else:
            salary = random.randint(4000000, 7000000)

        status = random.choices(statuses, weights=[0.5, 0.3, 0.2], k=1)[0]
        hire_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))

        data.append({
            'No. Karyawan': f'EMP-{1000+i}',
            'Nama': f"{random.choice(first_names)} {random.choice(last_names)}",
            'Jenis Kelamin': random.choice(genders),
            'Departemen': dept,
            'Jabatan': pos,
            'Agama': random.choice(religions),
            'Status Kerja': status,
            'Tanggal Masuk': hire_date.strftime('%Y-%m-%d'),
            'Gaji Pokok': salary,
            'Tunjangan': random.randint(500000, 2000000),
            'Bonus': random.randint(0, 1000000) if status == 'Tetap' else 0
        })

    return pd.DataFrame(data)


# ==== 5. KPI kinerja bulanan ====
def generate_performance_data():
    months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
              'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

    return pd.DataFrame({
        'Bulan': months,
        'Akurasi Data Entry (%)': [98.5, 98.8, 99.0, 99.2, 99.4, 99.5, 99.6, 99.7, 99.8, 99.8, 99.9, 99.9],
        'Waktu Proses (jam)': [2.5, 2.3, 2.1, 2.0, 1.8, 1.7, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0],
        'Kepatuhan SOP (%)': [95, 96, 97, 97, 98, 98, 99, 99, 99, 100, 100, 100],
        'Transaksi Diproses': [850, 920, 980, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450],
        'Penghematan Biaya (jt)': [15, 18, 22, 25, 28, 30, 35, 38, 40, 45, 48, 50]
    })


# ==== 6. Anggaran vs realisasi ====
def generate_budget_data():
    categories = [
        'Bahan Baku', 'Gaji & Tunjangan', 'Listrik & Air', 'Sewa & Gedung',
        'Transportasi & Logistik', 'ATK & Perlengkapan', 'Pemeliharaan & Perbaikan',
        'Pemasaran & Promosi', 'Teknologi & Software', 'Lainnya'
    ]
    budget = [500000000, 350000000, 120000000, 180000000, 150000000,
              80000000, 100000000, 200000000, 90000000, 60000000]
    realization = [480000000, 345000000, 115000000, 175000000, 140000000,
                   75000000, 95000000, 180000000, 85000000, 55000000]

    return pd.DataFrame({
        'Kategori': categories,
        'Anggaran (Rp)': budget,
        'Realisasi (Rp)': realization,
        'Selisih (Rp)': [b - r for b, r in zip(budget, realization)],
        'Persentase': [round(r / b * 100, 1) for b, r in zip(budget, realization)]
    })


# ==== Fungsi utama ====
def load_all_data():
    inventory = generate_inventory(150)
    transactions = generate_inventory_transactions(inventory, 5000)
    financial = generate_financial_transactions(800)
    employees = generate_employee_data(50)
    performance = generate_performance_data()
    budget = generate_budget_data()

    return {
        'inventory': inventory,
        'transactions': transactions,
        'financial': financial,
        'employees': employees,
        'performance': performance,
        'budget': budget
    }


if __name__ == '__main__':
    data = load_all_data()
    for key, df in data.items():
        print(f"\n=== {key.upper()} ===")
        print(f"Shape: {df.shape}")
        print(df.head(3))
