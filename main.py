# main.py
import os
# Menghubungkan ke file login.py
from login import jalankan_autentikasi

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Panggil fungsi gerbang menu utama dari file login.py
    status_akses = jalankan_autentikasi()
    
    if status_akses:
        bersihkan_layar()
        print("┌────────────────────────────────────────────────────────┐")
        print("│      SELAMAT DATANG DI APLIKASI UTAMA ANAGRAM GAME     │")
        print("├────────────────────────────────────────────────────────┤")
        print("│  Aplikasi berhasil diakses menggunakan akun Anda!       │")
        print("│                                                        │")
        print("│  [!] Taruh menu utama game atau logika anagram kalian  │")
        print("│      di bawah baris ini pada file main.py.             │")
        print("└────────────────────────────────────────────────────────┘")
    else:
        bersihkan_layar()
        print("Program ditutup secara aman. Sampai jumpa!")

if __name__ == "__main__":
    main()