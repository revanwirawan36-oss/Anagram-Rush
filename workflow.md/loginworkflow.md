```markdown
# Workflow & Logic Flow: `login.py` (Anagram Rush - Authentication System)

Dokumen ini menjelaskan alur logika, struktur fungsi, dan mekanika kerja dari file `login.py`[cite: 7]. File ini bertindak sebagai **pintu gerbang utama (Authentication & Data Persistence Layer)** yang mengelola proses pendaftaran akun baru, masuk ke akun lama, serta menyimpan perkembangan level pemain ke dalam berkas teks[cite: 7].

---

## 1. Penjelasan Umum File
File `login.py` bertugas mengamankan dan mengelola data pengguna dengan memanfaatkan sistem penyimpanan berbasis teks local (`user.txt`)[cite: 7]. Berbeda dengan input standar Python (`input()`), file ini mengadopsi penuh pustaka **`curses`** untuk membangun antarmuka grafis terminal bergaya retro[cite: 7]. 

Sistem ini memfasilitasi tiga fitur utama:
1.  **Sign Up (Registrasi):** Mendaftarkan *username* baru yang belum terpakai ke dalam sistem dengan level awal diset ke 1[cite: 7].
2.  **Login (Autentikasi):** Mencocokkan *username* dan *password* yang dimasukkan dengan data pada berkas teks[cite: 7].
3.  **Level Persistence:** Memperbarui data level tertinggi yang berhasil dicapai oleh pemain agar tidak mengulang dari level 1 saat game dibuka kembali[cite: 7].

---

## 2. Format Penyimpanan Data (`user.txt`)

Data pengguna disimpan dalam bentuk teks datar (*flat-file database*) dengan menggunakan karakter titik dua (`:`) sebagai pemisah (*delimiter*) antar kolom data[cite: 7]. Format penulisannya adalah:

```text
username:password:level_terbuka

```

Secara default, jika berkas `user.txt` belum terdeteksi di dalam folder proyek, fungsi `inisialisasi_database_file()` akan otomatis membuatkannya dengan menyuntikkan dua akun bawaan:

* `admin:alpro123:1`

* `kelompok:anagram:1`


---

## 3. Alur Logika Cara Kerja Program (Workflow)

Saat program utama menjalankan sistem autentikasi, fungsi `gerbang_awal(stdscr)` akan memicu rentetan logika berikut:

```
                        [Program Utama Dimulai]
                                   │
                                   ▼
                       [Fungsi: gerbang_awal()]
                                   │
                                   ▼
                    [Tampilkan Menu Utama Navigasi]
                 (Login Akun / Sign Up / Keluar Program)
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
 [Pilih: Login Akun]       [Pilih: Sign Up]          [Pilih: Keluar]
         │                         │                         │
         ▼                         ▼                         ▼
[Fungsi: tampilan_login]  [Fungsi: tampilan_signup]    [Kembalikan: False]
         │                         │                         │
         ├─► Validasi Sukses       ├─► Buat Akun Berhasil    └─► (Program Selesai)
         │   │                     │   (Simpan ke user.txt)
         │   ▼                     │
         │ [Kembalikan Data Tuple] ◄───┘
         │ (True, username, level)
         │
         ▼
[Masuk ke Menu Pilih Level]

```

### Detail Mekanisme Input Tersensor (`custom_input`)

Untuk mengamankan pengetikan kata sandi, dibuat fungsi kustom `custom_input(...)`. Fungsi ini membaca karakter per karakter tombol keyboard yang ditekan pemain via `stdscr.getch()`:

* Jika parameter `mask=True`, huruf asli yang diketik pemain akan disimpan ke dalam variabel string, namun layar terminal hanya akan mencetak karakter bintang (`*`).


* Fungsi ini juga mendeteksi tombol `Backspace` secara manual untuk menghapus memori string sekaligus memundurkan kursor dan menghapus karakter di layar terminal.



---

## 4. Alur Logika Validasi Pendaftaran Akun (Sign Up)

Ketika pengguna memilih menu "Sign Up", fungsi `tampilan_signup(stdscr)` dijalankan dengan urutan pemeriksaan sebagai berikut:

```
                     [Pengguna Mengisi Kolom Registrasi]
                                     │
                                     ▼
                      [Ambil Input New User & New Pass]
                                     │
                                     ▼
                   [Cek 1: Apakah salah satu kolom kosong?]
                                     │
                       ┌─────────────┴─────────────┐
                    (Benar)                     (Salah)
                       │                           │
                       ▼                           ▼
            [LOG: "Kolom tidak boleh         [Cek 2: Apakah Username
              kosong! Ulangi."]              sudah ada di database?"]
                                                           │
                                             ┌─────────────┴─────────────┐
                                          (Ada)                       (Belum)
                                             │                           │
                                             ▼                           ▼
                                    [LOG: "Username telah       [STATUS: REGISTRASI SUKSES]
                                     terdaftar! Ganti."]        1. Panggil tambah_akun_ke_file()
                                                                2. Tulis data format user:pass:1
                                                                3. Keluar menuju Gerbang Awal

```

---

## 5. Alur Logika Validasi Masuk Akun (Login)

Ketika pengguna mengisi kolom pada fungsi `tampilan_login(stdscr)`, data akan dicocokkan dengan *dictionary* `db_akun` yang diinisialisasi dari file teks:

* **Pemeriksaan Kondisi:**

```python
    if username in db_akun and db_akun[username]["password"] == password:
    ```
*   **Jika Kredensial Valid (Cocok):**
    Program membersihkan layar, mematikan visual kursor (`curses.curs_set(0)`), menampilkan notifikasi `"Login Berhasil! Sukses."`, dan mengembalikan data bertipe objek *Tuple*: `(True, username, db_akun[username]["level"])`[cite: 7]. Data *Tuple* inilah yang memberi tahu program utama mengenai siapa nama pemain dan sejauh mana level yang sudah berhasil ia buka[cite: 7].
*   **Jika Kredensial Salah:**
    Program memancarkan pesan galat `"Username/Password Salah! (Enter)"` menggunakan atribut cetak tebal `curses.A_BOLD`, lalu menahan layar hingga tombol Enter ditekan kembali untuk mengulang input[cite: 7].

---

## 6. Logika Sinkronisasi Data (`update_level_user`)

Fungsi `update_level_user(username_target, level_baru)` dipanggil dari luar file (biasanya dipicu ketika pemain memenangkan sebuah level di file gameplay)[cite: 5, 7]. 

Cara kerjanya adalah memanfaatkan metode **Tulis Ulang Total (Overwrite Mode)**[cite: 7]:
1.  Membaca seluruh isi file `user.txt` ke dalam memori RAM komputer berupa objek *dictionary* via `inisialisasi_database_file()`[cite: 7].
2.  Mengubah nilai tingkat level milik `username_target` di dalam struktur data memori tersebut[cite: 7].
3.  Membuka kembali berkas `user.txt` menggunakan mode `"w"` (*write*) yang otomatis mengosongkan/menghapus seluruh teks lama di dalam file[cite: 7].
4.  Melakukan perulangan looping untuk menuangkan kembali seluruh data akun dari memori RAM ke dalam file teks dengan kondisi level yang sudah diperbarui[cite: 7].

```
