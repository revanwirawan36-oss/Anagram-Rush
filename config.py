# config.py

#Konfigurasi data level game Anagram Rush
#'timer' dalam satuan detik (60 = 1 menit)

CONFIG_LEVEL = {
    1: {
        "timer": 60,
        "kata_dasar": ["kasur", "peras", "pita", "tipu", "sapi"]
    },
    2: {
        "timer": 60,
        "kata_dasar": ["bakar", "tebar", "darah", "serat", "tunas"]
    },
    3: {
        "timer": 60,
        "kata_dasar": ["pahat", "sirap", "sebar", "kamis", "kamar"]
    },
    4: {
        "timer": 60,
        "kata_dasar": ["teras", "karib", "lebah", "balok", "berat"]
    },
    5: {
        "timer": 60,
        "kata_dasar": ["getar", "selat", "pakar", "laris", "keras"]
    },
    # ── LEVEL 6-10: HARD MODE (WAJIB MINIMAL 2 ANAGRAM YANG SANGAT MUDAH & COMMON) ──
    6: {
        "timer": 60,
        "kata_dasar": ["rakus", "seram", "pasar", "rawat", "sepat"]
    },
    7: {
        "timer": 55,
        "kata_dasar": ["merak", "pesta", "basah", "derap", "karsa"]
    },
    8: {
        "timer": 55,
        "kata_dasar": ["marah", "batal", "talam", "gatal", "salak"]
    },
    9: {
        "timer": 50,
        "kata_dasar": ["kasur", "peras", "keras", "suaka", "seram"]
    },
    10: {
        "timer": 45, # Level Terakhir: Tantangan Kata 6 Huruf yang Familiar
        "kata_dasar": ["garang", "sarang", "kosong", "kreasi", "karang"]
    }
}