# level.py
import curses

def draw_box(stdscr, y, x, h, w, title=""):
    """Fungsi pembantu membuat kotak besar visual luar"""
    stdscr.addstr(y, x, "┌" + "─" * (w-2) + "┐")
    stdscr.addstr(y + h - 1, x, "└" + "─" * (w-2) + "┘")
    for i in range(1, h - 1):
        stdscr.addstr(y + i, x, "│")
        stdscr.addstr(y + i, x + w - 1, "│")
    if title:
        stdscr.addstr(y, x + (w // 2) - (len(title) // 2), f" {title} ")

def menu_pilih_level(stdscr, username, max_level_user):
    """Sistem Pilih Level Grid Matriks 5x5 dengan Skala Jauh Lebih Besar dan Lebar"""
    curses.curs_set(0)
    stdscr.keypad(True)
    
    TOTAL_LEVEL = 25
    KOLOM_GRID = 5  # Matriks 5 baris x 5 kolom = 25 level pas
    pilihan_aktif = 0  # Indeks level aktif (0 sampai 24)
    
    # REVISI SKALA: Kotak utama dibuat jauh lebih raksasa dan melebar
    h_box, w_box = 24, 96
    
    # REVISI KOTAK KECIL: Dibuat lebih besar (Lebar 14, Tinggi 3) agar gagah
    h_kotak, w_kotak = 3, 14
    
    while True:
        screen_y, screen_x = stdscr.getmaxyx()
        
        # Validasi jika terminal kekecilan agar tidak crash
        if screen_y < h_box or screen_x < w_box:
            stdscr.clear()
            stdscr.addstr(0, 0, "Perbesar ukuran terminal VS Code kamu!")
            stdscr.refresh()
            stdscr.getch()
            continue
            
        start_y = (screen_y - h_box) // 2
        start_x = (screen_x - w_box) // 2
        
        stdscr.clear()
        draw_box(stdscr, start_y, start_x, h_box, w_box, f"LEVEL SELECT - {username.upper()}")
        
        # Menggambar ke-25 kotak level
        for idx in range(TOTAL_LEVEL):
            nomor_level = idx + 1
            
            row = idx // KOLOM_GRID
            col = idx % KOLOM_GRID
            
            # REVISI KOORDINAT: Jarak antar kotak dilebarkan secara proporsional
            # Vertikal melompat per 4 baris, Horizontal melompat per 18 kolom
            box_y = start_y + 2 + (row * 4)
            box_x = start_x + 5 + (col * 18)
            
            terbuka = nomor_level <= max_level_user
            
            # REVISI SIMBOL: Mengganti emoji gembok yang error dengan teks ASCII aman
            if terbuka:
                teks_level = f"  LEVEL {nomor_level:02d}  "
            else:
                teks_level = f"  [LOCKED]  "
            
            # Render Kotak Kecil Level
            if idx == pilihan_aktif:
                # Efek Highlight penuh saat dipilih menggunakan REVERSE warna
                stdscr.addstr(box_y,     box_x, "┌" + "─" * (w_kotak-2) + "┐", curses.A_REVERSE | curses.A_BOLD)
                stdscr.addstr(box_y + 1, box_x, f"│{teks_level}│", curses.A_REVERSE | curses.A_BOLD)
                stdscr.addstr(box_y + 2, box_x, "└" + "─" * (w_kotak-2) + "┘", curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(box_y,     box_x, "┌" + "─" * (w_kotak-2) + "┐")
                stdscr.addstr(box_y + 1, box_x, f"│{teks_level}│")
                stdscr.addstr(box_y + 2, box_x, "└" + "─" * (w_kotak-2) + "┘")
        
        # Informasi menu di bagian paling bawah dalam kotak besar
        stdscr.addstr(start_y + h_box - 3, start_x + (w_box // 2) - 18, "[ Gunakan Panah ◄/▲/▼/► & ENTER ]")
        stdscr.addstr(start_y + h_box - 2, start_x + (w_box // 2) - 12, "[ Tekan 'Q' untuk Kembali ]")
        stdscr.refresh()
        
        tombol = stdscr.getch()
        
        # Logika pergerakan panah 4 arah pada matriks 5x5
        if tombol == curses.KEY_LEFT:
            if pilihan_aktif % KOLOM_GRID > 0:
                pilihan_aktif -= 1
            else:
                pilihan_aktif = pilihan_aktif + (KOLOM_GRID - 1)
                
        elif tombol == curses.KEY_RIGHT:
            if (pilihan_aktif + 1) % KOLOM_GRID != 0 and pilihan_aktif < TOTAL_LEVEL - 1:
                pilihan_aktif += 1
            else:
                pilihan_aktif = (pilihan_aktif // KOLOM_GRID) * KOLOM_GRID
                
        elif tombol == curses.KEY_UP:
            if pilihan_aktif - KOLOM_GRID >= 0:
                pilihan_aktif -= KOLOM_GRID
            else:
                pilihan_aktif = pilihan_aktif + (KOLOM_GRID * 4)
                
        elif tombol == curses.KEY_DOWN:
            if pilihan_aktif + KOLOM_GRID < TOTAL_LEVEL:
                pilihan_aktif += KOLOM_GRID
            else:
                pilihan_aktif = pilihan_aktif % KOLOM_GRID
                
        elif tombol in (ord('q'), ord('Q')):
            return None
            
        elif tombol in (10, 13):  # Tekan ENTER
            level_pilihan = pilihan_aktif + 1
            if level_pilihan <= max_level_user:
                return level_pilihan
            else:
                stdscr.addstr(start_y + h_box - 4, start_x + (w_box // 2) - 13, "LEVEL MASIH TERKUNCI!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()

def jalankan_pemilihan_level(username, max_level_user):
    return curses.wrapper(menu_pilih_level, username, max_level_user)