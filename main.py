import customtkinter as ctk
from tkinter import filedialog
from pytube import YouTube
import os
import time
from command.deltemp import DeleteFilesAndDirectories
from command.phone import PhoneBookApp
from tkinter import messagebox
import json
import shutil

# Create the Tkinter application instance
app = ctk.CTk()
app.title("System Manager")

# Set the size of the window
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}")

# Function to delete temporary files
def delete_temp_files():
    user = os.path.expanduser('~')
    directory_paths = [os.path.join(user, 'AppData', 'Local', 'Temp'), 'C:\\Windows\\Temp', 'C:\\Windows\\Prefetch']
    
    success_label = ctk.CTkLabel(app, text='Temporary files deleted successfully', text_color='green')
    success_label.pack(pady=1)
    
    deleter = DeleteFilesAndDirectories(directory_paths, success_label)
    deleter.delete()

    app.after(3000, success_label.destroy)

# Function to handle shutdown
def shutdown():
    try:
        delay = int(time_var.get())
        os.system(f"shutdown /s /t {delay}")
    except ValueError:
        error_label.config(text="Please enter a valid time in seconds.", text_color="red")

# Function to handle restart
def restart():
    try:
        delay = int(time_var.get())
        os.system(f"shutdown /r /t {delay}")
    except ValueError:
        error_label.config(text="Please enter a valid time in seconds.", text_color="red")

# Function to toggle the phone book visibility
def toggle_phone_book():
    if phone_book_frame.winfo_ismapped():
        phone_book_frame.pack_forget()
        toggle_phone_button.configure(text="Show Phone Book")
    else:
        phone_book_frame.pack(fill='both', expand=True)
        toggle_phone_button.configure(text="Hide Phone Book")

# Button widget for deleting temp files
delbtn = ctk.CTkButton(app, text='Delete All Temp Files', width=250, command=delete_temp_files)
delbtn.pack(pady=10)

# Separator line
line_label = ctk.CTkLabel(app, text="-"*100)
line_label.pack(pady=10)

# Time entry
time_var = ctk.StringVar()
time_label = ctk.CTkLabel(app, text='Time (in seconds):')
time_label.pack(pady=5)
time_entry = ctk.CTkEntry(app, textvariable=time_var)
time_entry.pack(pady=5)

# Error message label
error_label = ctk.CTkLabel(app, text='')
error_label.pack(pady=5)

# Button widget for shutdown
shutbtn = ctk.CTkButton(app, text='Shutdown', width=250, command=shutdown)
shutbtn.pack(pady=10)

# Button widget for restart
restbtn = ctk.CTkButton(app, text='Restart', width=250, command=restart)
restbtn.pack(pady=10)

line_label = ctk.CTkLabel(app, text="-"*100)
line_label.pack(pady=10)

# Phone book app section
phone_book_frame = ctk.CTkFrame(app)
phone_app = PhoneBookApp(phone_book_frame)

# Toggle button for phone book
toggle_phone_button = ctk.CTkButton(app, text="Show Phone Book", width=250, command=toggle_phone_book)
toggle_phone_button.pack(pady=10)

# Video downloader section
link = ctk.StringVar()
link_label = ctk.CTkLabel(app, text='Paste Link Here:')
link_label.pack(pady=5)
link_entry = ctk.CTkEntry(app, width=70, textvariable=link)
link_entry.pack(pady=5)

def Downloader():
    try:
        url = YouTube(str(link.get()))
        video = url.streams.first()
        file_name = filedialog.askdirectory()
        video.download(file_name)
        ctk.CTkLabel(app, text='DOWNLOADED').pack(pady=10)
    except Exception as e:
        ctk.CTkLabel(app, text=f"Error: {str(e)}", text_color='red').pack(pady=10)

download_btn = ctk.CTkButton(app, text='DOWNLOAD', width=250, command=Downloader)
download_btn.pack(pady=10)

# Start the Tkinter main loop
app.mainloop()
