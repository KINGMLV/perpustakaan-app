"""Validasi satu baris data peminjaman (defensive programming)."""
from datetime import datetime, date

KOLOM_WAJIB = ("id_pinjam", "id_anggota", "nama", "judul",
               "kategori", "tgl_pinjam", "tgl_kembali", "status")
STATUS_VALID = {"dipinjam", "dikembalikan"}
FORMAT_TANGGAL = "%Y-%m-%d"


class DataTidakValidError(ValueError):
    """Dilempar saat data/baris tidak memenuhi aturan."""


def parse_tanggal(teks: str) -> date:
    """Ubah teks 'YYYY-MM-DD' menjadi objek date.

    Raises:
        DataTidakValidError: jika format tanggal salah.
    """
    try:
        return datetime.strptime(teks.strip(), FORMAT_TANGGAL).date()
    except ValueError as err:
        raise DataTidakValidError(f"Tanggal tidak valid: {teks!r}") from err


def validasi_baris(baris: dict) -> dict:
    """Validasi dan bersihkan satu baris CSV.

    Args:
        baris: dict mentah dari csv.DictReader.
    Returns:
        dict bersih; tgl_pinjam/tgl_kembali bertipe date (tgl_kembali bisa None).
    Raises:
        DataTidakValidError: jika ada field kosong, status salah, atau tanggal tidak logis.
    """
    bersih = {k: (baris.get(k) or "").strip() for k in KOLOM_WAJIB}

    for kolom in ("id_pinjam", "id_anggota", "nama", "judul", "kategori"):
        if not bersih[kolom]:
            raise DataTidakValidError(f"Kolom '{kolom}' tidak boleh kosong")

    bersih["status"] = bersih["status"].lower()
    if bersih["status"] not in STATUS_VALID:
        raise DataTidakValidError(f"Status tidak dikenal: {bersih['status']!r}")

    bersih["tgl_pinjam"] = parse_tanggal(bersih["tgl_pinjam"])

    if bersih["status"] == "dikembalikan":
        if not bersih["tgl_kembali"]:
            raise DataTidakValidError("Status dikembalikan tetapi tgl_kembali kosong")
        bersih["tgl_kembali"] = parse_tanggal(bersih["tgl_kembali"])
        if bersih["tgl_kembali"] < bersih["tgl_pinjam"]:
            raise DataTidakValidError("tgl_kembali lebih awal dari tgl_pinjam")
    else:
        bersih["tgl_kembali"] = None
    return bersih
