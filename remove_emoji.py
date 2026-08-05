# Script sekali pakai: hapus semua emoji dari file proyek.
import re
import pathlib

# Pola emoji Unicode yang umum
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2600-\u27BF"
    "\uFE0F"  # variation selector
    "\u200D"  # zero width joiner
    "]+",
    flags=re.UNICODE,
)

files = [
    "app.py",
    "api/index.py",
    "data/generate_data.py",
    "utils/formulas.py",
    "utils/charts.py",
    "README.md",
    "TODO.md",
    ".streamlit/config.toml",
    "vercel.json",
    "requirements.txt",
    "fix_deprecation.py",
]

for fname in files:
    path = pathlib.Path(fname)
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")

    # Hapus emoji
    cleaned = emoji_pattern.sub("", text)

    # Rapikan spasi ganda yang muncul karena emoji dihapus
    cleaned = re.sub(r" {2,}", " ", cleaned)

    # Rapikan judul yang jadi kosong/aneh
    cleaned = re.sub(r"^(#{1,6})\s+", r"\1 ", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^-\s+", "- ", cleaned, flags=re.MULTILINE)

    # Hapus trailing whitespace
    cleaned = re.sub(r" +$", "", cleaned, flags=re.MULTILINE)

    path.write_text(cleaned, encoding="utf-8")
    print(f"Bersih: {fname}")

print("Selesai menghapus emoji.")
