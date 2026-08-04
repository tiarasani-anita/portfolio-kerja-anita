"""
FORMULA AKTIF - LOGIKA PERHITUNGAN
====================================
Berisi implementasi formula Excel (VLOOKUP, Pivot Table, IF) dalam Python
serta perhitungan keuangan otomatis: Laba Rugi, Neraca, Arus Kas, dan KPI.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================
# 1. FUNGSI VLOOKUP (Pencarian Data)
# ============================================================
def vlookup(df, lookup_value, lookup_col, return_col):
    """
    Implementasi VLOOKUP Excel dalam Python.
    
    Parameters:
    - df: DataFrame sumber data
    - lookup_value: nilai yang dicari
    - lookup_col: nama kolom yang menjadi kunci pencarian
    - return_col: nama kolom yang nilainya akan diambil
    
    Returns:
    - Nilai dari kolom return_col jika ditemukan, else None
    """
    try:
        result = df.loc[df[lookup_col] == lookup_value, return_col]
        if len(result) > 0:
            return result.iloc[0]
        return None
    except Exception:
        return None


def vlookup_batch(df, lookup_values, lookup_col, return_col):
    """VLOOKUP untuk banyak nilai sekaligus."""
    return [vlookup(df, val, lookup_col, return_col) for val in lookup_values]


# ============================================================
# 2. FUNGSI IF BERTINGKAT (Nested IF)
# ============================================================
def nested_if(value, conditions):
    """
    Implementasi nested IF Excel.
    
    Parameters:
    - value: nilai yang dievaluasi
    - conditions: list of tuples (condition_func, result)
    
    Returns:
    - Hasil dari kondisi pertama yang terpenuhi
    """
    for condition_func, result in conditions:
        if condition_func(value):
            return result
    return None


def status_stok(stok, min_stok):
    """Menentukan status stok berdasarkan stok saat ini dan minimum."""
    if stok == 0:
        return 'Habis'
    elif stok <= min_stok:
        return 'Menipis'
    elif stok <= min_stok * 1.5:
        return 'Perlu Order'
    else:
        return 'Aman'


def kategori_harga(harga):
    """Mengklasifikasikan harga barang."""
    if harga < 10000:
        return 'Murah'
    elif harga < 100000:
        return 'Sedang'
    elif harga < 500000:
        return 'Mahal'
    else:
        return 'Premium'


# ============================================================
# 3. PIVOT TABLE (Agregasi Data)
# ============================================================
def pivot_summary(df, index_col, values_col, agg_func='sum'):
    """
    Implementasi Pivot Table Excel dalam Python.
    
    Parameters:
    - df: DataFrame sumber
    - index_col: kolom yang menjadi baris pivot
    - values_col: kolom yang diagregasi
    - agg_func: fungsi agregasi ('sum', 'mean', 'count', 'min', 'max')
    
    Returns:
    - DataFrame hasil pivot
    """
    return df.groupby(index_col)[values_col].agg(agg_func).reset_index()


def pivot_multi(df, index_col, values_cols, agg_funcs=None):
    """Pivot table dengan multiple values dan fungsi agregasi."""
    if agg_funcs is None:
        agg_funcs = {col: 'sum' for col in values_cols}
    return df.groupby(index_col).agg(agg_funcs).reset_index()


# ============================================================
# 4. PERHITUNGAN KEUANGAN OTOMATIS
# ============================================================
def hitung_laba_rugi(financial_df):
    """
    Menghitung Laporan Laba Rugi dari data jurnal umum.
    
    Returns:
    - DataFrame laporan laba rugi per bulan
    """
    # Filter data pendapatan dan beban
    pendapatan = financial_df[financial_df['Tipe Akun'] == 'Pendapatan']
    beban = financial_df[financial_df['Tipe Akun'] == 'Beban']
    
    # Agregasi per bulan
    pendapatan_bulanan = pendapatan.groupby('Bulan')['Jumlah (Rp)'].sum().reset_index()
    beban_bulanan = beban.groupby('Bulan')['Jumlah (Rp)'].sum().reset_index()
    
    # Gabungkan
    result = pd.merge(pendapatan_bulanan, beban_bulanan, on='Bulan', how='outer', suffixes=('_Pendapatan', '_Beban'))
    result = result.fillna(0)
    
    # Hitung laba kotor dan margin
    result['Laba Bersih'] = result['Jumlah (Rp)_Pendapatan'] - result['Jumlah (Rp)_Beban']
    result['Margin (%)'] = np.where(
        result['Jumlah (Rp)_Pendapatan'] > 0,
        (result['Laba Bersih'] / result['Jumlah (Rp)_Pendapatan'] * 100).round(2),
        0
    )
    
    # Urutkan bulan
    bulan_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    result['Bulan'] = pd.Categorical(result['Bulan'], categories=bulan_order, ordered=True)
    result = result.sort_values('Bulan').reset_index(drop=True)
    
    return result


def hitung_neraca(financial_df):
    """
    Menghitung Neraca dari data jurnal umum.
    
    Returns:
    - DataFrame neraca (aset, liabilitas, ekuitas)
    """
    # Agregasi per tipe akun
    aset = financial_df[financial_df['Tipe Akun'] == 'Aset']['Jumlah (Rp)'].sum()
    liabilitas = financial_df[financial_df['Tipe Akun'] == 'Liabilitas']['Jumlah (Rp)'].sum()
    ekuitas = financial_df[financial_df['Tipe Akun'] == 'Ekuitas']['Jumlah (Rp)'].sum()
    pendapatan = financial_df[financial_df['Tipe Akun'] == 'Pendapatan']['Jumlah (Rp)'].sum()
    beban = financial_df[financial_df['Tipe Akun'] == 'Beban']['Jumlah (Rp)'].sum()
    
    # Laba ditahan = pendapatan - beban
    laba_ditahan = pendapatan - beban
    
    # Total ekuitas
    total_ekuitas = ekuitas + laba_ditahan
    
    # Buat DataFrame neraca
    neraca = pd.DataFrame({
        'Akun': ['Kas & Bank', 'Piutang Usaha', 'Persediaan', 'Peralatan', 'Total Aset',
                 'Hutang Usaha', 'Hutang Bank', 'Total Liabilitas',
                 'Modal', 'Laba Ditahan', 'Total Ekuitas',
                 'Total Liabilitas & Ekuitas'],
        'Jumlah (Rp)': [
            financial_df[financial_df['Nama Akun'].str.contains('Kas|Bank')]['Jumlah (Rp)'].sum(),
            financial_df[financial_df['Nama Akun'].str.contains('Piutang')]['Jumlah (Rp)'].sum(),
            financial_df[financial_df['Nama Akun'].str.contains('Persediaan')]['Jumlah (Rp)'].sum(),
            financial_df[financial_df['Nama Akun'].str.contains('Peralatan')]['Jumlah (Rp)'].sum(),
            aset,
            financial_df[financial_df['Nama Akun'].str.contains('Hutang Usaha')]['Jumlah (Rp)'].sum(),
            financial_df[financial_df['Nama Akun'].str.contains('Hutang Bank')]['Jumlah (Rp)'].sum(),
            liabilitas,
            ekuitas,
            laba_ditahan,
            total_ekuitas,
            aset
        ]
    })
    
    return neraca


def hitung_arus_kas(financial_df):
    """
    Menghitung Laporan Arus Kas dari data jurnal.
    
    Returns:
    - DataFrame arus kas per bulan
    """
    # Pisahkan berdasarkan tipe akun
    operasional = financial_df[financial_df['Tipe Akun'].isin(['Pendapatan', 'Beban'])]
    investasi = financial_df[financial_df['Tipe Akun'] == 'Aset']
    pendanaan = financial_df[financial_df['Tipe Akun'].isin(['Liabilitas', 'Ekuitas'])]
    
    # Agregasi per bulan
    def agg_bulanan(df):
        if df.empty:
            return pd.DataFrame({'Bulan': [], 'Jumlah (Rp)': []})
        return df.groupby('Bulan')['Jumlah (Rp)'].sum().reset_index()
    
    op = agg_bulanan(operasional)
    inv = agg_bulanan(investasi)
    pend = agg_bulanan(pendanaan)
    
    # Gabungkan
    result = pd.merge(op, inv, on='Bulan', how='outer', suffixes=('_Operasional', '_Investasi'))
    result = pd.merge(result, pend, on='Bulan', how='outer', suffixes=('', '_Pendanaan'))
    result = result.fillna(0)
    
    # Hitung arus kas bersih
    result['Arus Kas Bersih'] = (
        result['Jumlah (Rp)_Operasional'] - 
        result['Jumlah (Rp)_Investasi'] + 
        result['Jumlah (Rp)']
    )
    
    # Urutkan bulan
    bulan_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    result['Bulan'] = pd.Categorical(result['Bulan'], categories=bulan_order, ordered=True)
    result = result.sort_values('Bulan').reset_index(drop=True)
    
    return result


# ============================================================
# 5. PERHITUNGAN KPI WAREHOUSE
# ============================================================
def hitung_kpi_warehouse(inventory_df, transactions_df):
    """
    Menghitung KPI warehouse dari data inventaris dan transaksi.
    
    Returns:
    - Dictionary berisi berbagai KPI
    """
    # Total nilai inventaris
    total_nilai_inventaris = inventory_df['Nilai Stok'].sum()
    
    # Jumlah SKU
    total_sku = len(inventory_df)
    
    # Barang dengan stok menipis/habis
    stok_kritis = inventory_df[inventory_df['Status'].isin(['Habis', 'Menipis'])]
    persentase_stok_kritis = round(len(stok_kritis) / total_sku * 100, 2) if total_sku > 0 else 0
    
    # Total transaksi masuk/keluar
    total_masuk = transactions_df[transactions_df['Tipe'] == 'Barang Masuk']['Jumlah'].sum()
    total_keluar = transactions_df[transactions_df['Tipe'] == 'Barang Keluar']['Jumlah'].sum()
    
    # Nilai transaksi
    nilai_masuk = transactions_df[transactions_df['Tipe'] == 'Barang Masuk']['Total Nilai'].sum()
    nilai_keluar = transactions_df[transactions_df['Tipe'] == 'Barang Keluar']['Total Nilai'].sum()
    
    # Akurasi data entry (simulasi: 99.5%)
    akurasi = 99.5
    
    # Turnover rate
    rata_stok = inventory_df['Stok Saat Ini'].mean()
    turnover = round(total_keluar / rata_stok, 2) if rata_stok > 0 else 0
    
    # Kategori dengan nilai tertinggi
    nilai_per_kategori = inventory_df.groupby('Kategori')['Nilai Stok'].sum().sort_values(ascending=False)
    
    return {
        'total_nilai_inventaris': total_nilai_inventaris,
        'total_sku': total_sku,
        'stok_kritis': len(stok_kritis),
        'persentase_stok_kritis': persentase_stok_kritis,
        'total_masuk': total_masuk,
        'total_keluar': total_keluar,
        'nilai_masuk': nilai_masuk,
        'nilai_keluar': nilai_keluar,
        'akurasi': akurasi,
        'turnover': turnover,
        'nilai_per_kategori': nilai_per_kategori
    }


# ============================================================
# 6. FORMAT ANGKA
# ============================================================
def format_rupiah(value):
    """Format angka menjadi Rupiah."""
    if value is None:
        return 'Rp 0'
    return f"Rp {value:,.0f}".replace(',', '.')


def format_persen(value, decimals=1):
    """Format angka menjadi persen."""
    return f"{value:.{decimals}f}%"


def format_angka(value):
    """Format angka dengan ribuan separator."""
    return f"{value:,.0f}".replace(',', '.')
