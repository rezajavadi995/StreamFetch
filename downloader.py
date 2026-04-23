#!/usr/bin/env python3

import os
import sys
import hashlib
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = os.path.expanduser("~/storage/downloads/yt_downloader")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def is_valid_url(url):
    return "youtube.com" in url or "youtu.be" in url or "soundcloud.com" in url


def get_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r⬇️ {percent} | Speed: {speed} | ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print("\nProcessing file...")


def download(url, choice):
    if choice == "1":
        format_sel = "bestaudio/best"
        post = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        format_sel = "bestvideo+bestaudio/best"
        post = []

    ydl_opts = {
        'format': format_sel,
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'postprocessors': post,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    print("\n🔥 Termux Media Downloader (yt-dlp)\n")

    url = input("Enter URL: ").strip()

    if not is_valid_url(url):
        print("❌ Invalid URL!")
        sys.exit()

    print("\n📦 Fetching info...\n")

    try:
        info = get_info(url)
    except Exception as e:
        print("❌ Error fetching info:", e)
        sys.exit()

    print("\n🎬 Title:", info.get("title"))
    print("⏱ Duration:", info.get("duration"), "seconds")
    print("👤 Uploader:", info.get("uploader"))

    print("\nChoose format:")
    print("1) Audio (MP3)")
    print("2) Video (MP4)")

    choice = input("\nYour choice: ").strip()

    confirm = input("\nProceed download? (y/n): ").lower()

    if confirm != "y":
        print("❌ Cancelled.")
        sys.exit()

    print("\n⬇️ Download starting...\n")

    try:
        download(url, choice)
        print("\n\n✅ Download completed successfully!")
        print(f"📁 Saved in: {DOWNLOAD_DIR}")
    except Exception as e:
        print("\n❌ Download failed:", e)

if __name__ == "__main__":
    main()
