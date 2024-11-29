menu = {
    1: {"nama": "Nasi Goreng", "harga": 20000},
    2: {"nama": "Mie Goreng", "harga": 18000},
    3: {"nama": "Es Teh", "harga": 5000},
    4: {"nama": "Es Jeruk", "harga": 7000},
}

# Fungsi Menampilkan Menu
def tampilkan_menu():
    print(f"\n{'MENU RESTORAN':^40}")
    print("=" * 40)
    print(f"{'ID':<5}{'Nama Menu':<25}{'Harga':>10}")
    print("-" * 40)
    for id_menu, detail in menu.items():
        print(f"{id_menu:<5}{detail['nama']:<25}{detail['harga']:>10,}")
    print("=" * 40)

# Fungsi Pemisah untuk Interaksi
def garis_pemisah():
    print("\n" + "=" * 40 + "\n")

# Fungsi Menambahkan Pesanan
def tambah_pesanan(pesanan):
    tampilkan_menu()
    while True:
        try:
            id_menu = int(input("\nMasukkan ID Menu yang dipesan (0 untuk batal): "))
            if id_menu == 0:
                print("Kembali ke menu utama.\n")
                break
            if id_menu not in menu:
                print("ID Menu tidak valid! Coba lagi.")
                continue
            jumlah = int(input("Masukkan jumlah: "))
            if jumlah <= 0:
                print("Jumlah harus lebih dari 0! Coba lagi.")
                continue

            nama_menu = menu[id_menu]["nama"]
            harga = menu[id_menu]["harga"]
            total_harga = harga * jumlah

            # Periksa apakah sudah ada di pesanan, jika ya update jumlah
            for item in pesanan:
                if item["nama"] == nama_menu:
                    item["jumlah"] += jumlah
                    item["total_harga"] += total_harga
                    print(f"\n{nama_menu} berhasil diperbarui! Jumlah sekarang: {item['jumlah']}")
                    return

            # Jika belum ada, tambahkan pesanan baru
            pesanan.append({"nama": nama_menu, "jumlah": jumlah, "total_harga": total_harga})
            print(f"\n{nama_menu} sejumlah {jumlah} berhasil ditambahkan!\n")
            break
        except ValueError:
            print("Harap masukkan angka yang valid!")

# Fungsi Menampilkan Pesanan
def tampilkan_pesanan(pesanan):
    if not pesanan:
        print("\nBelum ada pesanan.")
        return 0

    print("\n=== PESANAN ANDA ===")
    total_bayar = 0
    for idx, item in enumerate(pesanan, start=1):
        print(f"{idx}. {item['nama']} - {item['jumlah']} porsi - Rp{item['total_harga']:,}")
        total_bayar += item['total_harga']
    print(f"\nSubtotal: Rp{total_bayar:,}\n")
    return total_bayar

# Fungsi Menghapus Pesanan
def hapus_pesanan(pesanan):
    if not pesanan:
        print("\nBelum ada pesanan untuk dihapus!")
        return
    
    tampilkan_pesanan(pesanan)
    try:
        id_hapus = int(input("Masukkan nomor pesanan yang ingin dihapus: "))
        if 1 <= id_hapus <= len(pesanan):
            item_dihapus = pesanan.pop(id_hapus - 1)
            print(f"\n{item_dihapus['nama']} berhasil dihapus dari pesanan.\n")
            garis_pemisah()
        else:
            print("Nomor pesanan tidak valid!")
    except ValueError:
        print("Harap masukkan angka yang valid!")

# Fungsi Edit Pesanan
def edit_pesanan(pesanan):
    if not pesanan:
        print("\nBelum ada pesanan untuk diedit!")
        return

    tampilkan_pesanan(pesanan)
    try:
        id_edit = int(input("\nMasukkan nomor pesanan yang ingin diedit: "))
        if 1 <= id_edit <= len(pesanan):
            item = pesanan[id_edit - 1]
            print(f"\nAnda sedang mengedit pesanan: {item['nama']} - {item['jumlah']} porsi")
            jumlah_baru = int(input("Masukkan jumlah baru: "))
            if jumlah_baru <= 0:
                print("Jumlah harus lebih dari 0! Coba lagi.")
                return
            item["jumlah"] = jumlah_baru
            item["total_harga"] = jumlah_baru * menu[next(key for key, value in menu.items() if value["nama"] == item["nama"])]["harga"]
            print(f"\nPesanan {item['nama']} berhasil diperbarui menjadi {jumlah_baru} porsi.\n")
            garis_pemisah()
        else:
            print("Nomor pesanan tidak valid!\n")
    except ValueError:
        print("Harap masukkan angka yang valid!")

# Fungsi Menghitung Diskon
def hitung_diskon(total):
    if total >= 100000:
        return total * 0.10
    elif total >= 50000:
        return total * 0.05
    return 0

# Fungsi Menghitung Pajak
def hitung_pajak(total, pajak=0.1):
    return total * pajak

# Fungsi Pembayaran dengan struk yang lebih rapih
def proses_pembayaran(pesanan, voucher=None):
    total_bayar = tampilkan_pesanan(pesanan)
    if total_bayar == 0:
        print("Belum ada pesanan untuk dibayar!\n")
        return

    diskon = hitung_diskon(total_bayar)
    pajak = hitung_pajak(total_bayar)

    # Jika ada voucher, beri diskon tambahan
    if voucher:
        if voucher == "BULAN10":
            voucher_diskon = total_bayar * 0.10
            print(f"\nVoucher BULANAN10 diterapkan: -Rp{int(voucher_diskon):,}")
            diskon += voucher_diskon
        else:
            print("\nVoucher tidak valid!")
    
    total_setelah_diskon = total_bayar - diskon + pajak

    print("\n=========== STRUK PEMBAYARAN ===========")
    print(f"Subtotal                        : Rp{int(total_bayar):,}")
    print(f"Diskon                          : Rp{int(diskon):,}")
    print(f"Pajak                           : Rp{int(pajak):,}")
    print(f"Total setelah diskon dan pajak  : Rp{int(total_setelah_diskon):,}")

    while True:
        try:
            bayar = int(input("\nMasukkan jumlah uang yang dibayarkan: "))
            if bayar >= total_setelah_diskon:
                kembalian = bayar - total_setelah_diskon
                print(f"Pembayaran berhasil! Kembalian Anda: Rp{int(kembalian):,}")
                pesanan.clear()
                garis_pemisah()
                break
            else:
                print("Uang yang dibayarkan tidak cukup! Coba lagi.")
        except ValueError:
            print("Harap masukkan angka yang valid!")

# Fungsi Menu Admin
def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Tambah Menu")
        print("2. Hapus Menu")
        print("3. Lihat Menu")
        print("4. Kembali ke Menu Utama")
        
        try:
            pilihan_admin = int(input("\nPilih menu admin: "))
            if pilihan_admin == 1:
                tambah_menu()
            elif pilihan_admin == 2:
                hapus_menu()
            elif pilihan_admin == 3:
                tampilkan_menu()
            elif pilihan_admin == 4:
                break
            else:
                print("Pilihan tidak valid! Coba lagi.")
        except ValueError:
            print("Harap masukkan angka yang valid!")

# Fungsi untuk Menambah Menu
def tambah_menu():
    try:
        nama_menu = input("Masukkan nama menu baru: ")
        harga_menu = int(input("Masukkan harga menu baru: "))
        id_menu_baru = max(menu.keys()) + 1
        menu[id_menu_baru] = {"nama": nama_menu, "harga": harga_menu}
        print(f"\n{nama_menu} berhasil ditambahkan ke menu!\n")
    except ValueError:
        print("Harga harus berupa angka! Coba lagi.")

# Fungsi untuk Menghapus Menu
def hapus_menu():
    try:
        tampilkan_menu()
        id_menu_hapus = int(input("\nMasukkan ID Menu yang ingin dihapus: "))
        if id_menu_hapus in menu:
            menu.pop(id_menu_hapus)
            print("\nMenu berhasil dihapus!\n")
        else:
            print("ID Menu tidak valid! Coba lagi.")
    except ValueError:
        print("Harap masukkan angka yang valid!")

# Program Utama dengan Pemisah Interaksi
def main():
    pesanan = []
    while True:
        try:
            print("=== SELAMAT DATANG DI RESTORAN UTM ===")
            print("=== SISTEM KASIR RESTORAN ===")
            print("1. Menu Admin")
            print("2. Tampilkan Menu")
            print("3. Tambah Pesanan")
            print("4. Lihat Pesanan")
            print("5. Hapus Pesanan")
            print("6. Edit Pesanan")
            print("7. Proses Pembayaran")
            print("8. Keluar")

            pilihan = int(input("\nPilih menu: "))

            if pilihan == 1:
                menu_admin()
            elif pilihan == 2:
                tampilkan_menu()
            elif pilihan == 3:
                tambah_pesanan(pesanan)
            elif pilihan == 4:
                tampilkan_pesanan(pesanan)
            elif pilihan == 5:
                hapus_pesanan(pesanan)
            elif pilihan == 6:
                edit_pesanan(pesanan)
            elif pilihan == 7:
                voucher = input("\nMasukkan kode voucher (kosongkan jika tidak ada): ")
                proses_pembayaran(pesanan, voucher)
            elif pilihan == 8:
                print("Terima kasih telah menggunakan sistem kasir!")
                garis_pemisah()
                break
            else:
                print("Pilihan tidak valid! Masukkan angka 1-8.")
        except ValueError:
            print("Harap masukkan angka yang valid!")

main()
