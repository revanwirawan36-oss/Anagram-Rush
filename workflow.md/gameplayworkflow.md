```markdown
# Workflow & Logic Flow: `gameplay.py` (Anagram Rush)

Dokumen ini menjelaskan alur logika, struktur fungsi, dan cara kerja dari `gameplay.py` yang bertugas sebagai **mesin utama (core engine) permainan** serta pengatur tampilan antarmuka (User Interface) berbasis teks menggunakan pustaka *Curses*.

---

## 1. Penjelasan Umum File
File `gameplay.py` adalah otak dari game **Anagram Rush**. Di sinilah seluruh interaksi pemain diproses secara *real-time*. File ini bertanggung jawab untuk:
* Mengurutkan huruf menggunakan algoritma **Bubble Sort** secara manual.
* Memvalidasi apakah kata yang diketik pemain merupakan anagram yang sah berdasarkan data dari `config.py` dan `database.py`.
* Menggambar antarmuka game (UI) di dalam terminal menggunakan pustaka **`curses`**, lengkap dengan kotak-kotak visual (*box-drawing*).
* Menangani input keyboard dari pemain secara langsung (*input polling*).

---

## 2. Struktur Fungsi Utama

Program ini dibagi menjadi beberapa fungsi modular agar mudah dipahami dan dikembangkan:

### A. Fungsi Logika & Validasi Anagram
* **`bubble_sort(arr)`**: Fungsi mengurutkan sebuah *array* (list) karakter secara alfabetis ($a \rightarrow z$) menggunakan algoritma Bubble Sort manual.
* **`cek_anagram_sorting(kata1, kata2)`**: Fungsi untuk mengecek kesamaan struktur anagram. Caranya dengan mengubah kedua kata menjadi list karakter, mengurutkannya dengan `bubble_sort`, lalu membandingkan kesamaan huruf demi huruf setelah terurut.

### B. Fungsi Desain Grafis Tampilan (UI)
* **`draw_box(...)`**: Menggambar kotak pembatas menggunakan karakter dekorasi tabel Unicode (`┌`, `─`, `│`, `└`).
* **`tulis_tengah_kotak(...)`**: Menghitung koordinat secara matematis agar teks tercetak tepat di tengah-tengah kotak (Center Alignment).
* **`render_pemeriksaan_box(...)`**: Menampilkan visualisasi proses pengurutan Bubble Sort dan status validasi kata secara *real-time* saat pemain sedang mengetik di kolom input.

### C. Game Loop Utama
* **`main_gameplay(stdscr, username, level)`**: Fungsi inti yang berisi *while loop* berjalan terus-menerus untuk memperbarui waktu (*timer*), merender ulang layar, dan membaca tombol keyboard yang ditekan pemain.

---

## 3. Alur Logika Cara Kerja Program (Workflow)

Saat level permainan dimulai, `gameplay.py` akan mengeksekusi logika dengan urutan sebagai berikut:

### Langkah 1: Inisialisasi Data Level & Curses
Program memuat konfigurasi waktu (*timer*) dan daftar kata dasar dari `config.py` berdasarkan level yang dipilih. Pustaka `curses` dikonfigurasi dalam mode `nodelay(True)` agar program tidak berhenti saat menunggu input keyboard, sehingga *timer* jam digital bisa terus berkurang setiap milidetik.

### Langkah 2: Siklus Rendering UI (Tampilan Layar)
Di dalam perulangan `while True`, layar terminal dibersihkan (`stdscr.clear()`), lalu program menghitung ukuran terminal secara dinamis (`stdscr.getmaxyx()`) untuk membagi layar menjadi 4 bagian kotak (Grid):
1.  **Kotak 1 (Baris Atas):** Menampilkan daftar **Kata Dasar** yang harus dicari anagramnya.
2.  **Kotak 2 (Baris Tengah):** Menampilkan **Jawaban User** yang berhasil ditebak. Jika belum menebak, kotak diisi simbol placeholder (`◦ ◦ ◦ ◦`).
3.  **Kotak 3 (Baris Bawah):** Kotak **Pemeriksaan Real-Time** yang memperlihatkan visualisasi *array* huruf yang sedang diurutkan oleh Bubble Sort berdasarkan apa yang sedang diketik pemain.
4.  **Kotak 4 (Paling Bawah):** Kolom tempat mengetik (**Kolom Input**) dan riwayat pesan (**Log Aktivitas**).

### Langkah 3: Menangani Input Pemain (*Input Polling*)
Program membaca tombol keyboard melalui `stdscr.getch()`.
* Jika pemain mengetik huruf biasa (`a-z`), karakter tersebut dimasukkan ke dalam `input_buffer`.
* Jika menekan tombol `Backspace`, karakter terakhir di dalam `input_buffer` dihapus.
* Jika menekan tombol `Q`, game akan langsung keluar (*Quit*).
* Jika menekan tombol **`ENTER`**, program akan mengunci string tersebut sebagai `kata_tebakan` dan masuk ke tahap **Validasi Berlapis**.

---

## 4. Alur Validasi Berlapis (Kondisi Enter)

Saat tombol `ENTER` ditekan, program menjalankan pemeriksaan logika yang ketat dengan urutan sebagai berikut:


```

```
              [Tombol ENTER Ditekan]
                        │
                        ▼
       [Cari Kecocokan Struktur Anagram]
         (Menggunakan cek_anagram_sorting)
                        │
          ┌─────────────┴─────────────┐
    (Tidak Cocok)                  (Cocok)
          │                           │
          ▼                           ▼
 [LOG: "Bukan Anagram          [Cek ke Validasi KBBI]
  dari kata mana pun!"]       (Apakah ada di kata_pilihan?)
                                      │
                        ┌─────────────┴─────────────┐
                     (Salah)                     (Benar)
                        │                           │
                        ▼                           ▼
               [LOG: "Anagram cocok,        [Cek: Apakah kata
               tapi tidak ada di KBBI"]     sama dengan kata dasar?]
                                                    │
                                      ┌─────────────┴─────────────┐
                                   (Sama)                      (Beda)
                                      │                           │
                                      ▼                           ▼
                             [LOG: "Gagal! Kata          [Cek: Apakah kolom
                             sama dengan kata dasar"]    sudah pernah diisi?]
                                                                  │
                                                    ┌─────────────┴─────────────┐
                                                 (Sudah)                     (Belum)
                                                    │                           │
                                                    ▼                           ▼
                                           [LOG: "Sudah diisi /         [STATUS: BERHASIL!]
                                          terisi anagram lain"]         - Masukkan ke Jawaban User
                                                                        - Reset Timer Level

```

```

---

## 5. Kondisi Menang dan Kalah

Siklus perulangan game akan berakhir secara otomatis jika memenuhi salah satu dari dua kondisi di bawah ini:

* **Kondisi Kalah (Waktu Habis):**
    Setiap putaran *loop*, waktu dihitung menggunakan rumus $\text{waktu\_tersisa} = \text{timer\_awal} - (\text{time.time()} - \text{waktu\_mulai})$. Jika hasil perhitungan $\le 0$, fungsi `tampilkan_menu_akhir(stdscr, False, username)` dipanggil untuk memicu layar *Game Over*.
* **Kondisi Menang (Semua Terjawab):**
    Menggunakan perintah Python `all(...)`. Jika seluruh kata dasar di dalam *dictionary* `jawaban_user` sudah memiliki nilai (tidak lagi bernilai `None`), game mendeteksi bahwa semua tebakan telah terjawab dengan benar. Fungsi `tampilkan_menu_akhir(stdscr, True, username)` dipanggil untuk memicu layar kemenangan (*Victory*).

```
