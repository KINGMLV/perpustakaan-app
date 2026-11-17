"""Titik masuk aplikasi. Jalankan: python main.py [--file PATH] [--otomatis]"""
import argparse
import logging
import sys
from pathlib import Path

from perpus import (DataTidakValidError, baca_csv, hapus_duplikat, cetak_tabel,
                    cetak_rekap, cetak_denda, rekap_per_kategori,
                    denda_per_anggota, buat_ringkasan, simpan_json, simpan_csv)
from perpus.menu import jalankan_menu

FOLDER_OUTPUT = Path("output")


def siapkan_logging() -> None:
    """Catat proses dan error ke output/app.log."""
    FOLDER_OUTPUT.mkdir(exist_ok=True)
    logging.basicConfig(filename=FOLDER_OUTPUT / "app.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s", encoding="utf-8")


def muat_data(path: str) -> list[dict]:
    """Baca, validasi, dan bersihkan duplikat. Mengembalikan data siap olah."""
    data, error = baca_csv(path)
    for pesan in error:
        print(f"[DILEWATI] {pesan}")
        logging.warning(pesan)
    data, duplikat = hapus_duplikat(data)
    print(f"Data valid: {len(data)} | baris bermasalah: {len(error)} | duplikat dibuang: {duplikat}")
    logging.info("Data dimuat: %d valid, %d error, %d duplikat", len(data), len(error), duplikat)
    return data


def mode_otomatis(data: list[dict]) -> None:
    """Jalankan semua analisis tanpa input pengguna (untuk bukti output)."""
    cetak_tabel(data)
    cetak_rekap(rekap_per_kategori(data))
    cetak_denda(denda_per_anggota(data))
    simpan_json(buat_ringkasan(data), FOLDER_OUTPUT / "ringkasan.json")
    simpan_csv(data, FOLDER_OUTPUT / "data_bersih.csv")
    print(f"\nLaporan disimpan di folder {FOLDER_OUTPUT}/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Pengolah data peminjaman perpustakaan")
    parser.add_argument("--file", default="data/peminjaman.csv", help="lokasi file CSV")
    parser.add_argument("--otomatis", action="store_true", help="jalankan tanpa menu")
    args = parser.parse_args()

    siapkan_logging()
    try:
        data = muat_data(args.file)
    except FileNotFoundError as err:
        print(f"Error: {err}")
        logging.error(err)
        return 1
    except DataTidakValidError as err:
        print(f"Error format data: {err}")
        logging.error(err)
        return 1

    if args.otomatis:
        mode_otomatis(data)
    else:
        jalankan_menu(data, FOLDER_OUTPUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
