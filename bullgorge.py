from tkinter import *
import argparse

parser = argparse.ArgumentParser(description='Guard a NS2 server from crashes.',
	usage='%(prog)s [-h] [--no-gui] [server arguments]')
parser.add_argument('--no-gui', help='suppress the GUI', action='store_true')
parser.add_argument('--name', help='server name to be shown in server browser')
parser.add_argument('--map', help='map to load')
parser.add_argument('--ip', help='ip address to bind to')
parser.add_argument('--port', help='port to use', type=int)
parser.add_argument('--limit', help='player slots', type=int)
parser.add_argument('--lan', help='show server in server browser')
parser.add_argument('--password', help='require a password to join')

class Frontend(Frame):
	def say_hi(self):
		print("Hello, Onee-chan~")
	
	def createWidgets(self):
		self.QUIT = Button(self)
		self.QUIT["text"] = "quit"
		self.QUIT["fg"] = "red"
		self.QUIT["command"] = self.quit

		self.QUIT.pack({"side": "left"})

		self.hi_there = Button(self)
		self.hi_there["text"] = "Hello"
		self.hi_there["command"] = self.say_hi

		self.hi_there.pack({"side": "left"})

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

if __name__ == '__main__':
	args = parser.parse_args()
	if not args.no_gui:
		root = Tk()
		app = Frontend(master=root)
		app.mainloop()
		root.destroy()