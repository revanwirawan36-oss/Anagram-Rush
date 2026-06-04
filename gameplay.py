import curses
import time
import textwrap
from database import kata_pilihan 
from config import CONFIG_LEVEL
from menang_kalah import tampilkan_menu_akhir


def bubble_sort(arr):
    """Mengurutkan array/list karakter secara manual dengan algoritma Bubble Sort"""
    n = len(arr)
    # Loop luar untuk mengontrol jumlah iterasi penjelajahan array
    for i in range(n - 1):
        # Loop dalam untuk membandingkan elemen yang bersebelahan
        for j in range(n - i - 1):
            # Jika elemen kiri lebih besar dari elemen kanan, tukar posisinya (Ascending)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def cek_anagram_sorting(kata1, kata2):
    """Mengecek apakah dua kata merupakan anagram menggunakan metode manual Bubble Sort"""
    k1 = kata1.lower()
    k2 = kata2.lower()
    
    # Jika panjang kedua kata berbeda, sudah pasti bukan anagram
    if len(k1) != len(k2):
        return False

    # Mengubah string menjadi list karakter lalu diurutkan dengan fungsi bubble_sort di atas
    sorted1 = bubble_sort(list(k1))
    sorted2 = bubble_sort(list(k2))

    # Membandingkan isi list karakter yang sudah terurut satu per satu
    anagram = True
    for i in range(len(sorted1)):
        if sorted1[i] != sorted2[i]:
            anagram = False # Jika ada satu huruf saja yang tidak cocok
            break
            
    return anagram


def draw_box(stdscr, y, x, height, width, attr=0):
    """Menggambar kotak bertepi visual menggunakan karakter box-drawing Unicode"""
    try:
        # Menggambar garis sudut dan horizontal atas
        stdscr.addstr(y, x, "┌" + "─" * (width - 2) + "┐", attr)
        # Menggambar garis vertikal kiri dan kanan
        for i in range(1, height - 1):
            stdscr.addstr(y + i, x, "│", attr)
            stdscr.addstr(y + i, x + width - 1, "│", attr)
        # Menggambar garis sudut dan horizontal bawah
        stdscr.addstr(y + height - 1, x, "└" + "─" * (width - 2) + "┘", attr)
    except curses.error:
        pass


def menu_gameplay(stdscr, username, level):
    """Fungsi utama pengatur jalannya permainan, tampilan, dan hitung mundur waktu"""
    cfg = CONFIG_LEVEL[level] # Mengambil konfigurasi kata dan timer berdasarkan level yang dipilih
    list_kata_dasar = cfg["kata_dasar"] # List kata dasar yang harus ditebak anagramnya
    
    # Membuat dictionary untuk menyimpan jawaban user (kosong/None di awal)
    jawaban_user = {kata: None for kata in list_kata_dasar}
    
    # List penampung pesan log notifikasi di bagian bawah layar game
    notifikasi_log = []

    def tambah_notifikasi(pesan):
        """Memasukkan pesan baru ke log notifikasi dan membatasi maksimal 3 baris tampilan"""
        notifikasi_log.append(pesan)
        if len(notifikasi_log) > 3:
            notifikasi_log.pop(0) # Menghapus pesan paling lama jika sudah lebih dari 3 baris

    # Mengaktifkan pembacaan tombol keyboard kustom dan menyembunyikan kursor
    stdscr.keypad(True)
    curses.curs_set(0)
    # AKTIFKAN NON-BLOCKING INPUT: getch() tidak akan berhenti menunggu ketikan, melainkan terus berjalan demi timer
    stdscr.nodelay(True)

    timer_awal = cfg["timer"] # Menyimpan durasi waktu maksimal level
    waktu_mulai = time.time()  # Mencatat waktu presisi saat level dimulai
    input_buffer = ""          # Tempat menampung teks tebakan yang sedang diketik user

    while True:
        stdscr.clear()
        sh, sw = stdscr.getmaxyx() # Mendapatkan ukuran dinamis jendela terminal saat ini

        # Menghitung sisa waktu pengerjaan
        waktu_berjalan = time.time() - waktu_mulai
        sisa_waktu = int(timer_awal - waktu_berjalan)

        # KONDISI KALAH: Jika waktu habis (sisa waktu <= 0)
        if sisa_waktu <= 0:
            stdscr.nodelay(False) # Matikan mode non-blocking sebelum pindah menu
            return tampilkan_menu_akhir(stdscr, False, username) # Panggil menu kalah

        # KONDISI MENANG: Memeriksa apakah semua kata dasar sudah berhasil dijawab oleh user
        if all(jawaban_user[kata] is not None for kata in list_kata_dasar):
            stdscr.nodelay(False)
            return tampilkan_menu_akhir(stdscr, True, username) # Panggil menu menang

        # --- TAHAP RENDERING TAMPILAN GRAFIS TERMINAL ---
        
        # 1. Judul Atas
        judul = f" ANAGRAM RUSH - LEVEL {level} "
        stdscr.addstr(2, (sw - len(judul)) // 2, judul, curses.A_BOLD | curses.A_REVERSE)
        
        info_user = f"Pemain: {username}"
        stdscr.addstr(3, (sw - len(info_user)) // 2, info_user, curses.A_DIM)

        # 2. Gambar Box Wadah Utama Pengingat Soal Game
        box_h, box_w = 11, 70
        box_y, box_x = 5, (sw - box_w) // 2
        draw_box(stdscr, box_y, box_x, box_h, box_w)

        # 3. Bar Informasi Sisa Waktu (Timer)
        teks_timer = f" Sisa Waktu: {sisa_waktu} detik "
        # Efek visual: teks berkedip dan tebal jika waktu kritis di bawah 15 detik
        attr_timer = curses.A_BOLD | curses.A_BLINK if sisa_waktu <= 15 else curses.A_BOLD
        stdscr.addstr(5, box_x + 4, teks_timer, attr_timer)

        # 4. Loop untuk Menampilkan Baris Soal Kata Dasar dan Hasil Slot Jawaban User
        for idx, kata in enumerate(list_kata_dasar):
            pos_y = box_y + 2 + idx
            slot_jawaban = jawaban_user[kata]
            
            if slot_jawaban is None:
                # Jika belum dijawab, tampilkan strip kosong [ _ _ _ _ ] sejumlah panjang kata dasar
                tampilan_slot = "[ " + " ".join(["_"] * len(kata)) + " ]"
                stdscr.addstr(pos_y, box_x + 6, f"{idx+1}. Kata Dasar: {kata.upper():<10} -> {tampilan_slot}")
            else:
                # Jika sudah berhasil dijawab, tampilkan kata jawaban dengan efek tebal warna standar
                stdscr.addstr(pos_y, box_x + 6, f"{idx+1}. Kata Dasar: {kata.upper():<10} -> [ {slot_jawaban.upper()} ]", curses.A_BOLD)

        # 5. Gambar Box Input Form Tempat Mengetik
        input_box_y = box_y + box_h + 1
        draw_box(stdscr, input_box_y, box_x, 3, box_w)
        stdscr.addstr(input_box_y + 1, box_x + 4, f"Ketik Tebakan Anagram: {input_buffer}")

        # 6. Menampilkan Log Baris Notifikasi Pesan Sistem di Bagian Bawah
        notif_y = input_box_y + 4
        for idx, log in enumerate(notifikasi_log):
            if notif_y + idx < sh - 1:
                stdscr.addstr(notif_y + idx, box_x, f"» {log}", curses.A_DIM)

        stdscr.refresh()
        time.sleep(0.05) # Delay mikro untuk mencegah penggunaan daya CPU 100% akibat loop non-blocking

        # --- PROSES MEMBACA INPUT KEYBOARD SECARA REAL-TIME ---
        try:
            ch = stdscr.getch()
        except Exception:
            ch = -1

        if ch == -1:
            continue # Jika tidak ada tombol yang ditekan, lewati proses di bawah dan ulangi loop

        # JIKA USER MENEKAN TOMBOL ENTER (Proses Validasi Dimulai)
        if ch in (10, 13):
            kata_tebakan = input_buffer.strip().lower()
            input_buffer = "" # Kosongkan kembali wadah mengetik setelah enter ditekan

            if not kata_tebakan:
                continue

            cocok = None
            # Mencari kata dasar mana di level ini yang memiliki kecocokan struktur anagram dengan kata tebakan
            for kata_dasar in list_kata_dasar:
                if cek_anagram_sorting(kata_dasar, kata_tebakan):
                    cocok = kata_dasar
                    break

            # TAHAP VALIDASI BERLAPIS (5 Kasus Gagal & 1 Kasus Sukses):
            
            # Kasus 1: Struktur huruf tidak membentuk anagram dengan kata dasar manapun di level ini
            if cocok is None:
                tambah_notifikasi(f"Gagal! Kombinasi huruf '{kata_tebakan.upper()}' salah / bukan anagram soal.")
                continue

            # Kasus 2: Kata tebakan merupakan anagram secara struktur, namun tidak terdaftar resmi di KBBI (file database)
            if kata_tebakan not in kata_pilihan:
                tambah_notifikasi(f"Gagal! Struktur anagram cocok, tapi '{kata_tebakan.upper()}' tidak ada di KBBI!")
                continue

            # Kasus 3: Kata tebakan sama persis dengan kata dasar (Tidak boleh curang memakai kata yang sama)
            if kata_tebakan == cocok:
                tambah_notifikasi(f"Gagal! '{kata_tebakan.upper()}' sama persis dengan kata dasar.")
                continue

            # Kasus 4: Jawaban anagram tersebut sudah pernah diisi sebelumnya oleh user di kolom tersebut
            if jawaban_user[cocok] == kata_tebakan:
                tambah_notifikasi(f"Sudah diisi! '{kata_tebakan.upper()}' sudah ada di kolom tersebut.")
                continue

            # Kasus 5: Kolom kata dasar tersebut sudah sukses terisi oleh kata anagram sah yang lain
            if jawaban_user[cocok] is not None:
                tambah_notifikasi(f"Kolom '{cocok.upper()}' sudah terisi dengan anagram lain!")
                continue

            # KONDISI SUKSES: Lolos semua validasi di atas, simpan jawaban dan reset timer durasi level
            jawaban_user[cocok] = kata_tebakan
            tambah_notifikasi(f"BERHASIL! '{kata_tebakan.upper()}' sah untuk anagram '{cocok.upper()}'!")
            waktu_mulai = time.time() # Reset pencatatan waktu (Pemain diberi bonus waktu penuh lagi setiap tebakan benar)
            timer_awal  = cfg["timer"]

        elif ch in (curses.KEY_BACKSPACE, 127, 8):   # Jika menekan backspace
            input_buffer = input_buffer[:-1]          # Hapus 1 karakter terakhir string

        elif ch in (ord('q'), ord('Q')):              # Jika menekan tombol 'q' untuk menyerah/keluar
            stdscr.nodelay(False)
            return None                               # Keluar dari level dan kembali ke menu awal

        elif 32 <= ch <= 126:                         # Membaca karakter huruf standar yang valid
            if len(input_buffer) < 20:                # Batas maksimal pengetikan tebakan adalah 20 huruf
                input_buffer += chr(ch)


def jalankan_gameplay_level(username, level):
    """Fungsi pembungkus (wrapper) aman untuk memanggil menu_gameplay di dalam lingkungan library curses"""
    return curses.wrapper(menu_gameplay, username, level)
