# login.py
import curses
import os

#nama file untuk menyimpan data akun (username, password, level)
FILE_AKUN = "user.txt"

def inisialisasi_database_file():
    """Membaca username, password, dan level user dari file"""
    kredensial = {}
    
    if not os.path.exists(FILE_AKUN):
        with open(FILE_AKUN, "w", encoding="utf-8") as file:
            #akun default
            file.write("admin:alpro123:1\n")
            file.write("kelompok:anagram:1\n")
            
    with open(FILE_AKUN, "r", encoding="utf-8") as file:
        for baris in file:
            baris_bersih = baris.strip()
            if baris_bersih and baris_bersih.count(":") == 2:
                username, password, level = baris_bersih.split(":")
                #simpan password dan level pada dict
                kredensial[username] = {
                    "password": password,
                    "level": int(level)
                }
                
    return kredensial

def tambah_akun_ke_file(username, password):
    """Menulis akun baru ke file, otomatis mulai dari level 1"""
    with open(FILE_AKUN, "a", encoding="utf-8") as file:
        file.write(f"{username}:{password}:1\n")

def draw_box(stdscr, y, x, h, w, title=""):
    """Fungsi pembantu membuat kotak visual di curses"""
    stdscr.addstr(y, x, "┌" + "─" * (w-2) + "┐")
    stdscr.addstr(y + h - 1, x, "└" + "─" * (w-2) + "┘")
    for i in range(1, h - 1):
        stdscr.addstr(y + i, x, "│")
        stdscr.addstr(y + i, x + w - 1, "│")
    if title:
        stdscr.addstr(y, x + (w // 2) - (len(title) // 2), f" {title} ")

def custom_input(stdscr, y, x, max_len, mask=False):
    """Fungsi mengambil input teks: kursor terkunci di dalam kotak"""
    curses.noecho()
    input_str = ""
    stdscr.move(y, x)
    
    while True:
        _, current_x = stdscr.getyx()
        ch = stdscr.getch()
        
        if ch in (10, 13): #enter
            break
        elif ch in (8, 127, curses.KEY_BACKSPACE): #backspace
            if len(input_str) > 0:
                input_str = input_str[:-1]
                stdscr.move(y, current_x - 1)
                stdscr.addch(' ')
                stdscr.move(y, current_x - 1)
        elif 32 <= ch <= 126: #karakter yang bisa dicetak
            if len(input_str) < max_len:
                char = chr(ch)
                input_str += char
                if mask:
                    stdscr.addch(y, current_x, '*')
                else:
                    stdscr.addch(y, current_x, char)
                stdscr.move(y, current_x + 1)
                
        stdscr.refresh()
    return input_str

def tampilan_login(stdscr):
    curses.curs_set(1)
    h, w = 14, 60
    
    while True:
        db_akun = inisialisasi_database_file()
        
        screen_y, screen_x = stdscr.getmaxyx()
        start_y = (screen_y - h) // 2
        start_x = (screen_x - w) // 2
        
        stdscr.clear()
        draw_box(stdscr, start_y, start_x, h, w, "LOGIN SYSTEM")
        
        stdscr.addstr(start_y + 3, start_x + 5, "Username : ")
        draw_box(stdscr, start_y + 2, start_x + 18, 3, 36)
        stdscr.addstr(start_y + 7, start_x + 5, "Password : ")
        draw_box(stdscr, start_y + 6, start_x + 18, 3, 36)
        
        stdscr.addstr(start_y + 11, start_x + (w // 2) - 21, "[ Tekan ENTER setelah mengisi tiap kolom ]")
        stdscr.refresh()
        
        username = custom_input(stdscr, start_y + 3, start_x + 20, 32, mask=False)
        password = custom_input(stdscr, start_y + 7, start_x + 20, 32, mask=True)
        
        #mengecek kredensial login dengan database file txt
        if username in db_akun and db_akun[username]["password"] == password:
            curses.curs_set(0)
            stdscr.clear()
            draw_box(stdscr, (screen_y - 5) // 2, (screen_x - w) // 2, 5, w, "STATUS")
            stdscr.addstr((screen_y - 5) // 2 + 2, (screen_x - w) // 2 + (w // 2) - 11, "Login Berhasil! Sukses.")
            stdscr.refresh()
            stdscr.getch()
            
            #return tuple
            return True, username, db_akun[username]["level"]
        else:
            stdscr.addstr(start_y + 10, start_x + (w // 2) - 18, "Username/Password Salah! (Enter)", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            
def update_level_user(username_target, level_baru):
    """Fungsi untuk memperbarui level user di file user.txt saat berhasil naik level"""
    db_akun = inisialisasi_database_file()
    
    if username_target in db_akun:
        db_akun[username_target]["level"] = level_baru
        
        #tulis ulang seluruh database ke file untuk menyimpan perubahan level
        with open(FILE_AKUN, "w", encoding="utf-8") as file:
            for user, data in db_akun.items():
                file.write(f"{user}:{data['password']}:{data['level']}\n")

def tampilan_signup(stdscr):
    curses.curs_set(1)
    h, w = 14, 60
    
    while True:
        db_akun = inisialisasi_database_file()
        
        screen_y, screen_x = stdscr.getmaxyx()
        start_y = (screen_y - h) // 2
        start_x = (screen_x - w) // 2
        
        stdscr.clear()
        draw_box(stdscr, start_y, start_x, h, w, "SIGN UP SYSTEM")
        
        stdscr.addstr(start_y + 3, start_x + 5, "New User : ")
        draw_box(stdscr, start_y + 2, start_x + 18, 3, 36)
        
        stdscr.addstr(start_y + 7, start_x + 5, "New Pass : ")
        draw_box(stdscr, start_y + 6, start_x + 18, 3, 36)
        
        stdscr.addstr(start_y + 11, start_x + (w // 2) - 17, "[ Buat akun barumu di kolom atas ]")
        stdscr.refresh()
        
        new_user = custom_input(stdscr, start_y + 3, start_x + 20, 32, mask=False).strip()
        new_pass = custom_input(stdscr, start_y + 7, start_x + 20, 32, mask=True).strip()
        
        if not new_user or not new_pass:
            stdscr.addstr(start_y + 10, start_x + (w // 2) - 16, "Kolom tidak boleh kosong! (Enter)", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
            continue
            
        #ngecek apakah username sudah ada di database file txt
        if new_user in db_akun:
            stdscr.addstr(start_y + 10, start_x + (w // 2) - 16, "Username sudah terdaftar! (Enter)", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
        else:
            #simpan akun baru ke file txt dengan level awal 1
            tambah_akun_ke_file(new_user, new_pass)
            
            curses.curs_set(0)
            stdscr.clear()
            draw_box(stdscr, (screen_y - 5) // 2, (screen_x - w) // 2, 5, w, "STATUS")
            stdscr.addstr((screen_y - 5) // 2 + 2, (screen_x - w) // 2 + (w // 2) - 17, "Registrasi Berhasil! Silakan Login.")
            stdscr.refresh()
            stdscr.getch()
            break

def gerbang_awal(stdscr):
    """Sistem Menu Utam dengan Navigasi Panah (Arrow Keys)"""
    curses.curs_set(0)
    stdscr.keypad(True)
    
    #pastikan file database akun sudah ada dan bisa diakses sebelum menampilkan menu utama
    inisialisasi_database_file()
    
    h, w = 12, 50
    pilihan_menu = ["Login Akun Lama", "Sign Up (Daftar Akun Baru)", "Keluar dari Program"]
    pilihan_aktif = 0
    
    while True:
        screen_y, screen_x = stdscr.getmaxyx()
        start_y = (screen_y - h) // 2
        start_x = (screen_x - w) // 2
        
        stdscr.clear()
        draw_box(stdscr, start_y, start_x, h, w, "WELCOME TO ANAGRAM ARCHIVE")
        
        for idx, menu in enumerate(pilihan_menu):
            pos_y = start_y + 3 + (idx * 2)
            if idx == pilihan_aktif:
                stdscr.addstr(pos_y, start_x + 5, f"► {menu}", curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(pos_y, start_x + 5, f"  {menu}")
                
        stdscr.refresh()
        tombol = stdscr.getch()
        
        if tombol == curses.KEY_UP:
            pilihan_aktif = (pilihan_aktif - 1) % len(pilihan_menu)
        elif tombol == curses.KEY_DOWN:
            pilihan_aktif = (pilihan_aktif + 1) % len(pilihan_menu)
        elif tombol in (10, 13): # Tombol ENTER
            if pilihan_aktif == 0: 
                hasil_login = tampilan_login(stdscr)
                if hasil_login: # Jika berhasil login
                    return hasil_login # me-return (True, username, level)
            elif pilihan_aktif == 1: 
                tampilan_signup(stdscr)
            elif pilihan_aktif == 2: 
                return False

def jalankan_autentikasi():
    return curses.wrapper(gerbang_awal)