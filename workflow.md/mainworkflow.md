```markdown
# Workflow & Logic Flow: `main.py` (Anagram Rush - Entry Point)

Dokumen ini menjelaskan alur logika, kontrol eksekusi, dan cara kerja dari file `main.py`. File ini bertindak sebagai **Konduktor Utama (Entry Point)** yang mengintegrasikan seluruh modul game **Anagram Rush**, mulai dari autentikasi akun, pemilihan level, hingga sistem pengulangan (*looping*) gameplay.

---

## 1. Penjelasan Umum File
File `main.py` adalah pintu gerbang pertama yang dieksekusi saat game dijalankan. Tugas utama dari file ini bukan memproses visual grafik atau mengecek kata, melainkan **mengatur alur perpindahan antar halaman (State Management)**. 

File ini mengontrol kapan pemain harus berada di menu login, kapan masuk ke menu pilih level, kapan masuk ke arena permainan, serta bagaimana data hasil pertandingan (Menang/Kalah/Restart/Quit) diproses secara aman.

---

## 2. Dependencies & Struktur Modul
Sebagai pusat kendali, `main.py` mengimpor fungsi-fungsi spesifik dari berkas Python lainnya yang sudah dibuat secara modular:
* `login`: Mengambil fungsi `jalankan_autentikasi` dan `update_level_user`.
* `level`: Mengambil fungsi `jalankan_pemilihan_level`.
* `gameplay`: Mengambil fungsi `jalankan_gameplay_level` (untuk Level 1-5).
* `gameplay2`: Mengambil fungsi `jalankan_gameplay_level` yang dinamai ulang sebagai `jalankan_gameplay_level_hard` (untuk Level 6-10).

---

## 3. Alur Logika Cara Kerja Program (Workflow)

Program ini menggunakan struktur **Nested Loop (Perulangan Bersarang)** yang sangat rapi untuk melacak status game. Berikut adalah diagram alur jalannya program dari awal hingga selesai:


```

```
              [Mulai Run main.py]
                       │
                       ▼
          [Fungsi: jalankan_autentikasi()]
                       │
         ┌─────────────┴─────────────┐
 (Akses Ditolak/Quit)        (Akses Diterima)
         │                           │
         ▼                           ▼
 [Tutup Program]          [Loop 1: Menu Pilih Level]
                                     │
                                     ▼
                         [Fungsi: jalankan_pemilihan_level()]
                                     │
                       ┌─────────────┴─────────────┐
                    (Batal/Q)                 (Level Dipilih)
                       │                           │
                       ▼                           ▼
                [Tutup Program]         [Loop 2: Inti Gameplay]
                                                   │
                                                   ▼
                                        [Evaluasi hasil_game]
                                                   │
           ┌──────────────┬────────────────────────┼──────────────┐
           ▼              ▼                        ▼              ▼
       ["quit"]      ["restart"]           ["menu" / False]    [True (Menang)]
           │              │                        │              │
           ▼              ▼                        ▼              ▼
     [Exit Game]   [Continue Loop 2]        [Break Loop 2]   [Cek Progress Level]
                   (Main ulang level)      (Kembali ke Loop 1)    │
                                                                  ▼
                                                          [Apakah Level Baru?]
                                                           ├─► YA: Naik Level &
                                                           │       update_level_user()
                                                           └─► TIDAK: Tetap
                                                                  │
                                                                  ▼
                                                            [Break Loop 2]

```

```

### Detail Langkah Per Langkah:

### Langkah 1: Tahap Autentikasi Pengguna
Saat fungsi `main()` dipanggil, hal pertama yang dieksekusi adalah proses login/registrasi:
```python
status_akses, username, level_tertinggi = jalankan_autentikasi()

```

Jika `status_akses` bernilai `False` (user memilih keluar dari menu login), program akan langsung masuk ke blok `else`, membersihkan layar, mencetak pesan salam penutup, dan program selesai. Jika `True`, data `username` dan `level_tertinggi` disimpan ke dalam memori untuk digunakan di tahap berikutnya.

### Langkah 2: Loop 1 - Navigasi Menu Pemilihan Level

Ketika sukses login, program memasuki perulangan pertama (`while True:`). Di sini, fungsi `jalankan_pemilihan_level(username, level_tertinggi)` dipanggil.

* Jika pemain menekan tombol `Q` di menu level, fungsi mengembalikan `None`. Program mendeteksi ini, keluar dari loop pemilihan level, dan game ditutup.
* Jika pemain memilih level yang valid, nomor level disimpan di variabel `level_dipilih` dan program lanjut ke Loop 2.

### Langkah 3: Loop 2 - Manajemen Sesi Gameplay & Fitur Restart

Program memasuki perulangan kedua (internal loop) untuk menangani sesi permainan. Di dalam blok ini, program langsung melakukan percabangan otomatis berdasarkan tingkat kesulitan:

* **Level 1 sampai 5:** Menjalankan mode normal lewat fungsi `jalankan_gameplay_level()`.
* **Level 6 sampai 10:** Menjalankan mode sulit (Hard Mode) lewat fungsi `jalankan_gameplay_level_hard()`.

Hasil akhir dari game ditampung ke dalam variabel `hasil_game`.

---

## 4. Logika Evaluasi Status `hasil_game` (State Handling)

Setelah game selesai dimainkan (baik karena waktu habis atau berhasil menjawab), variabel `hasil_game` dievaluasi menggunakan percabangan kondisional `if-elif`:

1. **Jika `hasil_game == "quit"`:**
Pemain memilih keluar dari game secara total saat berada di dalam arena pertandingan. Program membersihkan layar terminal, mencetak teks perpisahan, dan menggunakan perintah `return` untuk menghentikan fungsi `main()` secara paksa.
2. **Jika `hasil_game == "restart"`:**
Pemain menekan tombol restart (atau memilih menu restart setelah kalah). Program memanggil perintah `continue` pada Loop 2, sehingga program akan mengabaikan kode di bawahnya dan langsung memicu ulang level yang sama tanpa kembali ke menu pemilihan level.
3. **Jika `hasil_game == "menu"` atau `False`:**
Pemain memilih kembali ke menu utama atau kalah dan tidak ingin mengulang. Program memanggil perintah `break` untuk mematahkan Loop 2, sehingga alur program otomatis mundur ke Loop 1 (Menu Pemilihan Level).
4. **Jika `hasil_game is True` (Pemain MENANG):**
Program menjalankan logika penyimpanan kemajuan (*save game progression*):
```python
if level_dipilih == level_tertinggi and level_tertinggi < 10:
    level_tertinggi += 1
    update_level_user(username, level_tertinggi)

```


*Logika:* Progress level baru akan bertambah dan disimpan ke file database (`user.txt`) **hanya jika** pemain memenangkan level tertinggi yang baru saja ia buka (bukan hasil mengulang level rendah yang sudah pernah dimanginya dahulu). Setelah data tersimpan, perintah `break` dipanggil untuk kembali ke halaman menu level.

---

```
