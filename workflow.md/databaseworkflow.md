```markdown
# Workflow & Logic Flow: `database.py` (Anagram Rush)

Dokumen ini menjelaskan alur logika, fungsi, dan cara kerja dari file `database.py` yang bertugas sebagai komponen manajemen data teks (file handling) dalam game **Anagram Rush**.

---

## 1. Penjelasan Umum File
File `database.py` berfungsi untuk **membaca aset eksternal** berupa file teks (`kata_indonesia.txt`) yang berisi daftar kosakata. Program ini bertugas mengekstrak seluruh kata di dalam file tersebut, membersihkan format teksnya, lalu memasukkannya ke dalam sebuah *List* di Python agar siap digunakan oleh bagian logika game utama (`main.py` atau `gameplay.py`).

Dengan menggunakan file ini, database kata game kita menjadi dinamis. Jika kamu ingin menambahkan kata-kata baru, kamu cukup mengedit file `kata_indonesia.txt` tanpa perlu mengubah kode program Python-nya.

---

## 2. Pustaka (Library) yang Digunakan
File ini menggunakan satu modul bawaan dari Python, yaitu:
* **`import os`**: Modul ini digunakan untuk berinteraksi dengan sistem operasi komputer kita. Di dalam file ini, fungsi spesifik yang digunakan adalah `os.path.exists()` untuk memeriksa apakah file teks yang ingin dibaca benar-benar ada di dalam direktori komputer atau tidak. Ini sangat penting untuk mencegah program *crash* (berhenti tiba-tiba) karena error *FileNotFound*.

---

## 3. Alur Logika Cara Kerja Program (Workflow)

Secara garis besar, berikut adalah diagram alur logika dari fungsi `load_kata_dari_file()` saat dijalankan:


```

```
      [Mulai Fungsi]
             │
             ▼
 [Cek: Apakah File Ada?]
             │
    ┌────────┴────────┐
 (Benar)           (Salah)
    │                 │
    ▼                 ▼

```

[Buka File Teks]  [Tampilkan Peringatan:
│           File Tidak Ditemukan]
▼                 │
[Looping: Baca per baris]  │
├─► Hapus spasi/enter     │
├─► Ubah ke huruf kecil   │
└─► Masukkan ke List      │
│                 │
▼                 ▼
[Kembalikan List] ◄───┘
│
▼
[Selesai/Return]

```

### Detail Langkah Per Langkah:

### Langkah 1: Inisialisasi Wadah Data
Saat fungsi `load_kata_dari_file()` dipanggil, program menyiapkan sebuah *list* kosong bernama `daftar_kata = []` untuk menampung kata-kata yang sukses dibaca nanti. Nama file yang ditargetkan juga dikunci pada variabel `nama_file = "kata_indonesia.txt"`.

### Langkah 2: Validasi Keberadaan File (*Error Handling*)
Sebelum membuka file, program melakukan pengecekan dengan `if os.path.exists(nama_file):`.
* **Jika file DITEMUKAN:** Program akan lanjut ke tahap pembacaan file.
* **Jika file TIDAK DITEMUKAN:** Program akan langsung lompat ke blok `else`, menampilkan pesan peringatan di terminal (`Peringatan: File ... tidak ditemukan!`), dan mengembalikan *list* kosong.

### Langkah 3: Membaca dan Membersihkan Data (*Data Cleansing*)
Ketika file berhasil dibuka menggunakan perintah `with open(...)`, program akan membaca file tersebut baris demi baris menggunakan perulangan `for baris in file:`. 

Di dalam perulangan, terjadi proses pembersihan teks menggunakan dua *method* bawaan Python:
1. **`.strip()`**: Berfungsi untuk menghapus karakter tak terlihat seperti spasi di ujung kata atau karakter *newline* (`\n` / pindah baris) yang otomatis tercipta di dalam file teks.
2. **`.lower()`**: Berfungsi untuk mengubah semua huruf menjadi **huruf kecil (lowercase)**. Hal ini dilakukan agar validasi tebakan pemain di game nanti tidak bersifat *case-sensitive* (huruf kapital tidak merusak penilaian).

Setelah bersih, kata tersebut dimasukkan ke dalam wadah menggunakan `daftar_kata.append(kata)`.

### Langkah 4: Penyimpanan Global (*Variable Extraction*)
Setelah fungsi selesai berjalan, *list* yang sudah penuh berisi kata-kata dikembalikan (`return daftar_kata`) dan langsung disimpan ke dalam variabel global:
```python
kata_pilihan = load_kata_dari_file()

```

Variabel `kata_pilihan` inilah yang nantinya akan di-*import* oleh file utama game kamu.

---

## 4. Logika Blok Pengujian (`if __name__ == "__main__":`)

Di bagian akhir file, terdapat baris kode berikut:

```python
if __name__ == "__main__":
    # Kode debug di sini...

```

Sebagai mahasiswa ilmu komputer, memahami sintaks ini sangatlah penting:

* **Fungsinya:** Blok ini adalah **fitur pengujian mandiri (debug)**. Kode di dalam blok ini **hanya akan berjalan** jika kamu mengeksekusi/menjalankan file `database.py` ini secara langsung.
* **Jika di-import:** Apabila file `database.py` ini dipanggil atau di-*import* oleh file `main.py`, maka kode cetak (*print*) contoh kata di dalam blok ini **tidak akan ikut tereksekusi**, sehingga terminal game utamamu tetap bersih dari teks debug.

---

## 5. Cara Mengimpor ke Program Utama

Untuk memanfaatkan daftar kata yang sudah diekstrak oleh file ini ke dalam file logika game kamu (misalnya `main.py`), kamu cukup menuliskan kode berikut:

```python
from database import kata_pilihan

# Sekarang kamu bisa menggunakan list 'kata_pilihan' di game utama
print(f"Total kosakata yang tersedia di game: {len(kata_pilihan)}")

```

```

```
