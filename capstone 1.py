#  Diagram 1 — Flow Menu Utama
#                 +----------------------+
#                 |     Main Menu        |
#                 +----------+-----------+
#                            |
#         +------------------+------------------+
#         |                                     |
# +-------v-------+                     +--------v--------+
# |   Mode Admin  |                     |  Mode Pembeli   |
# +-------+-------+                     +--------+--------+
#         |                                     |
#         |                                     |
#  (Masuk Menu Admin)                   (Masuk Menu Pembeli)

# Diagram 2 — Flow Mode Admin
# Mode Admin
# |
# +-- Read (admin_read_menu)
# |   +-- option 1: tampilkan_semua_barang()
# |   +-- option 2: cari_barang_by_kode() -> tampilkan_detail_barang()
# |
# +-- Create (admin_create_menu)
# |   +-- input kode, nama, stok, harga, kategori
# |   +-- validasi kode unik -> daftar_barang.append(dict)
# |
# +-- Update (admin_update_menu)
# |   +-- cari barang -> pilih kolom -> validasi -> barang[field] = new_value
# |
# +-- Delete (admin_delete_menu)
# |   +-- cari barang -> konfirmasi -> daftar_barang.remove(barang)
# |
# +-- Riwayat (admin_lihat_riwayat)
#     +-- tampilkan riwayat_transaksi & pembeli_unik

# Diagram 3 — Flow Mode Pembeli
# Mode Pembeli
# |
# +-- Create Profile (pembeli_buat_profile)
# |   +-- input nama, email -> profil_pembeli = {..}
# |
# +-- Read Barang (pembeli_tampilkan_barang_tersedia)
# |   +-- filter daftar_barang where stok > 0
# |
# +-- Tambah ke Keranjang (pembeli_tambah_ke_keranjang)
# |   +-- input kode -> cari_barang_by_kode
# |   +-- validasi stok dan qty
# |   +-- gabungkan_item_di_keranjang() -> update qty & subtotal
# |
# +-- Hapus dari Keranjang (pembeli_delete_dari_keranjang)
# |   +-- tampilkan_keranjang -> input index -> del keranjang[index]
# |
# +-- Checkout (pembeli_checkout)
#     +-- pastikan profil & keranjang tidak kosong
#     +-- hitung total (hitung_total_keranjang)
#     +-- pilih metode bayar
#     +-- tampilkan struk
#     +-- cek stok final
#     +-- minta pembayaran (minta_int min_value=0)
#     +-- jika cukup: kurangi stok, simpan riwayat (deepcopy), add pembeli_unik, keranjang.clear()



# ============================================
#  DATA COLLECTION
# ============================================
import copy
KATEGORI_BARANG = ("Alat Tulis", "Buku / Bacaan", "Lainnya")

daftar_barang = [
    {"kode": "BRG001", "nama": "Pulpen",    "stok": 20, "harga": 7000, "kategori": "Alat Tulis"},
    {"kode": "BRG002", "nama": "Buku",      "stok": 15, "harga": 10000, "kategori": "Buku / Bacaan"},
    {"kode": "BRG003", "nama": "Penghapus", "stok": 10, "harga": 6000, "kategori": "Alat Tulis"},
    {"kode": "BRG004", "nama": "Baju",      "stok": 30, "harga": 20000, "kategori": "Lainnya"},
]

keranjang = []
profil_pembeli = None
riwayat_transaksi = []
pembeli_unik = set()


# ============================================
#  FUNGSI HELPER UMUM
# ============================================

def minta_int(pesan, min_value=None):
    """Minta input integer, opsional validasi min_value."""
    while True:
        nilai = input(pesan).strip()
        if nilai.lstrip('-').isdigit():
            iv = int(nilai)
            if min_value is not None and iv < min_value:
                print(f"Nilai harus >= {min_value}.")
                continue
            return iv
        else:
            print("Input harus berupa angka bulat (contoh: 0, 1, 12). Coba lagi.")


def minta_string_nonempty(pesan):
    """Minta input string tidak kosong."""
    while True:
        s = input(pesan).strip()
        if s == "":
            print("⚠️ Input tidak boleh kosong. Coba lagi.")
            continue
        return s


def cari_barang_by_kode(kode):
    """Cari barang case-insensitive berdasarkan kode. Kembalikan dict atau None."""
    if kode is None:
        return None
    kode = kode.strip().upper()
    for barang in daftar_barang:
        if barang["kode"].upper() == kode:
            return barang
    return None


def tampilkan_semua_barang():
    """Tampilkan semua barang."""
    if not daftar_barang:
        print("\n[INFO] Data does not exist\n")
        return
    print("\n=== DAFTAR BARANG TOKO ===")
    print("Kode   | Nama       | Stok | Harga   | Kategori")
    print("------------------------------------------------")
    for b in daftar_barang:
        print(f"{b['kode']:6} | {b['nama']:10} | {b['stok']:4} | {b['harga']:7} | {b['kategori']}")
    print()


def tampilkan_detail_barang(barang):
    """Tampilkan detail satu barang."""
    if not barang:
        print("[INFO] Barang tidak ditemukan.")
        return
    print("\n=== DETAIL BARANG ===")
    print(f"Kode     : {barang['kode']}")
    print(f"Nama     : {barang['nama']}")
    print(f"Stok     : {barang['stok']}")
    print(f"Harga    : {barang['harga']}")
    print(f"Kategori : {barang.get('kategori', '')}\n")


def pilih_kategori():
    """Pilih kategori dari tuple KATEGORI_BARANG."""
    print("\nPilih Kategori Barang:")
    for i, kat in enumerate(KATEGORI_BARANG, start=1):
        print(f"{i}. {kat}")
    pilih = minta_int("Masukkan nomor kategori: ", min_value=1)
    if 1 <= pilih <= len(KATEGORI_BARANG):
        return KATEGORI_BARANG[pilih - 1]
    else:
        print("[INFO] Pilihan kategori tidak valid, gunakan 'Lainnya'.")
        return "Lainnya"


def hitung_total_keranjang():
    """Hitung total keranjang."""
    return sum(item["subtotal"] for item in keranjang)


def tampilkan_ringkasan_keranjang():
    """Tampilkan ringkasan keranjang."""
    if not keranjang:
        print("\n[INFO] Keranjang masih kosong\n")
        return
    total_items = len(keranjang)
    total_qty = sum(item["qty"] for item in keranjang)
    total_price = hitung_total_keranjang()
    print("\n=== RINGKASAN KERANJANG ===")
    print(f"Jumlah baris (produk berbeda) : {total_items}")
    print(f"Total kuantitas               : {total_qty}")
    print(f"Total harga                   : {total_price}")
    print("==============================\n")


def gabungkan_item_di_keranjang(kode, nama, qty, harga):
    """Gabungkan qty jika kode sudah ada di keranjang, jika tidak append baru."""
    for item in keranjang:
        if item["kode"].upper() == kode.upper():
            item["qty"] += qty
            item["subtotal"] = item["qty"] * item["harga"]
            return
    keranjang.append({
        "kode": kode,
        "nama": nama,
        "qty": qty,
        "harga": harga,
        "subtotal": qty * harga
    })


# ============================================
#  MODE ADMIN – CRUD BARANG
# ============================================

def admin_read_menu():
    """Sub-menu Read untuk admin."""
    while True:
        print("\n===== [ADMIN] READ MENU (A) =====")
        print("1. Tampilkan semua data")
        print("2. Tampilkan data berdasarkan KODE barang")
        print("3. Kembali ke Menu Admin")
        pilihan = input("Pilih (1-3): ").strip()

        if pilihan == "1":
            tampilkan_semua_barang()
        elif pilihan == "2":
            if not daftar_barang:
                print("\n[INFO] Data does not exist\n")
                continue
            kode = input("Masukkan KODE barang: ").strip().upper()
            barang = cari_barang_by_kode(kode)
            if barang is None:
                print("\n[INFO] Data does not exist\n")
            else:
                tampilkan_detail_barang(barang)
        elif pilihan == "3":
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


def admin_create_menu():
    """Sub-menu Create untuk admin."""
    while True:
        print("\n==== [ADMIN] CREATE MENU ====")
        print("1. Tambah data barang")
        print("2. Kembali ke menu admin")
        pilihan = input("Pilih (1-2): ").strip()

        if pilihan == "1":
            kode = input("Masukkan KODE barang (primary key): ").strip().upper()
            if kode == "":
                print("\n[INFO] Kode tidak boleh kosong\n")
                continue
            if cari_barang_by_kode(kode) is not None:
                print("\n[INFO] Data already exists\n")
                continue
            nama = minta_string_nonempty("Masukkan nama barang: ").title()
            stok = minta_int("Masukkan stok barang: ", min_value=0)
            harga = minta_int("Masukkan harga barang: ", min_value=0)
            kategori = pilih_kategori()

            print("\nSimpan data berikut?")
            print(f"Kode     : {kode}")
            print(f"Nama     : {nama}")
            print(f"Stok     : {stok}")
            print(f"Harga    : {harga}")
            print(f"Kategori : {kategori}")
            simpan = input("Ketik 'ya' untuk menyimpan, lainnya batal: ").strip().lower()

            if simpan == "ya":
                daftar_barang.append({
                    "kode": kode,
                    "nama": nama,
                    "stok": stok,
                    "harga": harga,
                    "kategori": kategori
                })
                print("\n[INFO] Data successfully saved\n")
            else:
                print("\n[INFO] Data not saved\n")

        elif pilihan == "2":
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


def admin_update_menu():
    """Sub-menu Update untuk admin."""
    while True:
        print("\n==== [ADMIN] UPDATE MENU ====")
        print("1. Ubah data barang")
        print("2. Kembali ke menu admin")
        pilihan = input("Pilih (1-2): ").strip()

        if pilihan == "1":
            if not daftar_barang:
                print("\n[INFO] Data does not exist\n")
                continue
            kode = input("Masukkan KODE barang yang ingin diubah: ").strip().upper()
            barang = cari_barang_by_kode(kode)
            if barang is None:
                print("\n[INFO] The data you are looking for does not exist\n")
                continue

            tampilkan_detail_barang(barang)
            lanjut = input("Lanjut update? (ya/tidak): ").strip().lower()
            if lanjut != "ya":
                print("\n[INFO] Update cancelled\n")
                continue

            print("Kolom yang bisa diubah:")
            print("1. Nama")
            print("2. Stok")
            print("3. Harga")
            print("4. Kategori")
            kolom = input("Pilih kolom (1-4): ").strip()

            if kolom == "1":
                nilai_baru = minta_string_nonempty("Masukkan nama barang baru: ").title()
                nama_kolom = "nama"
            elif kolom == "2":
                nilai_baru = minta_int("Masukkan stok baru: ", min_value=0)
                nama_kolom = "stok"
            elif kolom == "3":
                nilai_baru = minta_int("Masukkan harga baru: ", min_value=0)
                nama_kolom = "harga"
            elif kolom == "4":
                nilai_baru = pilih_kategori()
                nama_kolom = "kategori"
            else:
                print("\n[INFO] The option you entered is not valid\n")
                continue

            konfirm = input("Yakin update data? (ya/tidak): ").strip().lower()
            if konfirm == "ya":
                barang[nama_kolom] = nilai_baru
                print("\n[INFO] Data successfully updated\n")
            else:
                print("\n[INFO] Update cancelled\n")

        elif pilihan == "2":
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


def admin_delete_menu():
    """Sub-menu Delete untuk admin."""
    while True:
        print("\n==== [ADMIN] DELETE MENU ====")
        print("1. Hapus data barang")
        print("2. Kembali ke menu admin")
        pilihan = input("Pilih (1-2): ").strip()

        if pilihan == "1":
            if not daftar_barang:
                print("\n[INFO] Data does not exist\n")
                continue
            kode = input("Masukkan kode barang yang ingin dihapus: ").strip().upper()
            barang = cari_barang_by_kode(kode)
            if barang is None:
                print("\n[INFO] The data you are looking for does not exist\n")
                continue
            tampilkan_detail_barang(barang)
            konfirm = input("Yakin hapus data ini? (ya/tidak): ").strip().lower()
            if konfirm == "ya":
                daftar_barang.remove(barang)
                print("\n[INFO] Data successfully deleted\n")
            else:
                print("\n[INFO] Delete cancelled\n")
        elif pilihan == "2":
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


def admin_lihat_riwayat():
    """Tampilkan riwayat transaksi untuk admin."""
    if not riwayat_transaksi:
        print("\n[INFO] Belum ada transaksi yang tercatat\n")
        return
    print("\n===== RIWAYAT TRANSAKSI PEMBELI =====")
    print(f"Total pembeli unik: {len(pembeli_unik)} -> {pembeli_unik}")
    for i, trx in enumerate(riwayat_transaksi, start=1):
        print(f"\nTransaksi #{i}")
        print(f"Nama Pembeli : {trx['nama_pembeli']}")
        print(f"Metode Bayar : {trx['metode']}")
        print("Detail barang:")
        print("Nama       | Qty | Harga | Subtotal")
        print("------------------------------------")
        for item in trx["detail"]:
            print(f"{item['nama']:10} | {item['qty']:3} | {item['harga']:7} | {item['subtotal']:9}")
        print("------------------------------------")
        print(f"TOTAL : {trx['total']}")
    print()


def menu_admin():
    """Menu utama admin (pemanggil sub-menu CRUD)."""
    while True:
        print("\n========== MODE ADMIN – CAPSTONE MENU ==========")
        print("1. Read   Data Barang")
        print("2. Create Data Barang")
        print("3. Update Data Barang")
        print("4. Delete Data Barang")
        print("5. Cek data yang sudah terbeli & siapa yang membeli")
        print("6. Kembali ke Menu Utama")

        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == "1":
            admin_read_menu()
        elif pilihan == "2":
            admin_create_menu()
        elif pilihan == "3":
            admin_update_menu()
        elif pilihan == "4":
            admin_delete_menu()
        elif pilihan == "5":
            admin_lihat_riwayat()
        elif pilihan == "6":
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


# ============================================
#  MODE PEMBELI – PROFILE, KERANJANG, CHECKOUT
# ============================================

def pembeli_buat_profile():
    """Buat profile pembeli."""
    global profil_pembeli
    print("\n===== CREATE PROFILE PEMBELI =====")
    nama = minta_string_nonempty("Masukkan nama pembeli: ").title()
    email = input("Masukkan email (boleh dikosongkan): ").strip()
    profil_pembeli = {"nama": nama, "email": email}
    print(f"\n[INFO] Profile berhasil dibuat untuk: {nama}\n")


def pembeli_tampilkan_barang_tersedia():
    """Tampilkan barang dengan stok > 0."""
    barang_tersedia = [b for b in daftar_barang if b["stok"] > 0]
    if not barang_tersedia:
        print("\n[INFO] Tidak ada barang yang tersedia\n")
        return
    print("\n==== DAFTAR BARANG TERSEDIA ====")
    print("Kode   | Nama       | Stok | Harga | Kategori")
    print("---------------------------------------------")
    for b in barang_tersedia:
        print(f"{b['kode']:6} | {b['nama']:10} | {b['stok']:4} | {b['harga']:6} | {b['kategori']}")
    print()


def pembeli_tambah_ke_keranjang():
    """Tambah barang ke keranjang, gabungkan jika kode sudah ada."""
    if not daftar_barang:
        print("\n[INFO] Data does not exist (belum ada barang)\n")
        return

    while True:
        pembeli_tampilkan_barang_tersedia()
        kode = input("Masukkan Kode barang yang ingin dimasukkan ke keranjang (atau 'X' untuk selesai): ").strip().upper()

        if kode == "X":
            break

        barang = cari_barang_by_kode(kode)
        if barang is None:
            print("\n[INFO] The data you are looking for does not exist\n")
            continue

        if barang["stok"] <= 0:
            print("\n[INFO] Stock is empty\n")
            continue

        qty = minta_int("Masukkan jumlah yang ingin dimasukkan ke keranjang: ", min_value=1)

        if qty > barang["stok"]:
            print(f"\n[INFO] stok is not enough. remaining {barang['stok']}\n")
            continue

        gabungkan_item_di_keranjang(barang["kode"], barang["nama"], qty, barang["harga"])
        print(f"\n[INFO] {barang['nama']} sebanyak {qty} berhasil dimasukkan ke keranjang\n")

        lanjut = input("Mau tambah barang lain ke keranjang? (ya/tidak): ").strip().lower()
        if lanjut != "ya":
            break


def pembeli_tampilkan_keranjang():
    """Tampilkan isi keranjang dan ringkasan."""
    if not keranjang:
        print("\n[INFO] Keranjang masih kosong\n")
        return
    print("\n=== ISI KERANJANG ===")
    print("Idx | Nama       | Qty | Harga | Subtotal")
    print("-----------------------------------------")
    for idx, item in enumerate(keranjang):
        print(f"{idx:3} | {item['nama']:10} | {item['qty']:3} | {item['harga']:7} | {item['subtotal']:9}")
    print()
    tampilkan_ringkasan_keranjang()


def pembeli_delete_dari_keranjang():
    """Hapus item dari keranjang berdasarkan index."""
    if not keranjang:
        print("\n[INFO] Keranjang masih kosong\n")
        return

    pembeli_tampilkan_keranjang()
    idx_str = input("Masukkan index barang yang ingin dihapus dari keranjang: ").strip()
    if not idx_str.isdigit():
        print("\n[INFO] Index harus berupa angka\n")
        return

    idx = int(idx_str)
    if idx < 0 or idx >= len(keranjang):
        print("\n[INFO] Index tidak valid\n")
        return

    item = keranjang[idx]
    konfirm = input(f"Yakin menghapus {item['nama']} dari keranjang? (ya/tidak): ").strip().lower()
    if konfirm == "ya":
        del keranjang[idx]
        print("\n[INFO] Barang berhasil dihapus dari keranjang\n")
    else:
        print("\n[INFO] Penghapusan dibatalkan\n")


def pembeli_checkout():
    """Proses checkout: tampilkan struk, cek stok, proses pembayaran, kurangi stok, simpan riwayat."""
    global profil_pembeli
    if profil_pembeli is None:
        print("\n[INFO] Silakan buat profile pembeli terlebih dahulu (Menu 1)\n")
        return
    if not keranjang:
        print("\n[INFO] Keranjang kosong. Tidak ada transaksi.\n")
        return

    total = hitung_total_keranjang()

    METODE_BAYAR = ("Cash", "Transfer", "QRIS")
    print("\nPilih metode pembayaran:")
    for i, m in enumerate(METODE_BAYAR, start=1):
        print(f"{i}. {m}")
    pilih = minta_int("Masukkan nomor metode: ", min_value=1)
    if 1 <= pilih <= len(METODE_BAYAR):
        metode = METODE_BAYAR[pilih - 1]
    else:
        metode = "Cash"

    # Cetak struk
    print("\n================================")
    print("          STRUK BELANJA         ")
    print("================================")
    print(f"Nama Pembeli : {profil_pembeli['nama']}")
    print(f"Metode Bayar : {metode}")
    print("Nama       | Qty | Harga | Subtotal")
    print("------------------------------------")
    for item in keranjang:
        print(f"{item['nama']:10} | {item['qty']:3} | {item['harga']:7} | {item['subtotal']:9}")
    print("------------------------------------")
    print(f"TOTAL BAYAR : {total}")
    print("================================")

    # Cek stok final
    for item in keranjang:
        barang = cari_barang_by_kode(item["kode"])
        if barang is None or barang["stok"] < item["qty"]:
            print(f"\n[INFO] Transaksi gagal, stok {item['nama']} tidak mencukupi.\n")
            return

    # Proses pembayaran
    while True:
        bayar = minta_int("Masukkan jumlah uang Anda: ", min_value=0)
        if bayar < total:
            print(f"\n[INFO] Uang tidak cukup. Kurang {total - bayar}\n")
        else:
            kembalian = bayar - total
            print("\n[INFO] Payment successful. Thank you for shopping!\n")
            print(f"Change : {kembalian}\n")
            break

    # Kurangi stok, simpan riwayat, kosongkan keranjang
    for item in keranjang:
        barang = cari_barang_by_kode(item["kode"])
        barang["stok"] -= item["qty"]

    pembeli_unik.add(profil_pembeli["nama"])

    riwayat_transaksi.append({
        "nama_pembeli": profil_pembeli["nama"],
        "detail": copy.deepcopy(keranjang),
        "total": total,
        "metode": metode
    })

    keranjang.clear()
    print("\n[INFO] Transaksi selesai dan keranjang dikosongkan.\n")


def menu_pembeli():
    """Menu utama mode pembeli."""
    while True:
        print("\n========== MODE PEMBELI – CAPSTONE MENU ==========")
        print("1. Create profile pembeli")
        print("2. Read Data Barang yang tersedia (A)")
        print("3. Masukkan ke keranjang (C)")
        print("4. Delete Data Barang di keranjang (D)")
        print("5. Belanja (Checkout + Struk Pembayaran)")
        print("6. Kembali ke Menu Utama (E)")

        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == "1":
            pembeli_buat_profile()
        elif pilihan == "2":
            pembeli_tampilkan_barang_tersedia()
        elif pilihan == "3":
            pembeli_tambah_ke_keranjang()
        elif pilihan == "4":
            pembeli_delete_dari_keranjang()
        elif pilihan == "5":
            pembeli_checkout()
        elif pilihan == "6":
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


# ============================================
#  MAIN PROGRAM
# ============================================

def main():
    while True:
        print("\n========== PILIH MODE ==========")
        print("1. Mode Admin")
        print("2. Mode Pembeli")
        print("3. Exit Program")

        main_mode = input("Pilih (1-3): ").strip()

        if main_mode == "1":
            menu_admin()
        elif main_mode == "2":
            menu_pembeli()
        elif main_mode == "3":
            print("\n[INFO] Program ended. Thank you.\n")
            break
        else:
            print("\n[INFO] The option you entered is not valid\n")


if __name__ == "__main__":
    main()
