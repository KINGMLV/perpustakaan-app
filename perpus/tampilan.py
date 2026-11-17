"""Fungsi untuk mencetak hasil ke layar (hanya tampilan)."""


def cetak_tabel(data: list[dict], judul: str = "Data peminjaman") -> None:
    """Cetak daftar transaksi. Data kosong menampilkan pesan."""
    print(f"\n{judul}")
    if not data:
        print("  (tidak ada data)")
        return
    for no, b in enumerate(data, start=1):
        kembali = b["tgl_kembali"].isoformat() if b["tgl_kembali"] else "-"
        print(f"{no:>2}. {b['id_pinjam']} | {b['nama']:<8} | {b['judul']:<22} | "
              f"{b['tgl_pinjam'].isoformat()} -> {kembali} | {b['status']}")


def cetak_rekap(rekap: dict[str, int]) -> None:
    """Cetak rekap per kategori."""
    print("\nRekap peminjaman per kategori")
    if not rekap:
        print("  (tidak ada data)")
        return
    for kategori, jumlah in rekap.items():
        print(f"  {kategori:<12}: {jumlah}")


def cetak_denda(denda: dict[str, int]) -> None:
    """Cetak total denda per anggota."""
    print("\nDenda keterlambatan")
    if not denda:
        print("  (tidak ada denda)")
        return
    for nama, nilai in denda.items():
        print(f"  {nama:<8}: Rp {nilai:,}".replace(",", "."))
