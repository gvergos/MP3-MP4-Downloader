import tkinter as tk
from GUI import Application

def main():
	window = tk.Tk()
	app = Application(window)
	window.mainloop()

if __name__ == '__main__':
	main()