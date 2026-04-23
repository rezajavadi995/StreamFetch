#!/data/data/com.termux/files/usr/bin/bash

echo "🔧 Updating packages..."
pkg update -y && pkg upgrade -y

echo "📦 Installing Python..."
pkg install python -y

echo "🎞 Installing FFmpeg..."
pkg install ffmpeg -y

echo "📥 Installing yt-dlp..."
pkg install python-pip -y
pip install yt-dlp

echo "📁 Enabling storage access..."
termux-setup-storage

echo "🔗 Making script executable..."
chmod +x downloader.py

echo "⚡ Creating symlink command..."

ln -sf $PWD/downloader.py $PREFIX/bin/downloader

echo "✅ Installation completed!"
echo "👉 Now just run: downloader"
