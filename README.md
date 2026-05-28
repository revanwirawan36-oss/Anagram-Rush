# 🏆 Tugas Akhir Matkul Algoritma Pemrograman (ALPRO)
# 🎯 Anagram-Rush: Program Analisis & Game Olah Kata

**Proyek Game Terminal Python Menggunakan Curses & Manual Bubble Sort**

Anagram-Rush adalah *game* berbasis terminal interaktif yang dirancang untuk melatih fokus, kecepatan berpikir, dan penguasaan kosakata bahasa Indonesia. Permainan ini memanfaatkan visualisasi teks secara *real-time* untuk menguji aspek pengolahan string, pencarian data kata, serta validasi pola karakter menggunakan algoritma pengurutan manual.

Proyek ini dikembangkan menggunakan bahasa pemrograman Python dan pustaka `curses` sebagai pemenuhan komponen penilaian Tugas Akhir / Ujian Akhir Praktikum (UAP) Algoritma Pemrograman, Jurusan Ilmu Komputer, Universitas Lampung.

---

## 🧭 Daftar Isi
1. [Latar Belakang Proyek (Misi Analisis Kata)](#1-latar-belakang-proyek-misi-analisis-kata)
2. [Fungsi Game: Pelatihan Kecerdasan Taktis](#2-fungsi-game-pelatihan-kecerdasan-taktis)
3. [Fitur Universal & Mekanika](#3-fitur-universal--mekanika)
4. [Input Kontrol](#4-input-kontrol)
5. [Spesifikasi Teknis & Alur Validasi Anagram](#5-spesifikasi-teknis--alur-validasi-anagram)
6. [Kredit Kelompok](#6-kredit-kelompok)

---

## 📖 1. Latar Belakang Proyek (Misi Analisis Kata)

Dalam studi ilmu komputer, pemrosesan teks (*string manipulation*) dan pengenalan pola merupakan fondasi penting dalam penyusunan algoritma pencarian. Salah satu tantangan klasik linguistik komputasi adalah mengidentifikasi kesamaan absolut dari sekumpulan karakter acak tanpa memedulikan urutannya, yang dikenal sebagai konsep **Anagram**.

Banyaknya kosakata terkadang membuat manusia kesulitan mengidentifikasi kesamaan pembentuk kata secara cepat. Permainan **Anagram-Rush** ini hadir sebagai visualisasi interaktif dari penerapan penataan struktur array karakter secara berurutan. Di bawah tekanan waktu (*countdown timer*) yang berjalan secara *real-time*, pengguna ditantang untuk berpikir taktis, sementara sistem di latar belakang secara aktif membandingkan susunan elemen karakter menggunakan algoritma internal guna menyaring mana kata yang valid secara semantik bahasa dan mana yang murni berupa kesalahan struktural.

---

## 🧠 2. Fungsi Game: Pelatihan Kecerdasan Taktis

Program ini dirancang tidak hanya sebagai pemenuhan fungsionalitas kode, melainkan juga sebagai instrumen stimulasi kognitif yang melatih **memori kerja leksikal**, **kecepatan reaksi**, dan **fungsi eksekutif** Anda melalui dua tingkat kesulitan permainan:

### 🌟 Mode Normal (Level 1–5)
* **Fokus:** Berjalan melalui modul `gameplay.py`. Pemain fokus pada **kecepatan reaksi** dan **strategi pencarian kata dasar** tunggal di bawah batasan waktu yang ketat. Pemain cukup melengkapi 1 slot anagram valid untuk tiap kata acak yang disajikan.

### 🔥 Mode Hard (Level 6–10)
* **Tujuan:** Menguji daya ingat kosa kata dan kalkulasi ganda Anda secara simultan melalui modul `gameplay2.py`. Antarmuka permainan menyediakan **2 slot jawaban bertingkat** untuk setiap kata dasar yang wajib dipenuhi.
* **Tantangan Ekstra:** Membutuhkan pencarian anagram yang lebih luas, memaksa pemain untuk mengekstrak minimal 2 kata unik valid dari satu rangkaian huruf acak yang sama tanpa boleh terjadi duplikasi entri.
* **Pengecekan Real-time:** Setiap kali input dikirimkan, sistem akan melakukan validasi silang terhadap database untuk mendeteksi kecocokan susunan karakter secara presisi sebelum waktu habis.

---

## 🎮 3. Fitur Universal & Mekanika

| Fitur Mekanika | Detail Universal |
| :---: | :--- |
| **Sistem Tampilan** | Menggunakan modul `curses` untuk rendering antarmuka berbasis teks (CLI) yang responsif. |
| **Mode Pemain** | Pemain Tunggal (*Single-player*) memasukkan kata secara interaktif langsung dari keyboard. |
| **Preprocessing Teks** | Bersifat *Case-Insensitive* dengan melakukan normalisasi penuh huruf menggunakan method `.lower()` sebelum dianalisis. |
| **Sistem Akun & Skor** | Data autentikasi login pengguna dan pencatatan skor akhir disimpan secara permanen di dalam berkas lokal `user.txt`. |
| **Dataset Kamus** | Memuat file eksternal `kata_indonesia.txt` berisi puluhan ribu kosakata bahasa Indonesia sebagai basis data validasi kata nyata. |

### Perbandingan Karakteristik File Gameplay

| Fitur / Modul | Mode Normal (`gameplay.py`) | Mode Hard (`gameplay2.py`) |
| :---: | :---: | :---: |
| **Target per Kata** | 1 Kata Anagram Valid | **2 Kata Anagram Valid** (Bertingkat) |
| **Rentang Level** | Level 1 sampai Level 5 | **Level 6 sampai Level 10** |
| **Kriteria Kelulusan** | Menebak sukses 5 kata dasar berturut-turut | **Menebak sukses 10 kata dasar berturut-turut** |
| **Slot Rendering** | 1 Baris Slot Pengisian | 2 Baris Slot Pengisian Berpasangan |

### 🧭 Komponen Arsitektur Program
* `main.py` : Berkas utama (*entry point*) yang pertama kali dijalankan untuk memicu seluruh sistem.
* `login.py` : Menangani antarmuka autentikasi pengguna dan pembuatan profil pemain baru.
* `level.py` : Mengatur logika manajemen kenaikan level (Total batas maksimal hingga 10 level).
* `database.py` : Memuat fungsi `kata_pilihan` untuk menyuplai kata acak dan melakukan query pencarian kata dari kamus utama.
* `config.py` : Menyimpan variabel konfigurasi global dan konstanta permainan (`CONFIG_LEVEL`).
* `menang_kalah.py` : Mengurus penampilan visual menu akhir (*Victory / Game Over screen*) saat permainan selesai.

---

## 🔑 4. Input Kontrol

Antarmuka dibangun secara responsif mendeteksi kode ketukan papan tik (*keyboard input handling*) melalui fungsi pengikatan *loop* bawaan dari pustaka `curses`:

| Aksi | Tombol | Keterangan |
| :---: | :---: | :--- |
| **Ketik Jawaban** | **Tombol Alfabet A-Z / a-z** | Memasukkan huruf ke dalam penampung teks aktif (`input_buffer`). |
| **Kirim Kata** | **ENTER** (`\n` / `\r`) | Menyerahkan tebakan kata ke sistem untuk divalidasi secara algoritmik. |
| **Hapus Huruf** | **BACKSPACE** | Melakukan pemotongan karakter paling belakang untuk mengoreksi salah ketik. |
| **Keluar Game** | **Q** / **q** | Menghentikan permainan seketika dan keluar dari *game loop*. |

---

## 🎨 5. Spesifikasi Teknis & Alur Validasi Anagram

Sesuai ketentuan tugas akhir mata kuliah Algoritma Pemrograman, program ini dilarang keras menggunakan fungsi pengurutan bawaan Python (seperti `sorted()` atau `.sort()`). Pengecekan kemiripan karakter diimplementasikan secara mandiri menggunakan **Algoritma Pengurutan Manual Bubble Sort** pada file `gameplay.py` dan `gameplay2.py`:

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

---

## 👥 6. Kredit Kelompok

Proyek Tugas Akhir mata kuliah Algoritma Pemrograman ini dikembangkan oleh:

| Nama Anggota | NPM |
| :--- | :---: |
| **Muhammad Revan Wirawan** | 2517051010 |
| **Isma Eru Salsabila** | 2517051018 |
| **Talitha Reva Nabila** | 2517051020 |
| **Adinda Alifia Az Zahra** | 2517051027 |
| **Afifah Raidhatu Nasya** | 2517051043 |
