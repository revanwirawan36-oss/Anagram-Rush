# gameplay2.py
import curses
import time
import textwrap
from database import kata_pilihan
from config import CONFIG_LEVEL
from menang_kalah import tampilkan_menu_akhir


#untuk mengurutkan array karakter secara manual menggunakan bubble sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

#untuk mengecek anagram
def cek_anagram_sorting(kata1, kata2):
    k1 = kata1.lower()
    k2 = kata2.lower()
    if len(k1) != len(k2):
        return False
    sorted1 = bubble_sort(list(k1))
    sorted2 = bubble_sort(list(k2))
    for i in range(len(sorted1)):
        if sorted1[i] != sorted2[i]:
            return False
    return True

#menggambar box
def draw_box(stdscr, y, x, height, width, attr=0):
    try:
        stdscr.addstr(y, x, "┌" + "─" * (width - 2) + "┐", attr)
        for i in range(1, height - 1):
            stdscr.addstr(y + i, x, "│", attr)
            stdscr.addstr(y + i, x + width - 1, "│", attr)
        stdscr.addstr(y + height - 1, x, "└" + "─" * (width - 2) + "┘", attr)
    except curses.error:
        pass

def render_pemeriksaan_box(stdscr, y, x, box_h, box_w, kata_dasar, kata_user):
    draw_box(stdscr, y, x, box_h, box_w)
    inner_w = max(1, box_w - 4)

    if not kata_user:
        try:
            stdscr.addstr(y + 1, x + 2, f"[{kata_dasar}]"[:inner_w], curses.A_DIM)
            stdscr.addstr(y + 2, x + 2, "menunggu input..."[:inner_w], curses.A_DIM)
        except curses.error:
            pass
        return

    k1 = kata_dasar.lower()
    k2 = kata_user.lower()
    sort1 = bubble_sort(list(k1))
    sort2 = bubble_sort(list(k2))

    def fmt(s):
        return "['" + "','".join(s) + "']"

    is_anagram = cek_anagram_sorting(k1, k2)
    is_valid = is_anagram and (k2 in kata_pilihan) and (k1 != k2)

    lines = [
        (f"memeriksa {kata_dasar} vs {kata_user}", curses.A_DIM),
        (f"terurut 1={fmt(sort1)}", curses.A_DIM),
        (f"terurut 2={fmt(sort2)}", curses.A_DIM),
        ("ANAGRAM" if is_anagram else "tdk anagram", curses.A_BOLD if is_anagram else curses.A_DIM),
        (f"{kata_user} valid" if is_valid else (f"{kata_user} tdk valid" if is_anagram else ""), curses.A_BOLD),
    ]

    for i, (line, attr) in enumerate(lines):
        row = y + 1 + i
        if row >= y + box_h - 1 or not line:
            continue
        try:
            stdscr.addstr(row, x + 2, line[:inner_w], attr)
        except curses.error:
            pass

#gameplay untuk level 6-10 dengan 2 anagram per kata dasar
def main_gameplay(stdscr, username, level):
    if level not in CONFIG_LEVEL:
        return False

    cfg = CONFIG_LEVEL[level]
    timer_awal = cfg["timer"]
    daftar_kata = [k.lower() for k in cfg["kata_dasar"]]

    #simpan jawaban user dalam bentuk dictionary dengan key = kata dasar, value = list jawaban anagram yang sudah diisi (maksimal 2)
    jawaban_user = {kata: [] for kata in daftar_kata}

    log_notifikasi = [
        "Waktu berjalan secara real-time...",
        "Masukkan MINIMAL 2 anagram valid untuk setiap kata dasar!",
        f"Selamat datang di Anagram Rush Hard Mode - Level {level}!",
    ]

    def tambah_notifikasi(teks):
        log_notifikasi.insert(0, teks)
        if len(log_notifikasi) > 10:
            log_notifikasi.pop()

    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)

    waktu_mulai = time.time()
    input_buffer = ""

    while True:
        waktu_tersisa = int(timer_awal - (time.time() - waktu_mulai))

        #gagal
        if waktu_tersisa <= 0:
            return tampilkan_menu_akhir(stdscr, False, username)

        #menang
        if all(len(jawaban_user[k]) == 2 for k in daftar_kata):
            return tampilkan_menu_akhir(stdscr, True, username)

        """
        ════════════════════════════════════════
        R E N D E R   U I   ( L A Y O U T   N E W )
        ════════════════════════════════════════
        """
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()

        MARGIN_X = 4
        HEADER_H = 3

        #ukuran box
        available_h = sh - HEADER_H - 4
        BOX_H = max(3, int(available_h * 0.13))
        BOX_GAP_X = 3
        N = len(daftar_kata)

        available_w = sw - (2 * MARGIN_X)
        BOX_W = max(12, (available_w - (N - 1) * BOX_GAP_X) // N)
        total_grid_w = N * BOX_W + (N - 1) * BOX_GAP_X
        grid_x = (sw - total_grid_w) // 2

        #header dengan title dan timer
        title = f"ANAGRAM RUSH HARD - LEVEL {level} [2 ANAGRAM PER KATA]"
        timer_str = f"TIME: {max(0, waktu_tersisa) // 60:02d}:{max(0, waktu_tersisa) % 60:02d}"
        try:
            stdscr.addstr(1, grid_x, title, curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.addstr(1, grid_x + total_grid_w - len(timer_str), timer_str, curses.A_BOLD | curses.A_REVERSE)
        except curses.error:
            pass

        #box 1: Kotak Kata Dasar
        ROW1_Y = HEADER_H + 1
        for i, kata in enumerate(daftar_kata):
            bx = grid_x + i * (BOX_W + BOX_GAP_X)
            draw_box(stdscr, ROW1_Y, bx, BOX_H, BOX_W)
            # Taruh kata dasar di tengah
            pad_x = max(0, (BOX_W - 2 - len(kata)) // 2)
            pad_y = max(0, (BOX_H - 2) // 2)
            try:
                stdscr.addstr(ROW1_Y + 1 + pad_y, bx + 1 + pad_x, kata.upper(), curses.A_BOLD)
            except curses.error:
                pass

        #box 2: Kotak Jawaban User (2 slot per kata dasar, bertingkat vertikal)
        #tambahkan variabel untuk mengatur jarak vertikal antar slot jawaban
        ROW2_H = BOX_H + 2 
        ROW2_Y = ROW1_Y + BOX_H + 1
        for i, kata in enumerate(daftar_kata):
            bx = grid_x + i * (BOX_W + BOX_GAP_X)
            list_jawab = jawaban_user[kata]
            
            draw_box(stdscr, ROW2_Y, bx, ROW2_H, BOX_W, curses.A_BOLD if list_jawab else curses.A_DIM)
            
            #slot ke-1
            ans1 = list_jawab[0].upper() if len(list_jawab) >= 1 else "◦ ◦ ◦ ◦"
            attr1 = curses.A_BOLD | curses.A_REVERSE if len(list_jawab) >= 1 else curses.A_DIM
            pad_x1 = max(0, (BOX_W - 2 - len(ans1)) // 2)
            try:
                stdscr.addstr(ROW2_Y + 1, bx + 1 + pad_x1, ans1, attr1)
            except curses.error:
                pass

            #slot ke-2
            ans2 = list_jawab[1].upper() if len(list_jawab) == 2 else "◦ ◦ ◦ ◦"
            attr2 = curses.A_BOLD | curses.A_REVERSE if len(list_jawab) == 2 else curses.A_DIM
            pad_x2 = max(0, (BOX_W - 2 - len(ans2)) // 2)
            try:
                stdscr.addstr(ROW2_Y + 2, bx + 1 + pad_x2, ans2, attr2)
            except curses.error:
                pass

        #box 3
        PEMERIKSA_Y = ROW2_Y + ROW2_H + 1
        PEMERIKSA_H = 7
        for i, kata in enumerate(daftar_kata):
            bx = grid_x + i * (BOX_W + BOX_GAP_X)
            render_pemeriksaan_box(stdscr, PEMERIKSA_Y, bx, PEMERIKSA_H, BOX_W, kata, input_buffer)

        #box 4
        BOTTOM_Y = PEMERIKSA_Y + PEMERIKSA_H + 1
        BOTTOM_H = max(5, sh - BOTTOM_Y - 1)
        INPUT_BOX_W = max(25, int(total_grid_w * 0.40))

        #kotak input
        draw_box(stdscr, BOTTOM_Y, grid_x, BOTTOM_H, INPUT_BOX_W)
        try:
            stdscr.addstr(BOTTOM_Y + 1, grid_x + 3, "KOLOM INPUT:", curses.A_DIM | curses.A_UNDERLINE)
            input_y = BOTTOM_Y + (BOTTOM_H // 2)
            isi_input = ">> " + input_buffer
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
        elif ch in (10, 13): #enter
            kata_tebakan = input_buffer.strip().lower()
            input_buffer = ""

            if not kata_tebakan:
                continue

            cocok = None
            for kd in daftar_kata:
                if cek_anagram_sorting(kd, kata_tebakan):
                    cocok = kd
                    break

            if cocok is None:
                tambah_notifikasi(f"Kata '{kata_tebakan.upper()}' bukan anagram dari kata mana pun!")
                continue

            if kata_tebakan not in kata_pilihan:
                tambah_notifikasi(f"Kata '{kata_tebakan.upper()}' merupakan anagram dari '{cocok.upper()}', tetapi tidak valid/tidak ada di KBBI!")
                continue

            if kata_tebakan == cocok:
                tambah_notifikasi(f"Gagal! '{kata_tebakan.upper()}' sama persis dengan kata dasar.")
                continue

            #validasi 1: cek apakah kata tebakan sudah ada di list jawaban user untuk kata dasar yang cocok
            if kata_tebakan in jawaban_user[cocok]:
                tambah_notifikasi(f"Sudah diisi! '{kata_tebakan.upper()}' sudah ada di kolom tersebut.")
                continue

            #validasi 2: cek apakah kolom jawaban untuk kata dasar yang cocok sudah penuh dengan 2 anagram valid
            if len(jawaban_user[cocok]) >= 2:
                tambah_notifikasi(f"Kolom '{cocok.upper()}' sudah penuh dengan 2 anagram valid!")
                continue

            #sukses
            jawaban_user[cocok].append(kata_tebakan)
            tambah_notifikasi(f"BERHASIL! ({len(jawaban_user[cocok])}/2) '{kata_tebakan.upper()}' sah untuk anagram '{cocok.upper()}'!")
            waktu_mulai = time.time()
            timer_awal = cfg["timer"]

        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            input_buffer = input_buffer[:-1]
        elif ch in (ord('q'), ord('Q')):
            stdscr.nodelay(False)
            return None
        elif 32 <= ch <= 126:
            if len(input_buffer) < 20:
                input_buffer += chr(ch)

def jalankan_gameplay_level(username, level):
    return curses.wrapper(main_gameplay, username, level)