```markdown
# Workflow & Logic Flow: `menang_kalah.py` (Anagram Rush - End Game Screen)

Dokumen ini menjelaskan alur logika, kontrol eksekusi, dan cara kerja dari file `menang_kalah.py`[cite: 9]. File ini bertindak sebagai **Halaman Akhir Sesi (Game Over / Level Clear Screen)** yang menjembatani pemain setelah menyelesaikan atau gagal dalam suatu level game **Anagram Rush**[cite: 9].

---

## 1. Penjelasan Umum File
File `menang_kalah.py` memanfaatkan pustaka **`curses`** untuk menggambar menu akhir permainan secara dinamis di dalam terminal[cite: 9]. Tugas utamanya adalah menangkap status permainan (apakah pemain menang atau kalah karena kehabisan waktu), menampilkan pesan yang relevan, dan memberikan opsi tindakan selanjutnya kepada pemain[cite: 9].

Nilai kembalian (*return value*) dari file ini akan dikirimkan kembali ke konduktor utama (`main.py`) untuk menentukan apakah permainan harus diulang, kembali ke menu pemilihan level, atau ditutup secara aman.

---

## 2. Struktur Fungsi Utama (`tampilkan_menu_akhir`)

Fungsi inti dari file ini adalah `tampilkan_menu_akhir(stdscr, status, username)` yang menerima tiga parameter penting[cite: 9]:
* **`stdscr`**: Objek layar bawaan dari pustaka *curses*[cite: 9].
* **`status`**: Variabel bertipe *boolean* (`True` jika pemain menang, `False` jika pemain kalah/kehabisan waktu)[cite: 9].
* **`username`**: String nama pemain untuk memberikan kesan personalisasi pada pesan kemenangan[cite: 9].

---

## 3. Alur Logika Cara Kerja Program (Workflow)

Saat permainan berakhir di file gameplay, fungsi di dalam file ini dipicu dan mengeksekusi urutan logika sebagai berikut[cite: 9]:


```

```
                   [Permainan Sesi Level Selesai]
                                 │
                                 ▼
                 [Fungsi: tampilkan_menu_akhir()]
                                 │
                                 ▼
                 [Konfigurasi Awal Layar Curses]
           (Matikan nodelay, Aktifkan keypad, Sembunyikan kursor)
                                 │
                                 ▼
                  [Evaluasi Parameter: status]
                                 │
             ┌───────────────────┴───────────────────┐
         (True / MENANG)                         (False / KALAH)
             │                                       │
             ▼                                       ▼
   • Judul: LEVEL CLEAR!                   • Judul: TIME UP! LEVEL GAGAL
   • Pesan: Apresiasi Username             • Pesan: Peringatan waktu habis
   • Opsi : 2 Pilihan Menu                 • Opsi : 3 Pilihan Menu
   • Map  : {0: True, 1: "quit"}           • Map  : {0: "restart", 1: "menu", 2: "quit"}
             │                                       │
             └───────────────────┬───────────────────┘
                                 │
                                 ▼
                       [Loop Utama: while True]
                                 │
                                 ▼
                   [Hitung Resolusi Layar (sh, sw)]
                                 │
                                 ▼
                   [Cetak Judul & Pesan di Tengah]
                                 │
                                 ▼
                [Render List Opsi Menu (Looping)]
             (Berikan efek REVERSE pada pilihan_aktif)
                                 │
                                 ▼
                  [Tunggu Input Tombol Keyboard]
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
(Panah Atas)               (Panah Bawah)              (Tombol ENTER)
     │                           │                           │
     ▼                           ▼                           ▼

```

[pilihan_aktif - 1]         [pilihan_aktif + 1]       [Ambil data mapping_hasil]
(Gunakan Modulus %)         (Gunakan Modulus %)                  │
│                           │                           ▼
└───────────────────┬───────┘                 [Kembalikan Nilai (Return)]
│                            (Loop Selesai & Keluar)
▼
[Ulangi Loop Utama]

```

---

## 4. Mekanisme Kondisional & State Mapping

Program ini menggunakan teknik efisiensi kode yang sangat baik dengan memanfaatkan struktur data *Dictionary* (`mapping_hasil`) untuk mengubah indeks pilihan angka (`0, 1, 2`) menjadi instruksi string atau boolean yang dipahami oleh program utama[cite: 9]:

### Kondisi A: Pemain Menang (`status = True`)[cite: 9]
* **Judul**: `"=== LEVEL CLEAR! ==="`[cite: 9]
* **Pesan**: `"Luar biasa [Nama User]! Semua kata terpecahkan."`[cite: 9]
* **Daftar Opsi**: `["Kembali ke Menu Level", "Quit Game"]`[cite: 9]
* **Mapping Hasil**[cite: 9]:
  * Indeks `0` (Kembali ke Menu Level) $\rightarrow$ mengembalikan nilai `True`[cite: 9].
  * Indeks `1` (Quit Game) $\rightarrow$ mengembalikan nilai `"quit"`[cite: 9].

### Kondisi B: Pemain Kalah (`status = False`)[cite: 9]
* **Judul**: `"=== TIME UP! LEVEL GAGAL ==="`[cite: 9]
* **Pesan**: `"Waktu habis! Silakan pilih aksi:"`[cite: 9]
* **Daftar Opsi**: `["Restart Level", "Kembali ke Menu Level", "Quit Game"]`[cite: 9]
* **Mapping Hasil**[cite: 9]:
  * Indeks `0` (Restart Level) $\rightarrow$ mengembalikan nilai `"restart"`[cite: 9].
  * Indeks `1` (Kembali ke Menu Level) $\rightarrow$ mengembalikan nilai `"menu"`[cite: 9].
  * Indeks `2` (Quit Game) $\rightarrow$ mengembalikan nilai `"quit"`[cite: 9].

---

## 5. Logika Navigasi & Render Sentralisasi Visual

Untuk memastikan teks menu selalu berada tepat di tengah-tengah terminal meskipun ukuran jendela terminal berubah, digunakan perhitungan koordinat pembagian dua[cite: 9]:
* **`sh // 2`** dan **`sw // 2`**: Mencari titik koordinat tengah vertikal (*screen height*) dan horizontal (*screen width*)[cite: 9].
* **`(sw - len(teks)) // 2`**: Memundurkan titik awal cetak teks sejauh setengah dari panjang teks tersebut, sehingga teks tercetak seimbang di tengah layar[cite: 9].

### Efek Sorotan Kursor (*Highlighting*)
Saat melakukan perulangan `for idx, item in enumerate(opsi):`, program mengecek nilai indeks saat itu[cite: 9]:
* Jika `idx == pilihan_aktif`, program menambahkan karakter dekorasi ` > ` di sisi teks serta menyuntikkan atribut `curses.A_BOLD | curses.A_REVERSE` (teks tebal dengan warna latar belakang dan tulisan dibalik) untuk menandakan bahwa menu tersebut sedang ditunjuk[cite: 9].
* Jika tidak cocok, teks dirender biasa (`curses.A_NORMAL`)[cite: 9].

### Batas Navigasi Menggunakan Operator Modulus (`%`)
Agar kursor tidak *error* atau keluar batas saat menekan panah di ujung opsi menu, program memanfaatkan rumus sisa pembagian[cite: 9]:
* **`pilihan_aktif = (pilihan_aktif + 1) % len(opsi)`**[cite: 9]
* *Contoh pada menu Kalah (panjang opsi = 3):* Jika posisi berada di indeks `2` (Quit) dan menekan panah bawah, maka `(2 + 1) % 3 = 0`. Kursor otomatis melompat kembali ke atas (indeks `0`: Restart)[cite: 9]. Logika yang sama berlaku sebaliknya saat menekan panah atas[cite: 9].

```
