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
root.geometry("500x300")
root.resizable(False, False)

# Variables
folder_path = tk.StringVar()
mp3_var = tk.BooleanVar()
mp4_var = tk.BooleanVar()

# UI Elements

# Label for URL
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(pady=(10, 0))

# Input for URL
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Checkbox for MP4 download
mp4_checkbox = tk.Checkbutton(root, text="Download as MP4 (Video + Audio)", variable=mp4_var)
mp4_checkbox.pack()

# Checkbox for MP3 download
mp3_checkbox = tk.Checkbutton(root, text="Download as MP3 (Audio Only)", variable=mp3_var)
mp3_checkbox.pack()

# Button to select save folder
folder_label = tk.Button(root, text="Choose Save Folder", command=select_folder)
folder_label.pack(pady=(10, 0))

# Entry to show a selected folder path
folder_entry = tk.Entry(root, textvariable=folder_path, width=60)
folder_entry.pack(pady=5)

# Button to start download
download_button = tk.Button(root, text="Download", command=download_video, bg="#4CAF50", fg="white", padx=10, pady=5)
download_button.pack(pady=(20, 0))

# Start the GUI loop
root.mainloop()