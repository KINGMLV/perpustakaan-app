"""Membaca dan menyimpan file CSV/JSON."""
import csv
import json
from pathlib import Path

from .validasi import KOLOM_WAJIB, DataTidakValidError, validasi_baris


def baca_csv(path) -> tuple[list[dict], list[str]]:
    """Baca CSV peminjaman dan validasi tiap baris.

    Args:
        path: lokasi file CSV.
    Returns:
        (data_valid, daftar_error) - baris bermasalah dicatat, tidak menghentikan program.
    Raises:
        FileNotFoundError: file tidak ada.
        DataTidakValidError: header kolom tidak lengkap.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    data, error = [], []
    with open(path, newline="", encoding="utf-8-sig") as file:
        pembaca = csv.DictReader(file)
        kurang = set(KOLOM_WAJIB) - set(pembaca.fieldnames or [])
        if kurang:
            raise DataTidakValidError(f"Header CSV kurang kolom: {sorted(kurang)}")
        for no, baris in enumerate(pembaca, start=2):  # baris 1 = header
            try:
                data.append(validasi_baris(baris))
            except DataTidakValidError as err:
                error.append(f"Baris {no}: {err}")
    return data, error


def _serialisasi(baris: dict) -> dict:
    """Ubah date menjadi teks ISO agar bisa ditulis ke JSON/CSV."""
    return {k: (v.isoformat() if hasattr(v, "isoformat") else v)
            for k, v in baris.items()}


def simpan_json(isi: dict, path) -> None:
    """Simpan dict ke file JSON (folder dibuat otomatis)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(isi, file, indent=2, ensure_ascii=False)


def simpan_csv(data: list[dict], path) -> None:
    """Simpan daftar transaksi ke CSV. Data kosong tetap menghasilkan header."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        penulis = csv.DictWriter(file, fieldnames=KOLOM_WAJIB)
        penulis.writeheader()
        for baris in data:
            penulis.writerow(_serialisasi(baris))
