# Aplikasi Pengolah Data Peminjaman Perpustakaan

Aplikasi command line (Python, standard library saja) untuk membaca data peminjaman buku dari CSV,
memvalidasi, mencari/memfilter, merekap, menghitung denda, dan menyimpan hasil ke JSON dan CSV.

## Persyaratan
- Python 3.10 atau lebih baru
- Dependency eksternal: **tidak ada** (hanya standard library: csv, json, argparse, logging, datetime, pathlib)

## Struktur Program
```
perpustakaan_app/
├── main.py              # titik masuk, argparse, logging, penanganan error utama
├── perpus/              # package buatan sendiri
│   ├── __init__.py      # mengekspor fungsi publik
│   ├── validasi.py      # validasi satu baris data
│   ├── io_file.py       # baca CSV, simpan JSON/CSV
│   ├── analisis.py      # pencarian, filter, rekap, denda, hapus duplikat
│   ├── tampilan.py      # mencetak hasil ke layar
│   └── menu.py          # menu interaktif dan input aman
├── data/peminjaman.csv  # contoh input
└── output/              # hasil (dibuat otomatis): ringkasan.json, data_bersih.csv, app.log
```

## Cara Menjalankan
Dari folder `perpustakaan_app/`:

```bash
python main.py                 # menu interaktif
python main.py --otomatis      # jalankan semua analisis tanpa menu
python main.py --file data/peminjaman.csv --otomatis
```

## Format Input (CSV)
Kolom: `id_pinjam,id_anggota,nama,judul,kategori,tgl_pinjam,tgl_kembali,status`
- Tanggal berformat `YYYY-MM-DD`
- `status` = `dipinjam` atau `dikembalikan`
- `tgl_kembali` kosong jika status `dipinjam`

## Output
- Layar: tabel data, rekap kategori, denda per anggota
- `output/ringkasan.json`: ringkasan analisis
- `output/data_bersih.csv`: data yang lolos validasi dan bebas duplikat
- `output/app.log`: catatan proses

## Aturan Denda
Batas pinjam 7 hari, denda Rp 1.000 per hari keterlambatan (diubah di `perpus/analisis.py`).

## Penanganan Error
| Kondisi | Perilaku |
|---|---|
| File tidak ditemukan | Pesan error, program berhenti dengan kode 1 |
| Header CSV kurang kolom | Pesan error, program berhenti dengan kode 1 |
| Baris tidak valid | Baris dilewati dan dilaporkan, program lanjut |
| Duplikat `id_pinjam` | Diambil yang pertama, sisanya dibuang |
| Input menu salah | Diminta mengulang |
| Data kosong | Menampilkan "(tidak ada data)" tanpa crash |
