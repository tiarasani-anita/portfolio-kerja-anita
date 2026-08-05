"""
Script kecil buat ngebersihin cache Streamlit dan ngecek syntax semua file .py.
Jalankan: python fix_deprecation.py
"""
import ast
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))


def clean_streamlit_cache():
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "streamlit")
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir)
        print(f"Cache Streamlit dihapus: {cache_dir}")
    else:
        print("Cache Streamlit tidak ditemukan, lanjut...")


def check_syntax():
    ok = True
    for folder, _, files in os.walk(ROOT):
        if 'venv' in folder or '__pycache__' in folder:
            continue
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(folder, f)
                try:
                    with open(path, encoding='utf-8') as fh:
                        ast.parse(fh.read())
                    print(f'OK: {path}')
                except SyntaxError as e:
                    ok = False
                    print(f'ERROR: {path} -> {e}')
    return ok


if __name__ == '__main__':
    clean_streamlit_cache()
    print('--- Cek syntax ---')
    if check_syntax():
        print('\nSemua file Python valid.')
    else:
        print('\nAda file Python yang bermasalah, cek di atas.')
