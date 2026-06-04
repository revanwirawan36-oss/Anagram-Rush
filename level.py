import curses

def draw_box(stdscr, y, x, h, w, title=""):
    """
    Fungsi utilitas untuk merender bingkai luar (border) persegi panjang.
    Memanfaatkan karakter box-drawing Unicode agar visual terminal rapi.
    """
    stdscr.addstr(y, x, "┌" + "─" * (w-2) + "┐")
    stdscr.addstr(y + h - 1, x, "└" + "─" * (w-2) + "┘")
    for i in range(1, h - 1):
        stdscr.addstr(y + i, x, "│")
        stdscr.addstr(y + i, x + w - 1, "│")
    if title:
        # Menempatkan judul string tepat di bagian tengah atas bingkai
        stdscr.addstr(y, x + (w // 2) - (len(title) // 2), f" {title} ")

def menu_pilih_level(stdscr, username, max_level_user):
    """
    Sistem navigasi pemilihan level menggunakan konsep struktur data Grid Matriks 2x5.
    Menggunakan library curses untuk menangkap input keyboard secara real-time.
    """
    curses.curs_set(0) # Menyembunyikan kursor pengetikan standar terminal
    stdscr.keypad(True) # Mengaktifkan pembacaan tombol khusus (tombol panah keyboard)

    # --- DEKLARASI KONFIGURASI DAN DIMENSI GRID ---
    TOTAL_LEVEL = 10
    KOLOM_GRID = 5  # Representasi jumlah kolom maksimum dalam satu baris horizontal
    pilihan_aktif = 0  # Menyimpan indeks posisi level yang sedang disorot (0 sampai 9)
    
    # Menentukan dimensi lebar dan tinggi kotak pembungkus utama dan elemen level
    h_box, w_box = 15, 96
    h_kotak, w_kotak = 3, 14
    
    while True:
        # Mengambil resolusi atau ukuran dimensi layar terminal saat ini
        screen_y, screen_x = stdscr.getmaxyx()
        
        # Validasi batas minimum ukuran terminal untuk mencegah error penggambaran koordinat
        if screen_y < h_box or screen_x < w_box:
            stdscr.clear()
            stdscr.addstr(0, 0, "Perbesar ukuran terminal VS Code kamu!")
            stdscr.refresh()
            stdscr.getch()
            continue
            
        # Kalkulasi koordinat titik tengah (centering layout) agar menu presisi di tengah layar
        start_y = (screen_y - h_box) // 2
        start_x = (screen_x - w_box) // 2
        
        stdscr.clear()
        draw_box(stdscr, start_y, start_x, h_box, w_box, f"LEVEL SELECT - {username.upper()}")
        
        # Iterasi looping untuk merender matriks tingkatan level (Level 1 s.d. Level 10)
        for idx in range(TOTAL_LEVEL):
            nomor_level = idx + 1
            
            # Konversi indeks linear menjadi koordinat baris (row) dan kolom (col) matriks
            row = idx // KOLOM_GRID
            col = idx % KOLOM_GRID
            
            # Kalkulasi posisi koordinat spesifik untuk masing-masing kotak level
            box_y = start_y + 2 + (row * 4)
            box_x = start_x + 5 + (col * 18)
            
            # Evaluasi hak akses pemain berdasarkan rekor level tertinggi di file database
            terbuka = nomor_level <= max_level_user
            
            if terbuka:
                teks_level = f"  LEVEL {nomor_level:02d}  "
            else:
                teks_level = f"  [LOCKED]  "
            
            # --- MEKANISME RENDERING DAN HIGHLIGHT ELEMEN GRUP ---
            # Jika elemen indeks saat ini cocok dengan posisi kursor pilihan pengguna
            if idx == pilihan_aktif:
                # Merender kotak dengan atribut teks terbalik (Reverse Video) dan cetak tebal (Bold)
                stdscr.addstr(box_y,     box_x, "┌" + "─" * (w_kotak-2) + "┐", curses.A_REVERSE | curses.A_BOLD)
                stdscr.addstr(box_y + 1, box_x, f"│{teks_level}│", curses.A_REVERSE | curses.A_BOLD)
                stdscr.addstr(box_y + 2, box_x, "└" + "─" * (w_kotak-2) + "┘", curses.A_REVERSE | curses.A_BOLD)
            else:
                # Merender kotak level dengan style standar (tidak sedang disorot)
                stdscr.addstr(box_y,     box_x, "┌" + "─" * (w_kotak-2) + "┐")
                stdscr.addstr(box_y + 1, box_x, f"│{teks_level}│")
                stdscr.addstr(box_y + 2, box_x, "└" + "─" * (w_kotak-2) + "┘")
        
        # Merender petunjuk instruksi kendali menu di posisi bagian bawah bingkai
        stdscr.addstr(start_y + h_box - 3, start_x + (w_box // 2) - 18, "[ Gunakan Panah ◄/▲/▼/► & ENTER ]")
        stdscr.addstr(start_y + h_box - 2, start_x + (w_box // 2) - 12, "[ Tekan 'Q' untuk Kembali ]")
        stdscr.refresh()
        
        # Menangkap satu aksi ketukan tombol keyboard dari pengguna
        tombol = stdscr.getch()
        
        # --- STRUKTUR LOGIKA NAVIGASI KURSOR (INTERAKTIF) ---
        if tombol == curses.KEY_LEFT:
            if pilihan_aktif % KOLOM_GRID > 0:
                pilihan_aktif -= 1
            else:
                # Fitur Wrap-around: Lompat otomatis menuju elemen kolom paling kanan
                pilihan_aktif = pilihan_aktif + (KOLOM_GRID - 1)
                
        elif tombol == curses.KEY_RIGHT:
            if (pilihan_aktif + 1) % KOLOM_GRID != 0 and pilihan_aktif < TOTAL_LEVEL - 1:
                pilihan_aktif += 1
            else:
                # Fitur Wrap-around: Kembali otomatis menuju elemen kolom paling kiri
                pilihan_aktif = (pilihan_aktif // KOLOM_GRID) * KOLOM_GRID
                
        elif tombol == curses.KEY_UP:
            if pilihan_aktif - KOLOM_GRID >= 0:
                pilihan_aktif -= KOLOM_GRID
            else:
                # Fitur Wrap-around Vertikal: Melompat langsung ke baris di bawahnya
                pilihan_aktif = pilihan_aktif + KOLOM_GRID
                
        elif tombol == curses.KEY_DOWN:
            if pilihan_aktif + KOLOM_GRID < TOTAL_LEVEL:
                pilihan_aktif += KOLOM_GRID
            else:
                # Fitur Wrap-around Vertikal: Melompat langsung ke baris di atasnya
                pilihan_aktif = pilihan_aktif - KOLOM_GRID
                
        elif tombol in (ord('q'), ord('Q')):
            return None # Keluar dari menu level dan kembali menuju menu utama
            
        elif tombol in (10, 13):  # Deteksi penekanan tombol ENTER (ASCII Line Feed / Carriage Return)
            level_pilihan = pilihan_aktif + 1
            if level_pilihan <= max_level_user:
                return level_pilihan # Mengembalikan nilai level yang dipilih untuk diproses gameplay
            else:
                # Blok proteksi jika pengguna mencoba mengakses tingkatan level yang masih terkunci
                stdscr.addstr(start_y + h_box - 4, start_x + (w_box // 2) - 13, "LEVEL MASIH TERKUNCI!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()

def jalankan_pemilihan_level(username, max_level_user):
    """Fungsi pembungkus (wrapper) untuk menginisialisasi modul curses secara aman"""
    return curses.wrapper(menu_pilih_level, username, max_level_user)
