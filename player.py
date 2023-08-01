import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk
import time
import pygame

class MusicPlayer:


    def __init__(self):
        self.directory = None
        self.song = []
        self.current_file_index = 0
        self.paused = False
        self.stopped = False
        self.cover_images = {}
        self.song_length = 0
        self.current_time = 0

        pygame.mixer.init()


    def browse_directory(self):
       
        self.directory = filedialog.askdirectory()
        files = os.listdir(self.directory)

        self.song = [file for file in files if file.endswith(".mp3")]


    def play(self):
        if not self.song:
            print("No music files found in the selected directory.")
            return

        # If music is already playing, then pausing
        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            return

        # If music is paused or stopped, then resuming or start playing
        selected_file = os.path.splitext(self.song[self.current_file_index])[0]
        file_path = os.path.join(self.directory, self.song[self.current_file_index])
        
        # If the music was paused, resuming from the last paused time
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            # Reseting the current_time to zero when starting a new song
            self.current_time = 0
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(start=self.current_time)

        self.song_length = pygame.mixer.Sound(file_path).get_length()

        cover_image = self.load_cover_image(selected_file)
        l1.config(image=cover_image)
        l1.image = cover_image
        l2.config(text=selected_file)

        self.update_progress()


    def update_progress(self):

        time_elapsed = self.current_time
        time_elapsed_str = time.strftime("%M:%S", time.gmtime(time_elapsed))

        time_label.config(text=time_elapsed_str)

        time_remaining = max(self.song_length - time_elapsed, 0)  
        time_remaining_str = time.strftime("%M:%S", time.gmtime(time_remaining))

        progress_value = (time_elapsed / self.song_length) * 100
        progress_bar["value"] = progress_value

        remaining_label.config(text=time_remaining_str)

        window.after(200, self.update_progress)


    def on_progress_click(self, event):

        x = event.x
        progress_value = x / progress_bar.winfo_width()
        seek_position = int(progress_value * self.song_length)
        self.current_time = seek_position

        pygame.mixer.music.rewind()
        pygame.mixer.music.play(start=self.current_time) 


    def update_time(self):
    
        if pygame.mixer.music.get_busy():
            self.current_time += 1

        window.after(1000, self.update_time)


    def load_cover_image(self, selected_file):
        
        cover_image_path = os.path.join(self.directory, selected_file + ".png")
        print(f"Cover image path: {cover_image_path}")

        try:
           
            cover_image = Image.open(cover_image_path)
       
            cover_image = cover_image.resize((290, 290), Image.LANCZOS)
     
            cover_image_tk = ImageTk.PhotoImage(cover_image)

            self.cover_images[selected_file] = cover_image_tk
            return cover_image_tk

        except (OSError, FileNotFoundError):
          
            default_image_path = "music.png"  
            default_cover_image = Image.open(default_image_path)
            default_cover_image = default_cover_image.resize((290, 290), Image.LANCZOS)
            default_cover_image_tk = ImageTk.PhotoImage(default_cover_image)

            print(f"Cover image not found for: {selected_file}")
            print(f"Default image path: {default_image_path}")

            self.cover_images[selected_file] = default_cover_image_tk
            return default_cover_image_tk


    def update_cover_image(self):
        if music_player.song:
            selected_file = music_player.song[music_player.current_file_index]
            cover_image = music_player.load_cover_image(selected_file)
            l1.config(image=cover_image)
            l1.image = cover_image  
            window.after(500, self.update_cover_image) 


    def pause_music(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True


    def resume_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False


    def stop_music(self):
        pygame.mixer.music.stop()
        self.stopped = True


    def play_next(self):
        if self.current_file_index < len(self.song) - 1:
            self.current_file_index += 1
            self.stop_music()
            self.play()


    def play_previous(self):
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self.stop_music()
            self.play()


music_player = MusicPlayer()

window = tk.Tk()
window.title("Music Player")
window.geometry("400x550")
window.configure(bg="#000000")
window.resizable(True,True)
window.iconbitmap('icon.ico')

#Frames
cover_frame = tk.Frame(window, bg="#000000")
cover_frame.pack(side=tk.TOP, anchor= tk.CENTER, expand=True,pady = 30)

button_frame = tk.Frame(window, bg="#000000",width=290,height=290)
button_frame.pack(expand=True,anchor=tk.CENTER)

style = ttk.Style()
style.theme_use('default')
style.configure("Custom.Horizontal.TProgressbar", thickness=4)

# Setting a default image for the cover frame
default_image_path = "music.png"  # Replace with the path to your default image
default_cover_image = Image.open(default_image_path)
default_cover_image = default_cover_image.resize((290, 290), Image.LANCZOS)
default_cover_image_tk = ImageTk.PhotoImage(default_cover_image)

#Labels
l1 = tk.Label(cover_frame, image=default_cover_image_tk, background="#000000")
l1.image = default_cover_image_tk
l1.pack(anchor=tk.N,side=tk.TOP, expand=True)  # Center the image label

l2 = tk.Label(cover_frame, text="", fg="white", background="#000000", font=("Toma Sans", 12,"bold"))
l2.pack(anchor=tk.S, expand=True, pady=15)  # Use pack instead of place

#Buttons
browse_image = tk.PhotoImage(file="library.gif")
browse_image = browse_image.subsample(3,3)
b1 = tk.Button(button_frame, image = browse_image, command=music_player.browse_directory, borderwidth=0,
               highlightthickness=0, highlightbackground="#000000", highlightcolor="#000000",width= 25,height=25)
b1.grid(row=2, column=1)  # Use pack instead of pack

play_image = tk.PhotoImage(file="play.gif")
play_image = play_image.subsample(3,3)
b2 = tk.Button(button_frame, image = play_image, command=music_player.play, borderwidth=0,
               highlightthickness=0, highlightbackground="#000000", highlightcolor="#000000",width= 60,height=60)
b2.grid(row=0, column=1, padx=0, pady=10)  # Use pack instead of pack

next_image = tk.PhotoImage(file="next.gif")
next_image = next_image.subsample(2,2)
b3 = tk.Button(button_frame,image = next_image,command=music_player.play_next,borderwidth=0,
               highlightthickness=0, highlightbackground="#000000", highlightcolor="#000000",width= 53,height=53)
b3.grid(row=0, column=2, padx=30, pady=10)  # Use pack instead of pack

previous_image = tk.PhotoImage(file="previous.gif")
previous_image = previous_image.subsample(2,2)
b4 = tk.Button(button_frame,image = previous_image,command=music_player.play_previous,borderwidth=0,
               highlightthickness=0, highlightbackground="#000000", highlightcolor="#000000",width= 53,height=53)
b4.grid(row=0, column=0, padx=30, pady=10) # Use pack instead of pack

#Progress bar
progress_bar = ttk.Progressbar(cover_frame, orient="horizontal", mode="determinate",
                               style="Custom.Horizontal.TProgressbar", length=500)
progress_bar.pack(anchor=tk.S,expand=True)  # Center the progress bar

progress_bar.bind("<Button-1>", music_player.on_progress_click)

#Time labels
time_label = tk.Label(cover_frame, text="00:00", fg="white", bg="#000000")
time_label.pack(anchor=tk.W,side = tk.LEFT,expand= True)  # Use pack instead of pack

remaining_label = tk.Label(cover_frame, text="00:00", fg="white", bg="#000000")
remaining_label.pack(anchor=tk.E,side = tk.LEFT,expand= True)  # Use pack instead of pack


music_player.update_cover_image()

music_player.update_time()

window.mainloop() 







