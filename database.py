# database.py
import os

def load_kata_dari_file():
    daftar_kata = []
    nama_file = "kata_indonesia.txt"
    
    #cek apakah filenya ada di folder yang sama
    if os.path.exists(nama_file):
        with open(nama_file, "r", encoding="utf-8") as file:
            for baris in file:
                kata = baris.strip().lower()
                daftar_kata.append(kata)
    else:
        print(f"Peringatan: File {nama_file} tidak ditemukan!")
        
    return daftar_kata

#ekkstrak seluruh kata ke dalam variabel yang siap di-import oleh main.py
kata_pilihan = load_kata_dari_file()

#debug
if __name__ == "__main__":
    print(f"Berhasil mengekstrak {len(kata_pilihan)} kata siap pakai untuk game!")
    print("Contoh kata:", kata_pilihan[:10])