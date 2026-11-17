"""Menjalankan skenario pengujian aplikasi dan menampilkan LULUS/GAGAL.

Jalankan dari folder perpustakaan_app:  python uji_otomatis.py
Skenario debugging (Soal 6.2) dilakukan manual, tidak ada di sini.
"""
import subprocess
import sys
from pathlib import Path

FOLDER_UJI = Path("data/uji")
HEADER = "id_pinjam,id_anggota,nama,judul,kategori,tgl_pinjam,tgl_kembali,status\n"


def siapkan_file_uji() -> None:
    """Buat file CSV kecil untuk pengujian."""
    FOLDER_UJI.mkdir(parents=True, exist_ok=True)
    (FOLDER_UJI / "kosong.csv").write_text(HEADER, encoding="utf-8")
    (FOLDER_UJI / "uji.csv").write_text(
        HEADER
        + "P100,A10,Uji,Buku Uji,Teknologi,2026-10-01,2026-10-08,dikembalikan\n"
        + "P101,A10,Uji,Buku Uji 2,Teknologi,2026-10-01,2026-10-09,dikembalikan\n",
        encoding="utf-8")
    (FOLDER_UJI / "salah.csv").write_text("a,b\n1,2\n", encoding="utf-8")


def jalankan(args: list[str], stdin: str = "") -> subprocess.CompletedProcess:
    """Jalankan main.py dengan argumen dan input tertentu."""
    return subprocess.run([sys.executable, "main.py", *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8")


SKENARIO = [
    ("1. Data normal", ["--otomatis"], "", 0,
     ["Data valid: 8 | baris bermasalah: 4 | duplikat dibuang: 1",
      "Teknologi   : 4", "Budi    : Rp 8.000", "Sari    : Rp 6.000", "Lina    : Rp 11.000"]),
    ("2. Edge: CSV hanya header", ["--file", "data/uji/kosong.csv", "--otomatis"], "", 0,
     ["(tidak ada data)", "(tidak ada denda)"]),
    ("3. Edge: batas 7 hari", ["--file", "data/uji/uji.csv", "--otomatis"], "", 0,
     ["Uji     : Rp 1.000"]),
    ("4. File tidak ditemukan", ["--file", "data/tidak_ada.csv"], "", 1,
     ["Error: File tidak ditemukan"]),
    ("5. Header salah", ["--file", "data/uji/salah.csv"], "", 1,
     ["Error format data: Header CSV kurang kolom"]),
    ("6. Menu interaktif", [], "9\n2\nalgo\n2\nzzz\n3\nbatal\ndipinjam\n6\n0\n", 0,
     ["Input tidak valid", "Hasil pencarian 'algo'", "P012", "Hasil pencarian 'zzz'",
      "(tidak ada data)", "Status: dipinjam", "Laporan disimpan", "Terima kasih."]),
]


def main() -> int:
    siapkan_file_uji()
    gagal = 0
    for nama, args, stdin, kode, harus_ada in SKENARIO:
        print("=" * 70)
        print(f"{nama}   ->   python main.py {' '.join(args)}")
        print("=" * 70)
        hasil = jalankan(args, stdin)
        print(hasil.stdout.rstrip())
        if hasil.stderr.strip():
            print(hasil.stderr.rstrip())
        kurang = [t for t in harus_ada if t not in hasil.stdout]
        if hasil.returncode != kode:
            kurang.append(f"exit code {kode} (didapat {hasil.returncode})")
        if kurang:
            gagal += 1
            print(f"\n>>> GAGAL. Tidak ditemukan: {kurang}\n")
        else:
            print("\n>>> LULUS\n")
    print("=" * 70)
    print(f"RINGKASAN: {len(SKENARIO) - gagal} lulus, {gagal} gagal dari {len(SKENARIO)} skenario")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
