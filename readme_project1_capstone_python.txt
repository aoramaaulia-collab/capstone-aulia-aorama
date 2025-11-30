=== Project Capstone Python – Sistem Mini Marketplace (Admin + Pembeli)
===

Project ini adalah aplikasi mini marketplace berbasis Python console,
dengan dua mode utama:

1.  Mode Admin → Mengelola data barang (CRUD) dan melihat riwayat
    pembelian
2.  Mode Pembeli → Melihat barang, membuat profile, belanja, mengelola
    keranjang, dan checkout

Seluruh proses dilakukan melalui input di terminal.

=== Cara Menjalankan Program ===

1.  Pastikan Python sudah terinstall di komputer.

2.  Simpan file program sebagai: capstone1.py

3.  Jalankan melalui terminal atau CMD:

    python capstone1.py

4.  Program akan menampilkan pilihan mode:

    -   Mode Admin
    -   Mode Pembeli
    -   Exit Program

=== Struktur Data Barang ===

Data barang disimpan dalam list of dictionary, contoh:

{ “kode”: “BRG001”, “nama”: “Pulpen”, “stok”: 20, “harga”: 7000,
“kategori”: “Alat Tulis” }

Setiap barang memiliki: 1. kode → ID unik barang 2. nama → Nama barang
3. stok → Jumlah stok yang tersedia 4. harga → Harga per item 5.
kategori → Kategori barang

=== Fitur dalam Mode Admin ===

1.  Read Data Barang
    -   Lihat semua barang
    -   Cari berdasarkan kode
    -   Tampilkan detail barang
2.  Create Data Barang
    -   Tambah barang baru
    -   Validasi kode unik
3.  Update Data Barang
    -   Mengubah nama, stok, harga, kategori
4.  Delete Data Barang
    -   Menghapus barang berdasarkan kode
5.  Riwayat Transaksi
    -   Menampilkan transaksi pembeli, total, metode bayar, pembeli unik

=== Fitur dalam Mode Pembeli ===

1.  Buat Profile
    -   Nama dan email
2.  Lihat Barang Tersedia
    -   Hanya stok > 0
3.  Tambah ke Keranjang
    -   Validasi stok
    -   Penggabungan barang otomatis
4.  Hapus dari Keranjang
    -   Berdasarkan index
5.  Checkout
    -   Pilih metode bayar
    -   Struk belanja
    -   Validasi stok
    -   Pembayaran
    -   Simpan riwayat

=== Menu Utama ===

1.  Mode Admin
2.  Mode Pembeli
3.  Exit Program
