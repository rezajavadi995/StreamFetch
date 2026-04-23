#!/usr/bin/env python3
#🔥 Termux Media Downloader (StreamFetch) v1.0.0
#MR_Hngr :) 
import os
import re
import sys
import time
import hashlib
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = os.path.expanduser("~/storage/downloads/yt_downloader")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def loading(text="Loading"):
    chars = "|/-\\"
    for i in range(10):
        sys.stdout.write(f"\r{text} {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r" + " " * 30 + "\r", end="")
    
#def is_valid_url(url):
    #return "youtube.com" in url or "youtu.be" in url or "soundcloud.com" in url

def is_valid_url(url):
    pattern = r"(youtube\.com|youtu\.be|soundcloud\.com)"
    return re.search(pattern, url) is not None
    

def get_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'js_runtimes': 'node',
    }

    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def progress_hook(d):
    if d['status'] == 'downloading':
        speed = d.get('_speed_str') or "N/A"
        eta = d.get('_eta_str') or "N/A"
        percent = d.get('_percent_str') or ""
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
        'js_runtimes': 'node',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_with_retry(url, choice, retries=3):
    for attempt in range(retries):
        try:
            print(f"\n⬇️ Attempt {attempt+1}/{retries}")
            download(url, choice)
            return True
        except Exception as e:
            print(f"❌ Failed attempt {attempt+1}: {e}")

            if attempt < retries - 1:
                print("🔁 Retrying...\n")
                time.sleep(2)

    return False


def main():
    clear_screen()
    print("="*40)
    print("🔥 StreamFetch v1.0.0")
    print("   Media Downloader for free")
    print("="*40 + "\n")
   # print("\n🔥 Termux Media Downloader (yt-dlp)\n")
    

    url = input("Enter URL: ").strip()
    loading("Checking URL")
    if not is_valid_url(url):
        print("❌ Invalid URL!")
        sys.exit()

    

    print("\n📦 Fetching info...\n")

    try:
        loading("Fetching info")
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
        success = download_with_retry(url, choice)
        print("\n\n✅ Download completed successfully!")
        print(f"📁 Saved in: {DOWNLOAD_DIR}")
    except Exception as e:
        print("\n❌ Download failed:", e)

if __name__ == "__main__":
    main()
