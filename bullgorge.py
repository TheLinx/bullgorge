from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import argparse
import os

if os.name == "nt":
	hlds_exe = "hldsupdatetool.exe"
	serv_exe = "server.exe"
else:
	hlds_exe = "hldsupdatetool"
	serv_exe = "wine server.exe"

parser = argparse.ArgumentParser(description='Guard a NS2 server from crashes.',
	usage='%(prog)s [-h] [--no-gui] [--no-log] [server arguments]')
parser.add_argument('--no-gui', help='suppress the GUI', action='store_true')
parser.add_argument('--no-log', help="don't store server logs", action='store_true')
parser.add_argument('--hlds', help='path of hldsupdatetool', default='.')
parser.add_argument('--server', help='path of NS2 server executable', default='ns2')
parser.add_argument('--name', help='server name to be shown in server browser', default='')
parser.add_argument('--map', help='map to load', default='ns2_summit')
parser.add_argument('--ip', help='ip address to bind to', default='')
parser.add_argument('--port', help='port to use', type=int, default='27015')
parser.add_argument('--limit', help='player slots', type=int, default=12)
parser.add_argument('--lan', help='show server in server browser', action='store_true')
parser.add_argument('--password', help='require a password to join', default='')

class Frontend(Frame):
	start = False

	def start_server(self):
		self.start = True
		self.master.quit()

	def set_by_filedialog(self, stringvar):
		def a():
			stringvar.set(filedialog.askdirectory())
	
	def createWidgets(self):
		self.grid(column=0, row=0, sticky=(N, W, E, S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.hlds = StringVar()
		ttk.Label(self, text="HLDSUpdateTool Path").grid(column=1, row=1, sticky=E)
		hldsframe = ttk.Frame(self)
		hldsframe.grid(column=2, row=1, sticky=(N, W, E, S))
		ttk.Entry(hldsframe, width=20, textvariable=self.hlds).grid(column=1, row=1, sticky=(W, E))
		ttk.Button(hldsframe, width=2, text="...",
			command=self.set_by_filedialog(self.hlds)).grid(column=2, row=1, sticky=E)

		self.server = StringVar()
		ttk.Label(self, text="Server Executable Path").grid(column=1, row=2, sticky=E)
		serverframe = ttk.Frame(self)
		serverframe.grid(column=2, row=2, sticky=(N, W, E, S))
		ttk.Entry(serverframe, width=20, textvariable=self.server).grid(column=1, row=1, sticky=(W, E))
		ttk.Button(serverframe, width=2, text="...",
			command=self.set_by_filedialog(self.server)).grid(column=2, row=1, sticky=E)

		self.sname = StringVar()
		ttk.Label(self, text="Server Name").grid(column=1, row=3, sticky=E)
		ttk.Entry(self, width=20, textvariable=self.sname).grid(column=2, row=3, sticky=(W, E))

		self.mapn = StringVar()
		ttk.Label(self, text="Map Name").grid(column=1, row=4, sticky=E)
		ttk.Entry(self, width=20, textvariable=self.mapn).grid(column=2, row=4, sticky=(W, E))

		self.ip = StringVar()
		ttk.Label(self, text="IP").grid(column=1, row=5, sticky=E)
		ttk.Entry(self, width=20, textvariable=self.ip).grid(column=2, row=5, sticky=(W, E))

		self.port = IntVar()
		ttk.Label(self, text="Port").grid(column=1, row=6, sticky=E)
		ttk.Entry(self, width=20, textvariable=self.port).grid(column=2, row=6, sticky=(W, E))

		self.limit = IntVar()
		ttk.Label(self, text="Player Limit").grid(column=1, row=7, sticky=E)
		ttk.Entry(self, width=20, textvariable=self.limit).grid(column=2, row=7, sticky=(W, E))

		self.lan = BooleanVar()
		ttk.Label(self, text="LAN").grid(column=1, row=8, sticky=E)
		ttk.Checkbutton(self, width=20, variable=self.lan).grid(column=2, row=8, sticky=(W, E))

		self.password = StringVar()
		ttk.Label(self, text="Password").grid(column=1, row=9, sticky=E)
		ttk.Entry(self, width=20, textvariable=self.password).grid(column=2, row=9, sticky=(W, E))

		ttk.Button(self, text="Start Server", command=self.start_server).grid(column=1, row=10,
			sticky=(N, W, E, S), columnspan=2)

		for child in self.winfo_children(): child.grid_configure(padx=3, pady=3)
	
	def setValues(self, args):
		self.hlds.set(args.hlds)
		self.server.set(args.server)
		self.sname.set(args.name)
		self.mapn.set(args.map)
		self.ip.set(args.ip)
		self.port.set(args.port)
		self.limit.set(args.limit)
		self.lan.set(args.lan)
		self.password.set(args.password)
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

if __name__ == '__main__':
	args = parser.parse_args()
	if not args.no_gui:
		root = Tk()
		root.title("Bullgorge")

		app = Frontend(master=root)
		app.setValues(args)
		app.mainloop()
		
		if not app.start:
			raise SystemExit
		
		print(app.hlds.get())