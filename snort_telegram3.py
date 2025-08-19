#!/usr/bin/env python3
import requests
import time
import re

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

try:
    with open(ALERT_FILE, "r") as f:
        f.seek(0, 2)  # skip log lama
        buffer = []
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            line = line.strip()
            if line:
                buffer.append(line)

                # Jika sudah cukup baris untuk 1 alert
                if len(buffer) >= 3:
                    jenis = ""
                    waktu = ""
                    ip_src = ""
                    ip_dst = ""

                    # Baris 1 = jenis serangan
                    if "[**]" in buffer[0]:
                        jenis = re.sub(r"\[.*?\]", "", buffer[0]).strip()

                    # Baris 3 = waktu + IP
                    if "->" in buffer[2]:
                        parts = buffer[2].split()
                        if len(parts) >= 3:
                            waktu = parts[0]  # ambil timestamp
                            ip_src = parts[1]
                            ip_dst = parts[3]

                    # Format pesan
                    pesan = (
                        "🚨 SNORT ALERT 🚨\n"
                        f"Jenis Serangan : {jenis}\n"
                        f"Waktu Serangan : {waktu}\n"
                        f"IP Penyerang   : {ip_src}\n"
                        f"IP Target      : {ip_dst}"
                    )

                    send_telegram(pesan)
                    buffer = []  # reset untuk alert berikutnya
except FileNotFoundError:
    print(f"File {ALERT_FILE} tidak ditemukan.")
