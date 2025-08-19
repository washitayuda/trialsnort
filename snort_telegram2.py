#!/usr/bin/env python3
import requests
import time

TOKEN = "8465459738:AAG7L5oMvT4-9MX_ZHo_LEKskNDUKML_k6o"  # ganti
CHAT_ID = "1277871346"  # ganti
ALERT_FILE = "/var/log/snort/alert"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print(f"Error kirim Telegram: {e}")

print("Monitoring Snort alert log...")
last_line = ""  # simpan log terakhir

try:
    with open(ALERT_FILE, "r") as f:
        f.seek(0, 2)  # skip log lama
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            line = line.strip()
            if line and line != last_line:  # hanya kirim jika log baru berbeda
                send_telegram(f"🚨 SNORT ALERT 🚨\n{line}")
                last_line = line
except FileNotFoundError:
    print(f"File {ALERT_FILE} tidak ditemukan.")