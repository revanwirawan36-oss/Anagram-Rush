# menang_kalah.py
import curses

def tampilkan_menu_akhir(stdscr, status, username):
    """
    Menampilkan menu akhir (Menang/Kalah) dengan navigasi tombol panah + Enter.
    status: True (jika menang), False (jika kalah)
    """
    stdscr.nodelay(False)
    stdscr.keypad(True)
    curses.curs_set(0)
    
    #tentukan judul, pesan, dan opsi berdasarkan status menang/kalah
    if status:
        judul = "=== LEVEL CLEAR! ==="
        pesan = f"Luar biasa {username}! Semua kata terpecahkan."
        opsi = ["Kembali ke Menu Level", "Quit Game"]
        # Mapping index pilihan ke nilai return yang akan dikirim balik ke game utama
        mapping_hasil = {0: True, 1: "quit"}
    else:
        judul = "=== TIME UP! LEVEL GAGAL ==="
        pesan = "Waktu habis! Silakan pilih aksi:"
        opsi = ["Restart Level", "Kembali ke Menu Level", "Quit Game"]
        mapping_hasil = {0: "restart", 1: "menu", 2: "quit"}

    pilihan_aktif = 0

    # --- LOOPING UTAMA MENU (RENDER & INPUT) ---
    while True:
        stdscr.clear()
        sh, sw = stdscr.getmaxyx()

        #print judul dan pesan di tengah layar dengan atribut khusus
        attr_judul = curses.A_BOLD | curses.A_REVERSE
        stdscr.addstr(sh // 2 - 4, (sw - len(judul)) // 2, judul, attr_judul)
        stdscr.addstr(sh // 2 - 2, (sw - len(pesan)) // 2, pesan, curses.A_BOLD)

        #print opsi menu dengan navigasi panah, sorot opsi yang aktif
        for idx, item in enumerate(opsi):
            if idx == pilihan_aktif:
                teks_opsi = f" > {item} < "
                attr_opsi = curses.A_BOLD | curses.A_REVERSE
            else:
                teks_opsi = f"   {item}   "
                attr_opsi = curses.A_NORMAL

            row = (sh // 2) + idx
            stdscr.addstr(row, (sw - len(teks_opsi)) // 2, teks_opsi, attr_opsi)

        stdscr.refresh()

        #input navigasi
        ch = stdscr.getch()
        if ch == curses.KEY_UP:
            pilihan_aktif = (pilihan_aktif - 1) % len(opsi)
        elif ch == curses.KEY_DOWN:
            pilihan_aktif = (pilihan_aktif + 1) % len(opsi)
        elif ch in (10, 13):  # Tombol ENTER
            return mapping_hasil[pilihan_aktif]
