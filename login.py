# login.py
import curses
import os

# Nama file teks yang bertindak sebagai database lokal tempat penyimpanan akun pemain
FILE_AKUN = "user.txt"

def inisialisasi_database_file():
    """Membaca username, password, dan progress level user dari file teks"""
    kredensial = {} # Dictionary kosong untuk menampung seluruh data akun di memori RAM
    
    # JIKA file database belum ada di komputer, otomatis buat baru dengan beberapa akun bawaan (default)
    if not os.path.exists(FILE_AKUN):
        with open(FILE_AKUN, "w", encoding="utf-8") as file:
            # Format penulisan di dalam file -> username:password:level_tertinggi
            file.write("admin:alpro123:1\n")
            file.write("kelompok:anagram:1\n")
            
    # Proses membaca data akun dari file teks baris demi baris
    with open(FILE_AKUN, "r", encoding="utf-8") as file:
        for baris in file:
            baris_bersih = baris.strip() # Menghapus karakter enter (\n) atau spasi di ujung baris
            
            # Validasi format: pastikan baris tidak kosong dan memiliki tepat 2 tanda titik dua (:)
            if baris_bersih and baris_bersih.count(":") == 2:
                username, password, level = baris_bersih.split(":")
                
                # Memasukkan data ke dalam struktur Nested Dictionary (Dictionary di dalam Dictionary)
                kredensial[username] = {
                    "password": password,
                    "level": int(level) # Konversi teks tingkat level menjadi tipe data integer
                }
                
    return kredensial # Mengembalikan seluruh data akun yang siap digunakan program

def tambah_akun_ke_file(username, password):
    """Menulis/mendaftarkan akun baru ke dalam file teks (Otomatis mulai dari level 1)"""
    # Menggunakan mode "a" (Append) agar data akun baru ditambahkan di baris paling bawah tanpa menghapus isi file
    with open(FILE_AKUN, "a", encoding="utf-8") as file:
        file.write(f"{username}:{password}:1\n")

def draw_box(stdscr, y, x, h, w, title=""):
    """Fungsi pembantu untuk menggambar kotak visual menggunakan karakter bingkai Unicode"""
    stdscr.addstr(y, x, "┌" + "─" * (w-2) + "┐")
    stdscr.addstr(y + h - 1, x, "└" + "─" * (w-2) + "┘")
    for i in range(1, h - 1):
        stdscr.addstr(y + i, x, "│")
        stdscr.addstr(y + i, x + w - 1, "│")
    if title:
        # Menempatkan teks judul tepat di tengah-tengah garis horizontal atas kotak bingkai
        stdscr.addstr(y, x + (w // 2) - (len(title) // 2), f" {title} ")

def form_input_curses(stdscr, prompt, y, x, is_password=False):
    """Pengganti fungsi input() biasa untuk menangkap ketikan user secara real-time di dalam library curses"""
    curses.curs_set(1)  # Tampilkan kursor pengetikan (garis kelap-kelip) agar user tahu posisi mengetik
    input_buffer = ""   # Variabel string untuk mengumpulkan karakter yang sedang diketik
    
    while True:
        stdscr.clear()
        # Menggambar ulang kotak pengetikan form input di terminal
        draw_box(stdscr, y, x, 5, 60, " INPUT FORM ")
        stdscr.addstr(y + 2, x + 3, prompt)
        
        # LOGIKA MASKING: Jika input adalah password, sembunyikan tulisan asli dengan karakter '*'
        if is_password:
            tampilan_teks = "*" * len(input_buffer)
        else:
            tampilan_teks = input_buffer
            
        stdscr.addstr(y + 2, x + 3 + len(prompt), tampilan_teks)
        stdscr.refresh()
        
        ch = stdscr.getch() # Menangkap input 1 karakter tombol dari keyboard pengguna
        
        if ch in (10, 13):  # 10 atau 13 melambangkan tombol ENTER (Artinya user selesai mengetik)
            break
        elif ch in (curses.KEY_BACKSPACE, 127, 8):  # Mendeteksi jika user menekan tombol HAPUS (Backspace)
            input_buffer = input_buffer[:-1]        # Memotong atau menghapus 1 karakter string paling belakang
        elif 32 <= ch <= 126:  # Memastikan karakter yang diketik adalah karakter teks normal yang valid (ASCII standar)
            if len(input_buffer) < 20: # Membatasi panjang maksimal input data yaitu 20 karakter
                input_buffer += chr(ch) # Mengubah kode angka desimal key menjadi bentuk Karakter Huruf/Angka
                
    curses.curs_set(0)  # Sembunyikan kembali kursor pengetikan setelah selesai mengisi form
    return input_buffer.strip()

def menu_utama_autentikasi(stdscr):
    """Menampilkan pilihan menu awal (Login / Sign Up / Keluar) dengan kontrol keyboard"""
    curses.curs_set(0)  # Menyembunyikan kursor standard terminal agar tampilan bersih
    stdscr.keypad(True) # Mengaktifkan fitur pembacaan tombol panah keyboard
    
    h, w = 12, 50       # Ukuran dimensi panjang dan lebar kotak menu utama
    pilihan_menu = ["Login Akun Lama", "Sign Up (Daftar Akun Baru)", "Keluar dari Program"]
    pilihan_aktif = 0   # Indeks penunjuk opsi menu yang sedang disorot kursor (0, 1, atau 2)
    
    while True:
        screen_y, screen_x = stdscr.getmaxyx() # Membaca resolusi ukuran terminal terupdate secara dinamis
        start_y = (screen_y - h) // 2          # Titik koordinat Y agar layout berada tepat di tengah layar
        start_x = (screen_x - w) // 2          # Titik koordinat X agar layout berada tepat di tengah layar
        
        stdscr.clear()
        draw_box(stdscr, start_y, start_x, h, w, "WELCOME TO ANAGRAM ARCHIVE")
        
        # Perulangan untuk menggambar opsi-opsi pilihan menu utama game
        for idx, menu in enumerate(pilihan_menu):
            pos_y = start_y + 3 + (idx * 2)
            if idx == pilihan_aktif:
                # Jika opsi menu sedang disorot, berikan tanda panah '►' dan efek warna terbalik (REVERSE)
                stdscr.addstr(pos_y, start_x + 5, f"► {menu}", curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(pos_y, start_x + 5, f"  {menu}")
                
        stdscr.refresh()
        tombol = stdscr.getch() # Membaca input navigasi keyboard dari user
        
        # LOGIKA NAVIGASI MENU (Menggunakan Operasi Aritmatika Sisa Bagi / Modulo)
        if tombol == curses.KEY_UP:
            pilihan_aktif = (pilihan_aktif - 1) % len(pilihan_menu)
        elif tombol == curses.KEY_DOWN:
            pilihan_aktif = (pilihan_aktif + 1) % len(pilihan_menu)
        elif tombol in (10, 13): # Jika tombol ENTER ditekan
            
            # --- BLOK PILIHAN 1: LOGIN AKUN ---
            if pilihan_aktif == 0:
                kredensial = inisialisasi_database_file() # Memuat ulang data user paling update dari file
                form_y = start_y + h + 1
                
                # Membuka form input pengisian username dan password
                user_input = form_input_curses(stdscr, "Username: ", form_y, start_x - 5)
                pass_input = form_input_curses(stdscr, "Password: ", form_y, start_x - 5, is_password=True)
                
                # VALIDASI LOGIN: Memeriksa apakah username terdaftar dan password-nya cocok di dictionary
                if user_input in kredensial and kredensial[user_input]["password"] == pass_input:
                    # Login Berhasil: Kembalikan status True, nama user, beserta level tertinggi mereka
                    return True, user_input, kredensial[user_input]["level"]
                else:
                    # Login Gagal: Tampilkan pesan peringatan kesalahan kredensial
                    stdscr.addstr(form_y + 6, start_x, "Username atau Password Salah!", curses.A_BOLD)
                    stdscr.refresh()
                    stdscr.getch()
            
            # --- BLOK PILIHAN 2: SIGN UP (DAFTAR AKUN BARU) ---
            elif pilihan_aktif == 1:
                kredensial = inisialisasi_database_file()
                form_y = start_y + h + 1
                
                user_input = form_input_curses(stdscr, "Username Baru: ", form_y, start_x - 5)
                
                # VALIDASI DATA: Mencegah nama kembar (double username)
                if user_input in kredensial:
                    stdscr.addstr(form_y + 6, start_x - 2, "Username sudah terdaftar! Gunakan nama lain.", curses.A_BOLD)
                    stdscr.refresh()
                    stdscr.getch()
                # VALIDASI FORMAT: Mencegah username terlalu pendek atau menggunakan spasi
                elif len(user_input) < 3 or " " in user_input:
                    stdscr.addstr(form_y + 6, start_x, "Username tidak valid (Min. 3 huruf, Tanpa Spasi)!", curses.A_BOLD)
                    stdscr.refresh()
                    stdscr.getch()
                else:
                    pass_input = form_input_curses(stdscr, "Password Baru: ", form_y, start_x - 5, is_password=True)
                    # VALIDASI PASSWORD: Mengamankan panjang minimum password
                    if len(pass_input) < 4:
                        stdscr.addstr(form_y + 6, start_x, "Password terlalu pendek! (Min. 4 Karakter)", curses.A_BOLD)
                        stdscr.refresh()
                        stdscr.getch()
                    else:
                        # Akun memenuhi seluruh syarat syarat, tulis data permanen ke dalam file teks
                        tambah_akun_ke_file(user_input, pass_input)
                        stdscr.addstr(form_y + 6, start_x + 5, "AKUN BERHASIL DAFTAR! SILAKAN LOGIN.", curses.A_BOLD)
                        stdscr.refresh()
                        stdscr.getch()
            
            # --- BLOK PILIHAN 3: KELUAR DARI PROGRAM ---
            elif pilihan_aktif == 2:
                return False, "", 1

def update_level_user(username, level_baru):
    """Mengupdate data progress pencapaian level tertinggi milik user di dalam file database teks"""
    kredensial = inisialisasi_database_file() # Ambil struktur dictionary terbaru
    if username in kredensial:
        # Perbarui nilai level tertinggi user di dalam memori RAM
        kredensial[username]["level"] = level_baru
        
        # Buka file dengan mode "w" (Write) untuk menulis ulang file teks secara keseluruhan berdasarkan data terbaru
        with open(FILE_AKUN, "w", encoding="utf-8") as file:
            for nama, data in kredensial.items():
                file.write(f"{nama}:{data['password']}:{data['level']}\n")

def jalankan_autentikasi():
    """Fungsi utama/wrapper pengeksekusi modul login secara aman menggunakan wrapper curses"""
    return curses.wrapper(menu_utama_autentikasi)
