"""Unit test fungsi inti. Jalankan: python -m unittest discover -s tests -v"""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from perpus import (DataTidakValidError, validasi_baris, hapus_duplikat, cari_judul,
                    filter_status, hitung_denda, rekap_per_kategori, denda_per_anggota)


def buat(id_="P1", nama="Budi", judul="Python", kat="Teknologi",
         pinjam=date(2026, 10, 1), kembali=date(2026, 10, 6), status="dikembalikan"):
    return {"id_pinjam": id_, "nama": nama, "judul": judul, "kategori": kat,
            "tgl_pinjam": pinjam, "tgl_kembali": kembali, "status": status}


class TestHitungDenda(unittest.TestCase):
    def test_tepat_waktu(self):
        self.assertEqual(hitung_denda(buat(kembali=date(2026, 10, 8))), 0)  # 7 hari

    def test_terlambat_satu_hari(self):
        self.assertEqual(hitung_denda(buat(kembali=date(2026, 10, 9))), 1000)

    def test_belum_dikembalikan(self):
        self.assertEqual(hitung_denda(buat(kembali=None, status="dipinjam")), 0)


class TestData(unittest.TestCase):
    def test_hapus_duplikat(self):
        unik, jumlah = hapus_duplikat([buat("P1"), buat("P1"), buat("P2")])
        self.assertEqual((len(unik), jumlah), (2, 1))

    def test_cari_judul_tidak_peka_huruf(self):
        self.assertEqual(len(cari_judul([buat(judul="Algoritma")], "ALGO")), 1)

    def test_cari_kata_kosong(self):
        self.assertEqual(cari_judul([buat()], "  "), [])

    def test_filter_status(self):
        data = [buat(status="dikembalikan"), buat("P2", kembali=None, status="dipinjam")]
        self.assertEqual(len(filter_status(data, "dipinjam")), 1)

    def test_rekap_kosong(self):
        self.assertEqual(rekap_per_kategori([]), {})

    def test_rekap_kategori(self):
        data = [buat("P1", kat="Novel"), buat("P2", kat="Novel"), buat("P3")]
        self.assertEqual(rekap_per_kategori(data), {"Novel": 2, "Teknologi": 1})

    def test_denda_per_anggota_hanya_yang_didenda(self):
        data = [buat("P1", nama="A", kembali=date(2026, 10, 10)), buat("P2", nama="B")]
        self.assertEqual(denda_per_anggota(data), {"A": 2000})


class TestValidasi(unittest.TestCase):
    dasar = {"id_pinjam": "P1", "id_anggota": "A1", "nama": "Budi", "judul": "X",
             "kategori": "K", "tgl_pinjam": "2026-10-01", "tgl_kembali": "2026-10-05",
             "status": "dikembalikan"}

    def test_baris_valid(self):
        self.assertEqual(validasi_baris(self.dasar)["tgl_pinjam"], date(2026, 10, 1))

    def test_nama_kosong(self):
        with self.assertRaises(DataTidakValidError):
            validasi_baris({**self.dasar, "nama": ""})

    def test_status_salah(self):
        with self.assertRaises(DataTidakValidError):
            validasi_baris({**self.dasar, "status": "selesai"})

    def test_tanggal_tidak_valid(self):
        with self.assertRaises(DataTidakValidError):
            validasi_baris({**self.dasar, "tgl_pinjam": "2026-31-10"})

    def test_kembali_sebelum_pinjam(self):
        with self.assertRaises(DataTidakValidError):
            validasi_baris({**self.dasar, "tgl_kembali": "2026-09-01"})


if __name__ == "__main__":
    unittest.main()
