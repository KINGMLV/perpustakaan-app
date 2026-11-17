"""Menu interaktif command line dan input pengguna yang aman."""
from .analisis import (cari_judul, filter_status, rekap_per_kategori,
                       denda_per_anggota, buat_ringkasan)
from .io_file import simpan_json, simpan_csv
from .tampilan import cetak_tabel, cetak_rekap, cetak_denda

MENU = """
=== Aplikasi Peminjaman Perpustakaan ===
1. Tampilkan semua data
2. Cari berdasarkan judul
3. Filter berdasarkan status
4. Rekap per kategori
5. Denda per anggota
6. Simpan laporan (JSON + CSV)
0. Keluar"""


def baca_pilihan(prompt: str, valid: set[str]) -> str:
    """Minta input sampai nilainya termasuk 'valid'. EOF dianggap keluar ('0')."""
    while True:
        try:
            nilai = input(prompt).strip().lower()
        except EOFError:
            return "0"
        if nilai in valid:
            return nilai
        print(f"Input tidak valid. Pilihan: {', '.join(sorted(valid))}")


def jalankan_menu(data: list[dict], folder_output) -> None:
    """Loop menu utama sampai pengguna memilih keluar."""
    while True:
        print(MENU)
        pilihan = baca_pilihan("Pilih menu: ", {"0", "1", "2", "3", "4", "5", "6"})
        if pilihan == "0":
            print("Terima kasih.")
            return
        if pilihan == "1":
            cetak_tabel(data)
        elif pilihan == "2":
            kata = input("Kata kunci judul: ")
            cetak_tabel(cari_judul(data, kata), f"Hasil pencarian '{kata.strip()}'")
        elif pilihan == "3":
            status = baca_pilihan("Status (dipinjam/dikembalikan): ",
                                  {"dipinjam", "dikembalikan"})
            cetak_tabel(filter_status(data, status), f"Status: {status}")
        elif pilihan == "4":
            cetak_rekap(rekap_per_kategori(data))
        elif pilihan == "5":
            cetak_denda(denda_per_anggota(data))
        elif pilihan == "6":
            simpan_json(buat_ringkasan(data), folder_output / "ringkasan.json")
            simpan_csv(data, folder_output / "data_bersih.csv")
            print(f"Laporan disimpan di folder {folder_output}")
