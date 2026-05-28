```markdown
# Workflow & Logic Flow: `level.py` (Anagram Rush - Level Selection)

Dokumen ini menjelaskan alur logika, struktur fungsi, dan cara kerja dari file `level.py`[cite: 6]. File ini bertanggung jawab untuk menampilkan **antarmuka pemilihan level (Level Selection Menu)** menggunakan bentuk grid matriks berbasis teks (*TUI*) dengan pustaka `curses`[cite: 6].

---

## 1. Penjelasan Umum File
File `level.py` berfungsi sebagai jembatan halaman utama setelah pemain login, di mana pemain bisa memilih level game yang ingin dimainkan[cite: 6]. Program ini membatasi akses pemain dengan sistem *progression*: level yang lebih tinggi akan terkunci (`[LOCKED]`) jika pemain belum mencapai atau menyelesaikan level sebelumnya[cite: 6].

Antarmukanya dirancang dinamis menggunakan grid **2 baris × 5 kolom** untuk merepresentasikan total 10 level game[cite: 6].

---

## 2. Struktur Fungsi Utama

Program ini dibagi menjadi beberapa fungsi pembantu dan fungsi inti[cite: 6]:

* **`draw_box(stdscr, y, x, h, w, title)`**: Fungsi pembantu untuk menggambar kotak bingkai luar dekoratif menggunakan karakter Unicode (`┌`, `─`, `│`, `└`) disertai judul di tengah atas bingkai[cite: 6].
* **`menu_pilih_level(stdscr, username, max_level_user)`**: Fungsi inti yang memproses perulangan menu pemilihan level, merender kotak-kotak level, dan membaca navigasi tombol keyboard[cite: 6].
* **`jalankan_pemilihan_level(username, max_level_user)`**: Fungsi pembungkus (*wrapper*) agar pustaka `curses` dapat berjalan dan diinisialisasi dengan aman tanpa merusak terminal asli komputer[cite: 6].

---

## 3. Alur Logika Cara Kerja Program (Workflow)

Siklus menu pemilihan level berjalan di dalam perulangan `while True` dengan tahapan sebagai berikut[cite: 6]:

### Langkah 1: Validasi Ukuran Layar Terminal
Sebelum menggambar menu, program membaca ukuran resolusi terminal saat itu menggunakan `stdscr.getmaxyx()`[cite: 6]. 
* Jika ukuran layar terminal terlalu kecil (kurang dari tinggi 15 atau lebar 96 karakter), program akan berhenti menggambar, membersihkan layar, dan menampilkan pesan `"Perbesar ukuran terminal VS Code kamu!"` sampai layar diperbesar[cite: 6].

### Langkah 2: Perhitungan Posisi Tengah (*Centering*)
Setelah ukuran terminal valid, program menghitung titik awal koordinat `start_y` dan `start_x` agar kotak menu utama setinggi 15 dan selebar 96 karakter selalu berada tepat di tengah-tengah layar, tidak peduli seberapa besar ukuran terminal laptop pemain[cite: 6].

### Langkah 3: Perhitungan Posisi Grid Matriks 2x5
Program melakukan perulangan indeks dari `0` sampai `9` (Total 10 Level)[cite: 6]. Untuk mengubah indeks linear (`0-9`) menjadi koordinat baris dan kolom matriks, digunakan operasi matematika dasar komputer[cite: 6]:
* **`row = idx // KOLOM_GRID`**: Pembagian bulat untuk menentukan baris (Baris `0` untuk level 1-5, Baris `1` untuk level 6-10)[cite: 6].
* **`col = idx % KOLOM_GRID`**: Sisa pembagian (modulus) untuk menentukan urutan kolom keberapa (`0` sampai `4`)[cite: 6].

Koordinat kotak kecil setiap level diatur secara presisi berdasarkan hasil perkalian `row` dan `col` tersebut[cite: 6].

### Langkah 4: Pemeriksaan Status Level & Efek Sorot (*Highlight*)
* **Status Terbuka/Terkunci:** Program membandingkan nilai `nomor_level <= max_level_user`[cite: 6]. Jika benar, kotak menampilkan tulisan `LEVEL X`[cite: 6]. Jika salah, kotak menampilkan tulisan `[LOCKED]`[cite: 6].
* **Kursor Aktif:** Jika indeks level yang sedang diproses sama dengan variabel `pilihan_aktif`, maka kotak level tersebut akan dirender menggunakan atribut `curses.A_REVERSE | curses.A_BOLD` yang memberikan efek warna terbalik (sorotan kursor) agar pemain tahu level mana yang sedang ditunjuk[cite: 6].

---

## 4. Logika Navigasi Tombol Keyboard (Arrow Keys)

Program mendeteksi tombol arah panah pada keyboard dan memindahkan nilai `pilihan_aktif` dengan logika batas dinding (*wrapping loop*)[cite: 6]:

* **Panah Kiri (`KEY_LEFT`):** Mengurangi `pilihan_aktif` sebanyak 1 angka[cite: 6]. Jika kursor berada di ujung paling kiri baris, kursor otomatis melompat ke ujung paling kanan pada baris yang sama[cite: 6].
* **Panah Kanan (`KEY_RIGHT`):** Menambah `pilihan_aktif` sebanyak 1 angka[cite: 6]. Jika sudah di ujung kanan baris, kursor otomatis melompat kembali ke ujung paling kiri pada baris yang sama[cite: 6].
* **Panah Atas (`KEY_UP`):** Mengurangi `pilihan_aktif` sebanyak nilai `KOLOM_GRID` (lompat ke baris di atasnya)[cite: 6]. Jika sudah di baris paling atas, kursor melompat ke baris bawahnya secara vertikal[cite: 6].
* **Panah Bawah (`KEY_DOWN`):** Menambah `pilihan_aktif` sebanyak nilai `KOLOM_GRID` (lompat ke baris di bawahnya)[cite: 6]. Jika sudah di baris paling bawah, kursor kembali melompat ke baris atasnya[cite: 6].

---

## 5. Konfirmasi Pilihan (Tombol ENTER atau Q)

Ketika pemain memutuskan menekan tombol di keyboard[cite: 6]:

1. **Tombol 'Q' atau 'q':** Program langsung keluar dari fungsi dan mengembalikan nilai `None` untuk memicu kembali ke menu sebelumnya[cite: 6].
2. **Tombol ENTER (Kode 10 atau 13):** Program menghitung level yang dipilih menggunakan rumus `level_pilihan = pilihan_aktif + 1`[cite: 6].
   * **Jika `level_pilihan <= max_level_user` (Terbuka):** Fungsi berhasil selesai dan mengembalikan nomor level tersebut (`return level_pilihan`) untuk kemudian dimuat oleh file gameplay utama[cite: 6].
   * **Jika `level_pilihan > max_level_user` (Terkunci):** Program menampilkan pesan peringatan sementara `"LEVEL MASIH TERKUNCI!"` di bagian bawah menu dan menunggu tombol apa saja ditekan sebelum kembali ke menu navigasi[cite: 6].

```
