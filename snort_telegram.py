#!/usr/bin/env python3
import time
import requests
import os

# KONFIGURASI
TOKEN = "8465459738:AAG7L5oMvT4-9MX_ZHo_LEKskNDUKML_k6o"  # Ganti dengan token bot
CHAT_ID = "1277871346"  # Ganti dengan chat ID Anda
ALERT_FILE = "/var/log/snort/alert"

# Cek posisi awal file (agar tidak kirim log lama)
if not os.path.exists(ALERT_FILE):
    print(f"File alert tidak ditemukan: {ALERT_FILE}")
    exit(1)

with open(ALERT_FILE, "r") as f:
    f.seek(0, os.SEEK_END)

print("Monitoring Snort alert log...")

while True:
    with open(ALERT_FILE, "r") as f:
        lines = f.readlines()
    if lines:
        last_line = lines[-1].strip()
        if last_line:
            # Kirim pesan ke Telegram
            message = f"🚨 SNORT ALERT 🚨\n{last_line}"
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": message}
            try:
                requests.post(url, data=payload)
            except Exception as e:
                print(f"Error kirim Telegram: {e}")
    time.sleep(2)
