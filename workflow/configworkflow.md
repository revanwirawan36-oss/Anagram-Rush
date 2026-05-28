```markdown
# Workflow & Logic Flow: `config.py` (Anagram Rush)

Dokumen ini menjelaskan alur logika, struktur data, dan cara kerja dari file konfigurasi `config.py` yang digunakan dalam game **Anagram Rush**. 

---

## 1. Penjelasan Umum File
File `config.py` berfungsi sebagai **pusat data (centralized configuration)** untuk mengatur tingkat kesulitan (level) dalam game. Di dalam file ini, terdapat sebuah *dictionary* besar bernama `CONFIG_LEVEL` yang menyimpan informasi penting seperti batas waktu (*timer*) dan daftar kata dasar yang siap diacak menjadi anagram untuk setiap levelnya.

Dengan memisahkan data level ke file tersendiri, kode program utama game (*main loop*) menjadi lebih rapi, modular, dan mudah dikembangkan jika ingin menambah level baru di kemudian hari.

---

## 2. Struktur Data `CONFIG_LEVEL`

Program ini memanfaatkan tipe data **Dictionary di dalam Dictionary (Nested Dictionary)** dengan struktur sebagai berikut:

* **Key Utama (Integer 1-10):** Merepresentasikan nomor level game.
* **Value (Dictionary):** Menyimpan pasangan *key-value* spesifik untuk level tersebut, yaitu:
    * `timer`: Batas waktu pengerjaan dalam satuan detik.
    * `kata_dasar`: List berisi kata-kata dasar yang memiliki potensi anagram yang familiar.

---

## 3. Alur Logika Cara Kerja Program (Workflow)

Jika file ini diintegrasikan ke dalam program game utama, berikut adalah alur logika bagaimana data dari `config.py` digunakan:


```

[Mulai Level X]
│
▼
[Ambil Data dari CONFIG_LEVEL[X]]
│
├─► Atur Hitung Mundur (Sesuai nilai "timer")
│
▼
[Looping untuk Setiap Kata dalam list "kata_dasar"]
│
├─► Acak huruf dari kata dasar (Scrambling)
├─► Tampilkan kata yang diacak ke user
├─► Validasi input user apakah merupakan anagram yang sah
│
▼
[Cek Kondisi Menang/Kalah atau Naik Level]

```

### Detail Langkah Per Langkah:

### Langkah 1: Inisialisasi Level
Saat game dimulai atau pemain berhasil naik level (misalkan ke Level 1), program utama akan memanggil data berdasarkan *key* level tersebut:
```python
current_level = 1
level_data = CONFIG_LEVEL[current_level]

```

### Langkah 2: Pengaturan Waktu (*Timer Control*)

Program membaca nilai dari *key* `"timer"`. Terlihat ada mekanisme penyesuaian tingkat kesulitan yang dinamis:

* **Level 1 - 6:** Diberikan waktu standar **60 detik**.
* **Level 7 - 8:** Waktu mulai dipangkas menjadi **55 detik**.
* **Level 9:** Waktu diperketat menjadi **50 detik**.
* **Level 10 (Final):** Tantangan tersulit dengan waktu hanya **45 detik**.

### Langkah 3: Pengambilan dan Pengacakan Kata

Program akan melakukan iterasi (*looping*) terhadap elemen yang ada di dalam list `"kata_dasar"`.

* **Level 1 - 9:** Berisi kata-kata dengan panjang **5 huruf** (contoh: *kasur*, *peras*, *pita*).
* **Level 10:** Tingkat kesulitan dinaikkan menggunakan kata-kata sepanjang **6 huruf** dengan akhiran seragam (*-ang*) seperti *barang*, *sarang*, dan *datang*.

Di program utama, kata-kata ini nantinya akan diacak posisinya menggunakan fungsi bantuan (misalnya `random.shuffle()`) sebelum ditampilkan kepada pemain untuk ditebak kata aslinya atau variasi anagram lainnya.

---

## 4. Skema Tingkat Kesulitan (Difficulty Curve)

Berdasarkan komentar dan struktur data di dalam file, game ini dirancang dengan peningkatan kesulitan yang terukur:

| Rentang Level | Mode | Karakteristik Kata | Karakteristik Waktu |
| --- | --- | --- | --- |
| **Level 1 - 5** | Easy - Medium | Kata dasar 4-5 huruf yang bervariasi. | Santai (60 Detik) |
| **Level 6 - 9** | Hard Mode | Kata 5 huruf yang memiliki minimal 2 anagram sangat mudah & umum (Contoh: *rakus* bisa jadi *kasur* atau *rusak*). | Menurun bertahap (60s ➔ 55s ➔ 50s) |
| **Level 10** | Final Challenge | Kata diperpanjang menjadi 6 huruf dengan rima serupa. | Sangat ketat (45 Detik) |

---

## 5. Cara Mengimpor ke Program Utama

Untuk menggunakan konfigurasi ini di file Python utama Anda (misalnya `main.py`), Anda cukup menggunakan syntax *import* standar Python:

```python
from config import CONFIG_LEVEL

# Contoh cara mengakses data level 1
print("Waktu Level 1:", CONFIG_LEVEL[1]["timer"], "detik")
print("Daftar Kata:", CONFIG_LEVEL[1]["kata_dasar"])

```

```

```
