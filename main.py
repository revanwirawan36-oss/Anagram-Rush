import os

# Data awal (Minimal 15 data untuk memenuhi ketentuan UAP)
# Kamu bisa isi dengan kata-kata yang punya pasangan anagram
arsip_kata = [
    "kasur", "rusak", "karus", 
    "aman", "mana", "nama", 
    "tuba", "buat", "batu",
    "bola", "balok", "loba",
    "makan", "makna", "kamna"
]

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_menu():
    print("┌────────────────────────────────────────┐")
    print("│         ANAGRAM ARCHIVE SYSTEM         │")
    print("├────────────────────────────────────────┤")
    print("│  [1] Input Kata Baru                   │")
    print("│  [2] Tampilkan & Grouping Anagram      │")
    print("│  [3] Cari Kata di Arsip                │")
    print("│  [4] Keluar                            │")
    print("└────────────────────────────────────────┘")

def input_kata():
    bersihkan_layar()
    print("=== [1] INPUT KATA BARU ===")
    kata_baru = input("Masukkan kata baru: ").strip()
    
    if kata_baru:
        # Preprocessing teks: menyamakan huruf besar/kecil (Fitur Wajib)
        arsip_kata.append(kata_baru.lower())
        print(f"\nKata '{kata_baru}' berhasil ditambahkan!")
    else:
        print("\nInput tidak boleh kosong.")
    
    input("\nTekan Enter untuk kembali ke menu...")

def grouping_anagram():
    bersihkan_layar()
    print("=== [2] GROUPING & VALIDASI ANAGRAM ===")
    print(f"Total data saat ini: {len(arsip_kata)} kata\n")
    
    # Logika Grouping menggunakan Dictionary
    kelompok_anagram = {}
    for kata in arsip_kata:
        # Karakter diurutkan sebagai KEY (Fitur Wajib: Analisis Karakter)
        key_pola = "".join(sorted(kata))
        
        if key_pola not in kelompok_anagram:
            kelompok_anagram[key_pola] = []
        kelompok_anagram[key_pola].append(kata)
    
    # Menampilkan hasil kelompok (Fitur Wajib)
    no = 1
    for pola, daftar_kata in kelompok_anagram.items():
        # Validasi anagram: jika anggotanya > 1, berarti dia punya pasangan anagram
        status = "(Anagram Terdeteksi)" if len(daftar_kata) > 1 else "(Bukan Anagram)"
        
        print(f"{no}. Pola ['{polas_format(pola)}'] {status}:")
        print(f"   -> {', '.join(daftar_kata)}")
        print("-" * 40)
        no += 1
        
    input("\nTekan Enter untuk kembali ke menu...")

def polas_format(pola):
    # Mengubah "akrsu" menjadi "a-k-r-s-u" biar rapi dilihat
    return "-".join(list(pola))

def cari_kata():
    bersihkan_layar()
    print("=== [3] PENCARIAN DATA ===")
    target = input("Masukkan kata yang dicari: ").strip().lower()
    
    # Fitur Wajib: Pencarian data
    if target in arsip_kata:
        print(f"\nKata '{target}' DITEMUKAN di dalam arsip!")
    else:
        print(f"\nKata '{target}' TIDAK DITEMUKAN dalam arsip.")
        
    input("\nTekan Enter untuk kembali ke menu...")

def main():
    while True:
        bersihkan_layar()
        tampilkan_menu()
        pilihan = input("Pilih menu (1-4): ").strip()
        
        if pilihan == "1":
            input_kata()
        elif pilihan == "2":
            grouping_anagram()
        elif pilihan == "3":
            cari_kata()
        elif pilihan == "4":
            bersihkan_layar()
            print("Terima kasih telah menggunakan program ini!")
            break
        else:
            input("\nPilihan tidak valid. Tekan Enter untuk coba lagi...")

if __name__ == "__main__":
    main()