# database.py
import os

def load_kata_dari_file():
    """Fungsi untuk membaca data kosakata dari file teks eksternal ke memori RAM"""
    daftar_kata = [] # Membuat struktur data List kosong untuk menampung seluruh kata sah
    nama_file = "kata_indonesia.txt" # Deklarasi target file yang berisi daftar kata KBBI
    
    # VALIDASI: Memeriksa apakah file "kata_indonesia.txt" tersedia di dalam folder project
    if os.path.exists(nama_file):
        # Membuka file dengan mode "r" (Read/Membaca saja) dan encoding UTF-8 agar karakter terbaca aman
        with open(nama_file, "r", encoding="utf-8") as file:
            for baris in file:
                # Membersihkan ujung string dari enter (\n) dan memaksa huruf menjadi kecil (lowercase)
                kata = baris.strip().lower()
                # Memasukkan kata yang sudah bersih ke dalam struktur data List menggunakan .append()
                daftar_kata.append(kata)
    else:
        # Menampilkan pesan peringatan di terminal jika file teks kamus tidak ditemukan
        print(f"Peringatan: File {nama_file} tidak ditemukan!")
        
    return daftar_kata # Mengembalikan kumpulan list kata ke baris pemanggil fungsi

# PROSES EKSTRAKSI: Menjalankan fungsi di atas dan menyimpannya ke variabel global 'kata_pilihan'
# Variabel 'kata_pilihan' inilah yang nantinya di-import oleh gameplay.py untuk mencocokkan jawaban user
kata_pilihan = load_kata_dari_file()

# --- BLOK DEBUGGING (Hanya berjalan jika berkas ini dieksekusi secara mandiri/di-run langsung) ---
if __name__ == "__main__":
    print(f"Berhasil mengekstrak {len(kata_pilihan)} kata siap pakai untuk game!")
    print("Contoh kata:", kata_pilihan[:10]) # Mencetak slicing 10 kata pertama dari list sebagai sampel data
