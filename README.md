# YouTube Downloader (Tkinter)

A simple desktop YouTube downloader with a clean Tkinter UI. Paste a YouTube link, choose **MP4 (video+audio)** and/or **MP3 (audio only)**, pick a save folder, and download in one click.

> **Note:** Use this tool responsibly and only download content you have permission to download.

---

## Features

- ✅ **MP4 download** (progressive stream: video + audio)
- ✅ **MP3 download** (audio-only stream, auto-converts to `.mp3`)
- ✅ Folder picker (no manual path typing needed)
- ✅ Basic YouTube URL validation
- ✅ Friendly success/error popups

---

## Tech Stack

- **Python** + **Tkinter** (GUI)
- **pytubefix** (`YouTube` streams + downloading)
- **moviepy** (convert downloaded audio file to MP3)
- **certifi + ssl** (uses a trusted CA bundle for HTTPS)

---

## Requirements

- Python **3.9+** recommended
- FFmpeg (required by MoviePy for MP3 conversion)

### Install dependencies

```bash
pip install pytubefix moviepy certifi
