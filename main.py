# main.py
import os
# Meng-import fungsi-fungsi dari kedua file pendukung
from login import jalankan_autentikasi, update_level_user
from level import jalankan_pemilihan_level

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. Jalankan autentikasi login/signup dari login.py
    status_akses, username, level_tertinggi = jalankan_autentikasi()
    
    if status_akses:
        # 2. Jalankan menu pemilih level dari level.py jika login sukses
        level_dipilih = jalankan_pemilihan_level(username, level_tertinggi)
        
        bersihkan_layar()
        if level_dipilih is not None:
            print("┌────────────────────────────────────────────────────────┐")
            print(f"  GAME START: LEVEL {level_dipilih}                       ")
            print("├────────────────────────────────────────────────────────┤")
            print(f"  Memuat database kata anagram untuk Level {level_dipilih}... ")
            print("└────────────────────────────────────────────────────────┘")
            
            # --- LOGIKA GAMEPLAY KELOMPOK KALIAN DIMULAI DI SINI ---
            # Contoh simulasi: Jika dia menyelesaikan level tertingginya, simpan progress baru
            if level_dipilih == level_tertinggi and level_tertinggi < 25:
                level_tertinggi += 1
                update_level_user(username, level_tertinggi)
                print(f"\nSelamat! Progress disimpan. Akun {username} naik ke Level {level_tertinggi}!")
        else:
            print("Anda membatalkan pemilihan level.")
    else:
        bersihkan_layar()
        print("Program ditutup secara aman. Sampai jumpa!")

if __name__ == "__main__":
    main()