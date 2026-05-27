
import os
from login import jalankan_autentikasi, update_level_user
from level import jalankan_pemilihan_level
from gameplay import jalankan_gameplay_level
from gameplay2 import jalankan_gameplay_level as jalankan_gameplay_level_hard

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    #jalanin login dan sign up
    status_akses, username, level_tertinggi = jalankan_autentikasi()
    
    if status_akses:
        #loop utama setelah login sukses, untuk pemilihan level dan gameplay
        while True:
            #jalankan menu pemilihan level dengan parameter username dan level tertinggi yang sudah dicapai
            level_dipilih = jalankan_pemilihan_level(username, level_tertinggi)
            
            if level_dipilih is None:
                print("Anda membatalkan pemilihan level.")
                break
                
            bersihkan_layar()
            
            #loop gameplay khusus untuk menangani fitur 'Restart' pada level yang sama
            while True:
                #pilihan berdasarkan level
                if level_dipilih >= 6:
                    hasil_game = jalankan_gameplay_level_hard(username, level_dipilih)
                else:
                    hasil_game = jalankan_gameplay_level(username, level_dipilih)
                
                #kalo menang
                if hasil_game is True:
                    #menang, cek apakah level yang dipilih adalah level tertinggi yang sudah dicapai, jika iya naikkan level tertinggi
                    if level_dipilih == level_tertinggi and level_tertinggi < 10:
                        level_tertinggi += 1
                        update_level_user(username, level_tertinggi)
                        print(f"\nSelamat! Progress disimpan. Akun {username} naik ke Level {level_tertinggi}!")
                    break
                
                #kalo restart
                elif hasil_game == "restart":
                    bersihkan_layar()
                    continue  # Mengulang loop gameplay pada level_dipilih yang sama
                    
                #kalo ke menu
                elif hasil_game == "menu" or hasil_game is False:
                    break  
                    
                #kalo quit
                elif hasil_game == "quit":
                    bersihkan_layar()
                    print("Program ditutup secara aman. Sampai jumpa!")
                    return  #keluar dari fungsi main untuk mengakhiri program
            
    else:
        bersihkan_layar()
        print("Program ditutup secara aman. Sampai jumpa!")

if __name__ == "__main__":
    main()