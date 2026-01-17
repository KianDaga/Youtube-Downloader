import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from pytubefix import YouTube  # Use pytube if pytubefix is unnecessary
from moviepy.audio.io.AudioFileClip import AudioFileClip  # For MP3 conversion
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

# --------------------------
# FUNCTION: is_valid_url
# --------------------------
def is_valid_url(url):
    """
    Checks if the given string is a valid YouTube URL.

    Args:
        url (str): The YouTube URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return bool(re.match(youtube_regex, url))


# --------------------------
# FUNCTION: download_video
# --------------------------
def download_video():
    """
    Handles the video/audio downloading based on user selection (MP3/MP4).
    """
    url = url_entry.get()
    save_path = folder_entry.get()

    # Validate input
    if not save_path:
        messagebox.showerror("Error", "Please select a folder to save the video.")
        return

    if not is_valid_url(url):
        messagebox.showerror("Error", "Invalid YouTube URL.")
        return

    try:
        yt = YouTube(url)  # Create a YouTube object

        # Handle MP3 download (audio only)
        if mp3_var.get():
            audio_stream = yt.streams.filter(only_audio=True).first()

            if audio_stream:
                out_file = audio_stream.download(output_path=save_path)  # Downloads audio as .mp4
                base, ext = os.path.splitext(out_file)
                mp3_path = base + '.mp3'

                # Convert .mp4 audio to .mp3 using moviepy
                audio_clip = AudioFileClip(out_file)
                audio_clip.write_audiofile(mp3_path)
                audio_clip.close()

                # Optionally remove original .mp4 audio
                os.remove(out_file)

        # Handle MP4 download (video + audio)
        if mp4_var.get():
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4') \
                                     .order_by('resolution') \
                                     .desc().first()

            if video_stream:
                video_stream.download(save_path)

        messagebox.showinfo("Success", "Download completed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")


# --------------------------
# FUNCTION: select_folder
# --------------------------
def select_folder():
    """
    Opens a folder dialog and updates the folder_path StringVar.
    """
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


# --------------------------
# TKINTER GUI INITIALIZATION
# --------------------------
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("760x520")
root.minsize(720, 480)
root.configure(bg="#0f172a")

# Variables
folder_path = tk.StringVar()
mp3_var = tk.BooleanVar(value=True)
mp4_var = tk.BooleanVar()

# Fonts
title_font = ("Georgia", 24, "bold")
subtitle_font = ("Georgia", 11, "italic")
label_font = ("Helvetica", 12)
label_bold = ("Helvetica", 12, "bold")
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")

# Style helpers
def make_button(parent, text, command, primary=False):
    bg = "#f97316" if primary else "#1e293b"
    fg = "#0b1020" if primary else "#cbd5f5"
    active_bg = "#fb923c" if primary else "#334155"
    active_fg = "#0b1020" if primary else "#e2e8f0"
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=active_fg,
        padx=14,
        pady=8,
        relief="flat",
        font=button_font,
        cursor="hand2",
    )

# Background frame
bg_frame = tk.Frame(root, bg="#0f172a")
bg_frame.pack(fill="both", expand=True)

# Header
header = tk.Frame(bg_frame, bg="#0f172a")
header.pack(fill="x", padx=28, pady=(24, 10))

title_label = tk.Label(
    header,
    text="YouTube Downloader",
    font=title_font,
    fg="#f8fafc",
    bg="#0f172a",
)
title_label.pack(anchor="w")

subtitle_label = tk.Label(
    header,
    text="Grab videos or audio with a clean one-click flow",
    font=subtitle_font,
    fg="#94a3b8",
    bg="#0f172a",
)
subtitle_label.pack(anchor="w", pady=(2, 0))

# Card container
card = tk.Frame(bg_frame, bg="#111827", highlightthickness=1, highlightbackground="#1f2937")
card.pack(fill="both", expand=True, padx=24, pady=12)

# URL section
url_section = tk.Frame(card, bg="#111827")
url_section.pack(fill="x", padx=24, pady=(22, 6))

url_label = tk.Label(url_section, text="YouTube URL", font=label_bold, fg="#e2e8f0", bg="#111827")
url_label.pack(anchor="w")

url_entry = tk.Entry(
    url_section,
    font=entry_font,
    width=56,
    bg="#0b1020",
    fg="#e2e8f0",
    insertbackground="#e2e8f0",
    relief="flat",
)
url_entry.pack(fill="x", pady=(8, 0), ipady=6)

# Format section
format_section = tk.Frame(card, bg="#111827")
format_section.pack(fill="x", padx=24, pady=(12, 6))

format_label = tk.Label(format_section, text="Format", font=label_bold, fg="#e2e8f0", bg="#111827")
format_label.pack(anchor="w")

format_row = tk.Frame(format_section, bg="#111827")
format_row.pack(anchor="w", pady=(8, 0))

mp4_checkbox = tk.Checkbutton(
    format_row,
    text="MP4 (Video + Audio)",
    variable=mp4_var,
    font=label_font,
    fg="#e2e8f0",
    bg="#111827",
    selectcolor="#0b1020",
    activebackground="#111827",
    activeforeground="#e2e8f0",
)
mp4_checkbox.pack(side="left", padx=(0, 16))

mp3_checkbox = tk.Checkbutton(
    format_row,
    text="MP3 (Audio Only)",
    variable=mp3_var,
    font=label_font,
    fg="#e2e8f0",
    bg="#111827",
    selectcolor="#0b1020",
    activebackground="#111827",
    activeforeground="#e2e8f0",
)
mp3_checkbox.pack(side="left")

# Save location section
save_section = tk.Frame(card, bg="#111827")
save_section.pack(fill="x", padx=24, pady=(12, 6))

save_label = tk.Label(save_section, text="Save Location", font=label_bold, fg="#e2e8f0", bg="#111827")
save_label.pack(anchor="w")

save_row = tk.Frame(save_section, bg="#111827")
save_row.pack(fill="x", pady=(8, 0))

folder_entry = tk.Entry(
    save_row,
    textvariable=folder_path,
    font=entry_font,
    bg="#0b1020",
    fg="#e2e8f0",
    insertbackground="#e2e8f0",
    relief="flat",
)
folder_entry.pack(side="left", fill="x", expand=True, ipady=6)

folder_button = make_button(save_row, "Choose Folder", select_folder)
folder_button.pack(side="left", padx=(10, 0))

# Action section
action_section = tk.Frame(card, bg="#111827")
action_section.pack(fill="x", padx=24, pady=(20, 24))

download_button = make_button(action_section, "Download Now", download_video, primary=True)
download_button.pack(side="left")

hint_label = tk.Label(
    action_section,
    text="Tip: MP3 downloads audio and auto-converts to .mp3",
    font=label_font,
    fg="#94a3b8",
    bg="#111827",
)
hint_label.pack(side="left", padx=(16, 0))

# Start the GUI loop
root.mainloop()
