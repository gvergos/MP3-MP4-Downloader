from downloader import Downloader
import tkinter as tk
import time

WIN_WIDTH = 500
WIN_HEIGHT = 300

class Video:
	def __init__(self, choice, string):
		self.choice = choice
		self.string = string
		self.check = False
		self.path = ''
		self.downloader = Downloader(self.choice)

	def search(self, popup):
		self.downloader.launch_youtube()
		self.downloader.search_youtube(self.string)
		self.downloader.get_titles()

		popup.destroy()

		self.popup = tk.Tk()
		self.popup.wm_attributes("-topmost", 1)
		self.popup.wm_title('Video List')
		self.posX = int(self.popup.winfo_screenwidth()/2 - WIN_WIDTH/2)
		self.posY = int(self.popup.winfo_screenheight()/2 - WIN_HEIGHT/2)
		self.popup.geometry('{}x{}+{}+{}'.format(600, 250, self.posX, self.posY))

		self.label = tk.Label(self.popup, text = 'Choose which one to download!')
		self.label.place(x = 40, y = 20)

		self.Button = []
		i = 0
		for title in self.downloader.titles:
			from functools import partial
			button = tk.Button(self.popup, text = i + 1, command = partial(self.clicked, i), width = 3, height = 1)
			self.Button.append(button)
			self.Button[i].place(x = 30, y = 50 + i*30)
			self.text = tk.Label(self.popup, text = title)
			self.text.place(x = 80, y = 50 + i*30 + 5)
			i += 1

		while True:
			self.popup.update_idletasks()
			self.popup.update()
			if (self.check):
				self.check = False
				print('Searching...')
				break

	def download(self):
		self.downloader.find_video(self.path)
		while True:
			try:
				self.downloader.launch_downloader()
			except:
				pass
			if(self.downloader.browser.current_url == 'https://ytmp3.cc/en13/'):
				break
		self.downloader.download()
		self.downloader.close()


	def clicked(self, i):
		self.check = True
		self.path = "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{}]".format(i + 1)
		self.popup.destroy()
