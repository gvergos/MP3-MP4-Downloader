import tkinter as tk
from video import Video
import os

WIN_WIDTH = 500
WIN_HEIGHT = 300

class Application:

	def __init__(self, window):
		# Window Title and position
		window.title('Downloader')
		window.resizable(width = False, height = False)
		self.positionX = int(window.winfo_screenwidth()/2 - WIN_WIDTH/2)
		self.positionY = int(window.winfo_screenheight()/2 - WIN_HEIGHT/2)
		window.geometry('{}x{}+{}+{}'.format(WIN_WIDTH, WIN_HEIGHT, self.positionX, self.positionY))

		# Background
		bg_path = os.getcwd() + "\\Images\\bg2.png"

		self.background = tk.PhotoImage(file = bg_path)
		self.bg = tk.Label(window, image = self.background)
		self.bg.pack(fill = 'both', expand = 'yes')

                
		self.choice = 'mp3'

		self.artist = tk.Label(window, text = 'Artist:')
		self.artist.place(x = 100, y = 40)

		self.song = tk.Label(window, text = 'Song:')
		self.song.place(x = 102, y = 80)

		self.artist_entry = tk.Entry(window, textvariable = self.artist, width = 40)
		self.artist_entry.place(x = 150, y = 40)
		self.artist_entry.config(borderwidth = 3, highlightbackground = 'black')

		self.song_entry = tk.Entry(window, textvariable = self.song, width = 40)
		self.song_entry.place(x = 150, y = 80)
		self.song_entry.configure(borderwidth = 3, highlightbackground = 'black')

		self.button_download = tk.Button(window, text = 'Download', width = 15, height = 2, command = self.download_click)
		self.button_download.place(x = 300, y = 200)

		self.mp3_btn = tk.Button(window, text = 'mp3', width = 4, height = 2, command = self.mp3_click)
		self.mp3_btn.place(x = 110, y = 200)

		self.mp4_btn = tk.Button(window, text = 'mp4', width = 4, height = 2, command = self.mp4_click)
		self.mp4_btn.place(x = 160, y = 200)

		self.choice_label = tk.Label(window, text = 'mp3', font='Helvetica 18 bold')
		self.choice_label.place(x = 220, y = 202)

	def mp3_click(self):
		self.choice = 'mp3'
		self.choice_label['text'] = self.choice

	def mp4_click(self):
		self.choice = 'mp4'
		self.choice_label['text'] = self.choice

	def popup(self):
		popup = tk.Tk()
		popup.wm_attributes("-topmost", 1)
		popup.wm_title('Info')
		popup.geometry('{}x{}+{}+{}'.format(200, 200, int(self.positionX + WIN_WIDTH/4 + 10), int(self.positionY + WIN_HEIGHT/4 - 5)))
		loading = tk.Label(popup, text = 'Loading...').place(x = 70, y = 60)
		wait = tk.Label(popup, text = 'Please Wait!').place(x = 60, y = 90)
		return popup

	def download_click(self):
		artist = self.artist_entry.get()
		song = self.song_entry.get()
		string = artist + ' ' + song
		popup = self.popup()
		popup.update_idletasks()
		popup.update()
		video = Video(self.choice, string)
		video.search(popup)
		popup = self.popup()
		while True:
			popup.update_idletasks()
			popup.update()
			video.download()
			popup.destroy()


