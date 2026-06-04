import curses

def draw_box(stdscr, y, x, h, w, title=""):
    """
    Fungsi utilitas untuk merender bingkai luar (border) persegi panjang.
    Memanfaatkan karakter box-drawing Unicode agar visual terminal rapi.
    """
    # 1. Menggambar sudut kiri atas, garis horizontal atas, dan sudut kanan atas
    stdscr.addstr(y, x, "┌" + "─" * (w-2) + "┐")
    
    # 2. Menggambar sudut kiri bawah, garis horizontal bawah, dan sudut kanan bawah
    stdscr.addstr(y + h - 1, x, "└" + "─" * (w-2) + "┘")
    
    # 3. Perulangan (looping) untuk menggambar garis vertikal di sisi kiri dan kanan bingkai
    for i in range(1, h - 1):
        stdscr.addstr(y + i, x, "│")            # Garis vertikal kiri
        stdscr.addstr(y + i, x + w - 1, "│")    # Garis vertikal kanan
        
    # 4. Pengondisian: Jika parameter title diisi, gambar teks judul tepat di tengah atas kotak
    if title:
        # Rumus mencari titik tengah: Koordinat X awal + (Setengah Lebar Kotak) - (Setengah Panjang Judul)
        stdscr.addstr(y, x + (w // 2) - (len(title) // 2), f" {title} ")

def menu_pilih_level(stdscr, username, max_level_user):
    """
    Sistem navigasi pemilihan level menggunakan konsep struktur data Grid Matriks 2x5.
    Menggunakan library curses untuk menangkap input keyboard secara real-time.
    """
    curses.curs_set(0) # Menyembunyikan kursor pengetikan standar terminal (agar tampilan bersih)
    stdscr.keypad(True) # Mengaktifkan pembacaan tombol khusus (seperti tombol panah keyboard)

    # --- DEKLARASI KONFIGURASI DAN DIMENSI GRID ---
    TOTAL_LEVEL = 10
    KOLOM_GRID = 5  # Menentukan bahwa dalam 1 baris maksimal ada 5 kotak level
    pilihan_aktif = 0  # Variabel pointer/indeks untuk mencatat kotak mana yang sedang dipilih (0 s.d. 9)
    
    # Menentukan dimensi ukuran lebar (w) dan tinggi (h) untuk layout menu
    h_box, w_box = 15, 96        # Ukuran bingkai luar besar
    h_kotak, w_kotak = 3, 14     # Ukuran masing-masing kotak kecil level
    
    # Perulangan utama (Main Loop) untuk menjaga menu tetap berjalan dan responsif
    while True:
        # Membaca ukuran resolusi layar terminal pengguna saat ini (Tinggi = Y, Lebar = X)
        screen_y, screen_x = stdscr.getmaxyx()
        
        # Validasi: Jika layar terminal terlalu kecil, hentikan render dan minta user memperbesar layar
        if screen_y < h_box or screen_x < w_box:
            stdscr.clear()
            stdscr.addstr(0, 0, "Perbesar ukuran terminal VS Code kamu!")
            stdscr.refresh()
            stdscr.getch() # Menunggu user menekan tombol apapun setelah memperbesar layar
            continue       # Melompat kembali ke awal perulangan while
            
        # Kalkulasi koordinat awal (Centering) agar kotak besar pas berada di tengah-tengah layar
        start_y = (screen_y - h_box) // 2
        start_x = (screen_x - w_box) // 2
        
        stdscr.clear() # Membersihkan sisa gambar di layar sebelum menggambar layout baru
        
        # Memanggil fungsi draw_box untuk menggambar bingkai luar utama menu
        draw_box(stdscr, start_y, start_x, h_box, w_box, f"LEVEL SELECT - {username.upper()}")
        
        # --- PROSES PEMETAAN & PENGGAMBARAN GRID MATRIKS ---
        for idx in range(TOTAL_LEVEL):
            nomor_level = idx + 1 # Konversi indeks coding (0-9) ke nomor level nyata (1-10)
            
            # MATEMATIKA KOMPUTER: Mengonversi indeks urutan linear (1D) menjadi posisi Baris & Kolom (2D)
            row = idx // KOLOM_GRID # Contoh: indeks 7 // 5 = Baris ke-1 (Baris kedua dalam komputer)
            col = idx % KOLOM_GRID  # Contoh: indeks 7 % 5 = Kolom ke-2 (Kolom ketiga dalam komputer)
            
            # Menghitung koordinat X dan Y spesifik di layar untuk setiap kotak kecil level
            box_y = start_y + 2 + (row * 4)  # Jarak antar baris dibatasi 4 rentang koordinat Y
            box_x = start_x + 5 + (col * 18) # Jarak antar kolom dibatasi 18 rentang koordinat X
            
            # Cek Hak Akses: Level terbuka HANYA JIKA nomor level tidak melewati batas max_level_user
            terbuka = nomor_level <= max_level_user
            
            if terbuka:
                teks_level = f"  LEVEL {nomor_level:02d}  " # Format :02d membuat angka 1 menjadi "01"
            else:
                teks_level = f"  [LOCKED]  "                 # Tampilan jika level belum di-unlock
            
            # --- PERCABANGAN STYLE VISUAL (HIGHLIGHT) ---
            # Jika kotak yang sedang diproses loop (idx) adalah kotak yang sedang disorot user (pilihan_aktif)
            if idx == pilihan_aktif:
                # Cetak dengan efek warna terbalik (A_REVERSE) dan tulisan tebal (A_BOLD)
                stdscr.addstr(box_y,     box_x, "┌" + "─" * (w_kotak-2) + "┐", curses.A_REVERSE | curses.A_BOLD)
                stdscr.addstr(box_y + 1, box_x, f"│{teks_level}│", curses.A_REVERSE | curses.A_BOLD)
                stdscr.addstr(box_y + 2, box_x, "└" + "─" * (w_kotak-2) + "┘", curses.A_REVERSE | curses.A_BOLD)
            else:
                # Cetak dengan gaya standar (tidak disorot/tidak ada kursor)
                stdscr.addstr(box_y,     box_x, "┌" + "─" * (w_kotak-2) + "┐")
                stdscr.addstr(box_y + 1, box_x, f"│{teks_level}│")
                stdscr.addstr(box_y + 2, box_x, "└" + "─" * (w_kotak-2) + "┘")
        
        # Menampilkan teks panduan kontrol game di bagian bawah dalam bingkai utama
        stdscr.addstr(start_y + h_box - 3, start_x + (w_box // 2) - 18, "[ Gunakan Panah ◄/▲/▼/► & ENTER ]")
        stdscr.addstr(start_y + h_box - 2, start_x + (w_box // 2) - 12, "[ Tekan 'Q' untuk Kembali ]")
        stdscr.refresh() # Render seluruh objek yang sudah diatur di atas ke layar terminal
        
        # Menangkap input satu tombol dari keyboard secara real-time
        tombol = stdscr.getch()
        
        # --- LOGIKA PERCABANGAN INTERAKSI KEYBOARD (NAVIGASI) ---
        if tombol == curses.KEY_LEFT:
            if pilihan_aktif % KOLOM_GRID > 0:
                pilihan_aktif -= 1 # Geser kursor ke kiri 1 kotak
            else:
                # Fitur Wrap-around: Jika sudah di paling kiri baris, lompat ke ujung paling kanan baris tersebut
                pilihan_aktif = pilihan_aktif + (KOLOM_GRID - 1)
                
        elif tombol == curses.KEY_RIGHT:
            # Validasi agar tidak melewati batas kolom kanan ATAU melewati total level (index 9)
            if (pilihan_aktif + 1) % KOLOM_GRID != 0 and pilihan_aktif < TOTAL_LEVEL - 1:
                pilihan_aktif += 1 # Geser kursor ke kanan 1 kotak
            else:
                # Fitur Wrap-around: Jika sudah di paling kanan baris, kembali ke ujung paling kiri baris tersebut
                pilihan_aktif = (pilihan_aktif // KOLOM_GRID) * KOLOM_GRID
                
        elif tombol == curses.KEY_UP:
            if pilihan_aktif - KOLOM_GRID >= 0:
                pilihan_aktif -= KOLOM_GRID # Melompat ke kotak tepat di baris atasnya (-5 indeks)
            else:
                # Fitur Wrap-around Vertikal: Jika di baris atas, menekan panah atas akan tembus ke baris bawahnya
                pilihan_aktif = pilihan_aktif + KOLOM_GRID
                
        elif tombol == curses.KEY_DOWN:
            if pilihan_aktif + KOLOM_GRID < TOTAL_LEVEL:
                pilihan_aktif += KOLOM_GRID # Melompat ke kotak tepat di baris bawahnya (+5 indeks)
            else:
                # Fitur Wrap-around Vertikal: Jika di baris bawah, menekan panah bawah akan tembus ke baris atasnya
                pilihan_aktif = pilihan_aktif - KOLOM_GRID
                
        elif tombol in (ord('q'), ord('Q')):
            return None # Mengembalikan nilai kosong/None (Sinyal untuk kembali ke menu utama)
            
        elif tombol in (10, 13):  # 10 = Enter di Linux/macOS, 13 = Enter di Windows (ASCII)
            level_pilihan = pilihan_aktif + 1 # Konversi index kursor menjadi nomor level asli
            
            # Validasi Proteksi: Cek apakah level pilihan user statusnya sudah terbuka atau belum
            if level_pilihan <= max_level_user:
                return level_pilihan # Valid, kembalikan nomor level untuk dimainkan di file gameplay
            else:
                # Blok proteksi: Tampilkan teks peringatan jika mencoba masuk ke level yang terkunci
                stdscr.addstr(start_y + h_box - 4, start_x + (w_box // 2) - 13, "LEVEL MASIH TERKUNCI!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch() # Menahan layar sampai user menekan tombol apa saja untuk mereset pesan

def jalankan_pemilihan_level(username, max_level_user):
    """
    Fungsi pembungkus (wrapper) untuk menginisialisasi modul curses secara aman.
    Menghindari terminal VS Code menjadi rusak/error berantakan jika program terhenti mendadak.
    """
    return curses.wrapper(menu_pilih_level, username, max_level_user)
