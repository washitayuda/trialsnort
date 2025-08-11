#!/usr/bin/env python3
import requests
import sys

# Ganti dengan token dan chat_id milik Anda
TOKEN = "8427189453:AAFTTtDI3EZqO8m9FjI19mGYqUz5NTRS2CM"
CHAT_ID = "1277871346"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Pesan diambil dari argumen command line
    message = " ".join(sys.argv[1:])
    send_telegram(message)