"""Logika pengolahan data. Tidak ada print/input di sini."""
BATAS_HARI = 7        # lama pinjam tanpa denda
TARIF_DENDA = 1000    # rupiah per hari keterlambatan


def hapus_duplikat(data: list[dict]) -> tuple[list[dict], int]:
    """Hapus transaksi dengan id_pinjam yang sama (ambil yang pertama).

    Menggunakan set untuk mencatat id yang sudah terlihat.
    Returns: (data_unik, jumlah_duplikat)
    """
    terlihat: set[str] = set()
    unik = []
    for baris in data:
        if baris["id_pinjam"] in terlihat:
            continue
        terlihat.add(baris["id_pinjam"])
        unik.append(baris)
    return unik, len(data) - len(unik)


def cari_judul(data: list[dict], kata: str) -> list[dict]:
    """Cari transaksi yang judulnya memuat 'kata' (tidak peka huruf besar/kecil)."""
    kata = kata.strip().lower()
    if not kata:
        return []
    return [b for b in data if kata in b["judul"].lower()]


def filter_status(data: list[dict], status: str) -> list[dict]:
    """Ambil transaksi dengan status tertentu."""
    return [b for b in data if b["status"] == status]


def hitung_denda(baris: dict, batas_hari: int = BATAS_HARI,
                 tarif: int = TARIF_DENDA) -> int:
    """Hitung denda satu transaksi. Belum kembali atau tepat waktu = 0."""
    if baris["tgl_kembali"] is None:
        return 0
    lama = (baris["tgl_kembali"] - baris["tgl_pinjam"]).days
    return max(0, lama - batas_hari) * tarif


def daftar_kategori(data: list[dict]) -> set[str]:
    """Kumpulan kategori unik (set comprehension)."""
    return {b["kategori"] for b in data}


def rekap_per_kategori(data: list[dict]) -> dict[str, int]:
    """Jumlah peminjaman per kategori. Data kosong menghasilkan {}."""
    return {kat: sum(1 for b in data if b["kategori"] == kat)
            for kat in sorted(daftar_kategori(data))}


def denda_per_anggota(data: list[dict]) -> dict[str, int]:
    """Total denda per nama anggota; anggota tanpa denda tidak dimasukkan."""
    total: dict[str, int] = {}
    for baris in data:
        total[baris["nama"]] = total.get(baris["nama"], 0) + hitung_denda(baris)
    return {nama: nilai for nama, nilai in total.items() if nilai > 0}


def buat_ringkasan(data: list[dict]) -> dict:
    """Gabungkan hasil analisis menjadi satu dict siap disimpan ke JSON."""
    denda = denda_per_anggota(data)
    return {
        "total_transaksi": len(data),
        "sedang_dipinjam": len(filter_status(data, "dipinjam")),
        "rekap_kategori": rekap_per_kategori(data),
        "denda_per_anggota": denda,
        "total_denda": sum(denda.values()),
    }
