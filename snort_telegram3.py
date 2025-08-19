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

                # Minimal 3 baris untuk 1 alert
                if len(buffer) >= 3 and "->" in buffer[2]:
                    # Jenis serangan (baris 1)
                    jenis = re.sub(r"\[.*?\]", "", buffer[0]).strip()

                    # Waktu + IP (baris 3)
                    waktu_ip = buffer[2]

                    waktu_match = re.match(r"^(\d+/\d+-\d+:\d+:\d+\.\d+)", waktu_ip)
                    ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s*->\s*(\d+\.\d+\.\d+\.\d+)", waktu_ip)

                    waktu = waktu_match.group(1) if waktu_match else "Tidak diketahui"
                    ip_src = ip_match.group(1) if ip_match else "?"
                    ip_dst = ip_match.group(2) if ip_match else "?"

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
