import curses
import time
import textwrap
from database import kata_pilihan 
from config import CONFIG_LEVEL
from menang_kalah import tampilkan_menu_akhir


def bubble_sort(arr):
    """Mengurutkan array karakter secara manual dengan algoritma Bubble Sort"""
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def cek_anagram_sorting(kata1, kata2):
    """Mengecek anagram menggunakan metode manual Bubble Sort"""
    k1 = kata1.lower()
    k2 = kata2.lower()
    
    if len(k1) != len(k2):
        return False

    sorted1 = bubble_sort(list(k1))
    sorted2 = bubble_sort(list(k2))

    anagram = True
    for i in range(len(sorted1)):
        if sorted1[i] != sorted2[i]:
            anagram = False
            break
            
    return anagram

#gambar kotak dengan border menggunakan karakter boxdrawing Unicode
def draw_box(stdscr, y, x, height, width, attr=0):
    """Menggambar kotak bertepi menggunakan karakter box-drawing Unicode"""
    try:
        stdscr.addstr(y, x, "┌" + "─" * (width - 2) + "┐", attr)
        for i in range(1, height - 1):
            stdscr.addstr(y + i, x,             "│", attr)
            stdscr.addstr(y + i, x + width - 1, "│", attr)
        stdscr.addstr(y + height - 1, x, "└" + "─" * (width - 2) + "┘", attr)
    except curses.error:
        pass


def tulis_tengah_kotak(stdscr, y, x, box_width, box_height, text, attr=0):
    """Menulis teks tepat di tengah-tengah kotak baik secara horizontal maupun vertikal"""
    inner_w = box_width - 2
    inner_h = box_height - 2

    pad_x = max(0, (inner_w - len(text)) // 2)
    pad_y = max(0, inner_h // 2)

    try:
        stdscr.addstr(y + 1 + pad_y, x + 1 + pad_x, text[:inner_w], attr)
    except curses.error:
        pass

#anagram rea time
def render_pemeriksaan_box(stdscr, y, x, box_h, box_w, kata_dasar, kata_user):
    """
    Menampilkan proses pengecekan anagram secara real-time di dalam kotak pemeriksaan.
    Menggunakan metode Bubble Sort untuk visualisasi terurut per huruf.
    Sekarang validasi status 'valid' juga mengecek keberadaan kata di database kata_pilihan.
    """
    draw_box(stdscr, y, x, box_h, box_w)
    inner_w = max(1, box_w - 4)

    #seblm input
    if not kata_user:
        try:
            stdscr.addstr(y + 1, x + 2, f"[{kata_dasar}]"[:inner_w],  curses.A_DIM)
            stdscr.addstr(y + 2, x + 2, "menunggu input..."[:inner_w], curses.A_DIM)
        except curses.error:
            pass
        return

    k1 = kata_dasar.lower()
    k2 = kata_user.lower()
    
    #visual pk buuble sort
    sort1 = bubble_sort(list(k1))
    sort2 = bubble_sort(list(k2))

    #biar kaya yang di modul
    def fmt(s):
        return "['" + "','".join(s) + "']"

    #penentuan hasil akhir menggunakan fungsi berbasis Bubble Sort
    is_anagram = cek_anagram_sorting(k1, k2)
    
    #VALIDASI JUGA MENGECEK DATABASE (kata_pilihan) DAN BUKAN KATA DASAR ITU SENDIRI
    is_valid   = is_anagram and (k2 in kata_pilihan) and (k1 != k2)

    lines = [
        (f"memeriksa {kata_dasar} vs {kata_user}", curses.A_DIM),
        (f"terurut 1={fmt(sort1)}",                curses.A_DIM),
        (f"terurut 2={fmt(sort2)}",                curses.A_DIM),
        ("ANAGRAM"      if is_anagram else "TDK ANAGRAM",
        curses.A_BOLD  if is_anagram else curses.A_DIM),
        (f"{kata_user} valid" if is_valid else (f"{kata_user} TDK VALID" if is_anagram else ""), curses.A_BOLD),
    ]

    for i, (line, attr) in enumerate(lines):
        row = y + 1 + i
        if row >= y + box_h - 1 or not line:
            continue
        try:
            stdscr.addstr(row, x + 2, line[:inner_w], attr)
        except curses.error:
            pass


#gameplay utama untuk level 1-5
def main_gameplay(stdscr, username, level):
    if level not in CONFIG_LEVEL:
        return False

    cfg         = CONFIG_LEVEL[level]
    timer_awal  = cfg["timer"]
    daftar_kata = [k.lower() for k in cfg["kata_dasar"]]

    jawaban_user = {kata: None for kata in daftar_kata}

    log_notifikasi = [
        "Waktu berjalan secara real-time...",
        "Masukkan 1 anagram valid untuk setiap kata dasar.",
        "Selamat datang di Anagram Rush!",
    ]
    #buat tambah notif
    def tambah_notifikasi(teks):
        log_notifikasi.insert(0, teks)
        if len(log_notifikasi) > 10:
            log_notifikasi.pop()

    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)

    waktu_mulai  = time.time()
    input_buffer = ""

    while True:
        waktu_tersisa = int(timer_awal - (time.time() - waktu_mulai))

        #klo gagal
        if waktu_tersisa <= 0:
            return tampilkan_menu_akhir(stdscr, False, username)

        #klo menang
        if all(jawaban_user[k] is not None for k in daftar_kata):
            return tampilkan_menu_akhir(stdscr, True, username)

        """
        ════════════════════════════════════════
         R E N D E R   U I   ( F U L L S C R E E N )
        ════════════════════════════════════════
        """

        stdscr.clear()
        sh, sw = stdscr.getmaxyx()

        #1. PENGATURAN SKALA DINAMIS UTAMA
        MARGIN_X    = 4
        HEADER_H    = 3

        available_h = sh - HEADER_H - 4
        BOX_H       = max(3, int(available_h * 0.15)) 
        BOX_GAP_X   = 3
        N           = len(daftar_kata)

        available_w  = sw - (2 * MARGIN_X)
        BOX_W        = max(12, (available_w - (N - 1) * BOX_GAP_X) // N)
        total_grid_w = N * BOX_W + (N - 1) * BOX_GAP_X
        grid_x       = (sw - total_grid_w) // 2

        #header dengan judul level dan timer
        title     = f"ANAGRAM RUSH - LEVEL {level}"
        mnt       = max(0, waktu_tersisa) // 60
        dtk       = max(0, waktu_tersisa) % 60
        timer_str = f"TIME: {mnt:02d}:{dtk:02d}"

        try:
            stdscr.addstr(1, grid_x, title, curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.addstr(1, grid_x + total_grid_w - len(timer_str), timer_str, curses.A_BOLD | curses.A_REVERSE)
        except curses.error:
            pass

        #box 1: Kotak Kata Dasar (Static, Tidak Berubah)
        ROW1_Y = HEADER_H + 1
        for i, kata in enumerate(daftar_kata):
            bx = grid_x + i * (BOX_W + BOX_GAP_X)
            draw_box(stdscr, ROW1_Y, bx, BOX_H, BOX_W)
            tulis_tengah_kotak(stdscr, ROW1_Y, bx, BOX_W, BOX_H, kata.upper(), curses.A_BOLD)

        # box 2: Kotak Jawaban User (Dinamis, Terisi Berdasarkan Input User)
        ROW2_Y = ROW1_Y + BOX_H + 1
        for i, kata in enumerate(daftar_kata):
            bx      = grid_x + i * (BOX_W + BOX_GAP_X)
            jawaban = jawaban_user[kata]
            if jawaban is not None:
                draw_box(stdscr, ROW2_Y, bx, BOX_H, BOX_W, curses.A_BOLD)
                tulis_tengah_kotak(stdscr, ROW2_Y, bx, BOX_W, BOX_H, jawaban.upper(), curses.A_BOLD | curses.A_REVERSE)
            else:
                draw_box(stdscr, ROW2_Y, bx, BOX_H, BOX_W, curses.A_DIM)
                tulis_tengah_kotak(stdscr, ROW2_Y, bx, BOX_W, BOX_H, "◦ ◦ ◦ ◦", curses.A_DIM)

        #box 3: Kotak Pemeriksaan Anagram Real-Time (Dinamis, Menampilkan Proses Validasi Anagram)
        PEMERIKSA_Y = ROW2_Y + BOX_H + 1
        PEMERIKSA_H = 7 

        for i, kata in enumerate(daftar_kata):
            bx = grid_x + i * (BOX_W + BOX_GAP_X)
            render_pemeriksaan_box(
                stdscr, PEMERIKSA_Y, bx, PEMERIKSA_H, BOX_W,
                kata, input_buffer
            )

        #box 4: Kotak Input User + Log Notifikasi (Dinamis, Terisi Berdasarkan Interaksi User dan Status Validasi)
        BOTTOM_Y = PEMERIKSA_Y + PEMERIKSA_H + 2
        BOTTOM_H = max(5, sh - BOTTOM_Y - 2)

        INPUT_BOX_W = max(25, int(total_grid_w * 0.40))

        #kotak input
        draw_box(stdscr, BOTTOM_Y, grid_x, BOTTOM_H, INPUT_BOX_W)
        try:
            stdscr.addstr(BOTTOM_Y + 1, grid_x + 3, "KOLOM INPUT:", curses.A_DIM | curses.A_UNDERLINE)

            input_y   = BOTTOM_Y + (BOTTOM_H // 2)
            label     = ">> "
            isi_input = label + input_buffer
            stdscr.addstr(input_y, grid_x + 4, isi_input, curses.A_BOLD)

            cursor_col = grid_x + 4 + len(isi_input)
            if cursor_col < grid_x + INPUT_BOX_W - 2:
                curses.curs_set(1)
                stdscr.move(input_y, cursor_col)
        except curses.error:
            pass

        #kotak log aktivitas
        KETER_X = grid_x + INPUT_BOX_W + 2
        KETER_W = (grid_x + total_grid_w) - KETER_X
        INNER_W = max(1, KETER_W - 6)

        draw_box(stdscr, BOTTOM_Y, KETER_X, BOTTOM_H, KETER_W)
        try:
            stdscr.addstr(BOTTOM_Y + 1, KETER_X + 3, "LOG AKTIVITAS:", curses.A_DIM | curses.A_UNDERLINE)
        except curses.error:
            pass

        wrapped_lines = []
        for notif in log_notifikasi:
            baris_wrap = textwrap.wrap(notif, width=INNER_W) or [notif[:INNER_W]]
            wrapped_lines.extend(baris_wrap)

        for idx, line in enumerate(wrapped_lines):
            row = BOTTOM_Y + 2 + idx
            if row < BOTTOM_Y + BOTTOM_H - 1:
                try:
                    attr_log = curses.A_BOLD if idx == 0 else curses.A_DIM
                    stdscr.addstr(row, KETER_X + 3, "• " + line, attr_log)
                except curses.error:
                    pass

        stdscr.refresh()
        """
        ════════════════════════════════════════
        I N P U T   P O L L I N G
        ════════════════════════════════════════
        """
        time.sleep(0.05)
        ch = stdscr.getch()

        if ch == -1:
            continue

        elif ch in (10, 13):   # ── ENTER ──
            kata_tebakan = input_buffer.strip().lower()
            input_buffer = ""

            if not kata_tebakan:
                continue

            #1. cari kata dasar yang cocok secara struktural (Menggunakan Bubble Sort manual)
            cocok = None
            for kd in daftar_kata:
                if cek_anagram_sorting(kd, kata_tebakan):
                    cocok = kd
                    break

            #case 1: Tidak ada struktur anagram yang cocok dengan kata dasar manapun
            if cocok is None:
                tambah_notifikasi(f"Kata '{kata_tebakan.upper()}' bukan anagram dari kata mana pun!")
                continue

            
            #case 2: Struktur anagram cocok, tapi kata tebakan tidak valid (tidak ada di database kata_pilihan)
            if kata_tebakan not in kata_pilihan:
                tambah_notifikasi(f"Kata '{kata_tebakan.upper()}' merupakan anagram dari '{cocok.upper()}', tetapi tidak valid/tidak ada di KBBI!")
                continue

            #case 3: Struktur anagram cocok, valid di database, tapi sama persis dengan kata dasar
            if kata_tebakan == cocok:
                tambah_notifikasi(f"Gagal! '{kata_tebakan.upper()}' sama persis dengan kata dasar.")
                continue

            #case 4: Struktur anagram cocok, valid di database, tapi sudah terisi di kolom yang sama
            if jawaban_user[cocok] == kata_tebakan:
                tambah_notifikasi(f"Sudah diisi! '{kata_tebakan.upper()}' sudah ada di kolom tersebut.")
                continue

            #case 5: Struktur anagram cocok, valid di database, tapi sudah terisi dengan anagram lain di kolom yang sama
            if jawaban_user[cocok] is not None:
                tambah_notifikasi(f"Kolom '{cocok.upper()}' sudah terisi dengan anagram lain!")
                continue

            #sukses validasi semua, update jawaban user di kolom yang sesuai
            jawaban_user[cocok] = kata_tebakan
            tambah_notifikasi(f"BERHASIL! '{kata_tebakan.upper()}' sah untuk anagram '{cocok.upper()}'!")
            waktu_mulai = time.time()
            timer_awal  = cfg["timer"]

        elif ch in (curses.KEY_BACKSPACE, 127, 8):   #backspace
            input_buffer = input_buffer[:-1]

        elif ch in (ord('q'), ord('Q')):              # q untuk quit
            stdscr.nodelay(False)
            return None

        elif 32 <= ch <= 126:                         #karakter valid 
            if len(input_buffer) < 20:
                input_buffer += chr(ch)


def jalankan_gameplay_level(username, level):
    return curses.wrapper(main_gameplay, username, level)