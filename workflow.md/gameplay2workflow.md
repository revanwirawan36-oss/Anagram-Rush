```markdown
# Workflow & Logic Flow: `gameplay2.py` (Anagram Rush - Hard Mode)

Dokumen ini menjelaskan alur logika, struktur fungsi, dan mekanika kerja dari file `gameplay2.py`[cite: 5]. File ini dirancang khusus sebagai mesin penggerak **Hard Mode (Level 6–10)** pada game **Anagram Rush**, di mana tantangannya dinaikkan: setiap kata dasar wajib dicari **minimal 2 anagram yang berbeda**[cite: 5].

---

## 1. Penjelasan Umum File
File `gameplay2.py` mengadopsi basis kode berbasis terminal (*TUI/Text User Interface*) menggunakan pustaka **`curses`**[cite: 5]. Perbedaan mendasar dari versi gameplay biasa terletak pada manajemen penampungan data jawaban pemain:
* **Gameplay Biasa:** Hanya membutuhkan 1 jawaban anagram per kata[cite: 4].
* **Gameplay 2 (Hard Mode):** Mempersyaratkan 2 slot jawaban anagram yang valid secara vertikal untuk setiap kata dasar tunggal sebelum level dianggap selesai[cite: 5].

---

## 2. Struktur Data Utama (`jawaban_user`)

Untuk mengakomodasi kebutuhan multi-jawaban, struktur penyimpanan data internal diubah menggunakan kombinasi **Dictionary dan List**[cite: 5]:

```python
# Setiap kata dasar dihubungkan dengan sebuah List kosong (Maksimal menampung 2 elemen)
jawaban_user = {kata: [] for kata in daftar_kata}

```

* **Key:** Berupa string kata dasar dari level terkait.


* **Value:** Berupa objek *List* dinamis yang akan diisi dengan metode `.append()` ketika pemain menemukan anagram baru yang sah.



---

## 3. Alur Logika Cara Kerja Program (Workflow)

Siklus utama (*Game Loop*) berjalan menggunakan perulangan tanpa henti (`while True`) yang mengeksekusi operasi berikut secara sekuensial:

```
[Mulai Loop Putaran Baru]
           │
           ▼
[Hitung Sisa Waktu Detik]
           │
           ├─► Sisa Waktu <= 0 ? ──► [Kalah: Panggil menu_akhir]
           │
           ▼
[Evaluasi Kondisi Kemenangan]
           │
           ├─► Apakah semua kata dasar memiliki 2 jawaban anagram?
           │     │
           │     └─► YA ──► [Menang: Panggil menu_akhir]
           │
           ▼
[Bersihkan & Gambar Ulang Layar Terminal (Render UI)]
           │
           ├─► Baris 1: Kotak Kata Dasar (Upper Case)
           ├─► Baris 2: Kotak Jawaban (Menampilkan Slot 1 & Slot 2)
           ├─► Baris 3: Visualisasi Bubble Sort Real-Time
           └─► Baris 4: Kolom Input Teks & Log Notifikasi Aktivitas
           │
           ▼
[Metode Input Polling (getch)] ──► Ambil Kode Tombol Keyboard

```

---

## 4. Struktur Validasi Berlapis Pasca Menekan `ENTER`

Ketika input buffer mendeteksi penekanan tombol `ENTER` (kode desimal `10` atau `13`), program menyaring string tebakan tersebut melalui 5 tahapan validasi logika:

```
                     [Pemain Menekan Tombol ENTER]
                                   │
                                   ▼
                [Pengecekan Struktur Kombinasi Huruf]
               (Menggunakan Algoritma Bubble Sort Manual)
                                   │
                     ┌─────────────┴─────────────┐
               (Tidak Cocok)                  (Cocok)
                     │                           │
                     ▼                           ▼
            [LOG: "Bukan anagram         [Pengecekan Kamus]
             dari kata mana pun!"]     (Apakah terdaftar di kata_pilihan?)
                                                 │
                                   ┌─────────────┴─────────────┐
                                (Tidak)                     (Ya)
                                   │                           │
                                   ▼                           ▼
                          [LOG: "Anagram cocok,       [Pengecekan Duplikasi]
                           tetapi tidak di KBBI"]   (Apakah sama dengan kata dasar?)
                                                               │
                                                 ┌─────────────┴─────────────┐
                                                (Ya)                        (Tidak)
                                                 │                             │
                                                 ▼                             ▼
                                        [LOG: "Gagal! Kata            [Pengecekan Redudansi]
                                        sama dengan kata dasar"]    (Apakah sudah pernah diinput?)
                                                                               │
                                                                 ┌─────────────┴─────────────┐
                                                                (Ya)                        (Tidak)
                                                                 │                             │
                                                                 ▼                             ▼
                                                        [LOG: "Sudah diisi!           [Pengecekan Kuota]
                                                         Kata sudah ada"]          (Apakah slot sudah penuh?)
                                                                                               │
                                                                                 ┌─────────────┴─────────────┐
                                                                                (Ya)                        (Tidak)
                                                                                 │                             │
                                                                                 ▼                             ▼
                                                                        [LOG: "Kolom penuh,          [STATUS: VALID & SUKSES]
                                                                        sudah isi 2 anagram"]        1. Masukkan kata ke dalam List
                                                                                                     2. Reset Timer ke waktu awal

```

---

## 5. Mekanisme Render Visual Multi-Slot

Perbedaan visual paling mencolok pada file `gameplay2.py` diatur pada bagian perulangan rendering kolom jawaban (`ROW2_Y`). Setiap kolom didesain bertingkat secara vertikal untuk menampilkan dua baris string secara bersamaan:

```python
# Membaca list data jawaban dari kata dasar saat ini
list_jawab = jawaban_user[kata]

# Slot ke-1 (Baris Atas di dalam kotak jawaban)
ans1 = list_jawab[0].upper() if len(list_jawab) >= 1 else "◦ ◦ ◦ ◦"
stdscr.addstr(ROW2_Y + 1, bx + 1 + pad_x1, ans1, attr1)

# Slot ke-2 (Baris Bawah di dalam kotak jawaban)
ans2 = list_jawab[1].upper() if len(list_jawab) == 2 else "◦ ◦ ◦ ◦"
stdscr.addstr(ROW2_Y + 2, bx + 1 + pad_x2, ans2, attr2)

```

Mekanisme kondisional `if len(list_jawab)` memastikan bahwa teks placeholder `◦ ◦ ◦ ◦` akan berubah menjadi string tebakan berformat huruf kapital satu per satu seiring keberhasilan pemain memecahkan anagram tersebut.

```

```
