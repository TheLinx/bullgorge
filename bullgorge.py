from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
import argparse
import io
import os
import re
import subprocess
import time
import threading

parser = argparse.ArgumentParser(description='Guard a NS2 server from crashes.',
	usage='%(prog)s [-h] [--no-gui] [--no-log] [--hlds PATH] [--server PATH] [server arguments]')
parser.add_argument('--no-gui', help='suppress the GUI', action='store_true')
parser.add_argument('--no-log', help="don't store server logs", action='store_true')
parser.add_argument('--hlds', help='path of hldsupdatetool', default='')
parser.add_argument('--server', help='path of NS2 server executable', default='')
parser.add_argument('--file', help='a server.xml info file', default='')
parser.add_argument('--name', help='server name to be shown in server browser', default='')
parser.add_argument('--map', help='map to load', default='ns2_summit')
parser.add_argument('--ip', help='ip address to bind to', default='')
parser.add_argument('--port', help='port to use', type=int, default='27015')
parser.add_argument('--limit', help='player slots', type=int, default=12)
parser.add_argument('--lan', help='show server in server browser', action='store_true')
parser.add_argument('--password', help='require a password to join', default='')

class Updatetool():
	ver_regex = re.compile("Installing 'Natural Selection 2 - Dedicated Server' version (\d+)")

	def construct_commandline(self):
		args = []
		args.append(os.path.join(self.srv.hlds_path, self.srv.hlds_exe))
		args.extend(['-command', 'update', '-game', 'naturalselection2', '-dir'])
		args.append(self.srv.server_path)
		return args

	def check_updates(self):
		args = self.construct_commandline()
		s = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()
		m = self.ver_regex.search(str(s))
		self.version = int(m.group(1))
	
	def __init__(self, srv):
		self.srv = srv

class Frontend(Frame):
	start = False

	def start_server(self):
		self.start = True
		self.master.quit()

	def set_by_askdirectory(self, stringvar):
		def a():
			stringvar.set(filedialog.askdirectory())
		return a
	
	def set_by_askopenfilename(self, stringvar):
		def a():
			stringvar.set(filedialog.askopenfilename())
		return a
	
	def toggle_file(self, event):
		self.use_file = not self.use_file
		if self.use_file:
			relief = 'sunken'
			text = "Configuration File"
			self.valuesframe.grid_forget()
			self.fileframe.grid(column=1, row=5, columnspan=2)
		else:
			relief = 'raised'
			text = "Values"
			self.valuesframe.grid(column=1, row=4, sticky=(N, W, E, S), columnspan=2)
			self.fileframe.grid_forget()
		event.widget['text'] = text
		event.widget['relief'] = relief
	
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
			command=self.set_by_askdirectory(self.hlds)).grid(column=2, row=1, sticky=E)

		self.server = StringVar()
		ttk.Label(self, text="Server Executable Path").grid(column=1, row=2, sticky=E)
		serverframe = ttk.Frame(self)
		serverframe.grid(column=2, row=2, sticky=(N, W, E, S))
		ttk.Entry(serverframe, width=20, textvariable=self.server).grid(column=1, row=1, sticky=(W, E))
		ttk.Button(serverframe, width=2, text="...",
			command=self.set_by_askdirectory(self.server)).grid(column=2, row=1, sticky=E)

		self.use_file = False
		values_toggle = ttk.Label(self, text="Values", relief='raised', borderwidth=4, anchor=CENTER)
		values_toggle.grid(column=1, row=3, sticky=(N, W, E, S), columnspan=2)
		values_toggle.bind("<ButtonPress-1>", self.toggle_file)

		self.valuesframe = ttk.Frame(self)
		self.valuesframe.grid(column=1, row=4, sticky=(N, W, E, S), columnspan=2)
		self.valuesframe.columnconfigure(0, weight=1)
		if 1: # valuesframe 
			self.sname = StringVar()
			ttk.Label(self.valuesframe, text="Server Name").grid(column=1, row=1, sticky=E)
			ttk.Entry(self.valuesframe, width=20, textvariable=self.sname).grid(column=2, row=1, sticky=(W, E))

			self.mapn = StringVar()
			ttk.Label(self.valuesframe, text="Map Name").grid(column=1, row=2, sticky=E)
			ttk.Entry(self.valuesframe, width=20, textvariable=self.mapn).grid(column=2, row=2, sticky=(W, E))

			self.ip = StringVar()
			ttk.Label(self.valuesframe, text="IP").grid(column=1, row=3, sticky=E)
			ttk.Entry(self.valuesframe, width=20, textvariable=self.ip).grid(column=2, row=3, sticky=(W, E))

			self.port = IntVar()
			ttk.Label(self.valuesframe, text="Port").grid(column=1, row=4, sticky=E)
			ttk.Entry(self.valuesframe, width=20, textvariable=self.port).grid(column=2, row=4, sticky=(W, E))

			self.limit = IntVar()
			ttk.Label(self.valuesframe, text="Player Limit").grid(column=1, row=5, sticky=E)
			ttk.Entry(self.valuesframe, width=20, textvariable=self.limit).grid(column=2, row=5, sticky=(W, E))

			self.lan = BooleanVar()
			ttk.Label(self.valuesframe, text="LAN").grid(column=1, row=6, sticky=E)
			ttk.Checkbutton(self.valuesframe, width=20, variable=self.lan).grid(column=2, row=6, sticky=(W, E))

			self.password = StringVar()
			ttk.Label(self.valuesframe, text="Password").grid(column=1, row=7, sticky=E)
			ttk.Entry(self.valuesframe, width=20, textvariable=self.password).grid(column=2, row=7, sticky=(W, E))

		self.fileframe = ttk.Frame(self)
		self.fileframe.grid(column=1, row=5, columnspan=2)
		self.fileframe.columnconfigure(0, weight=1)
		if 1: # fileframe 
			self.file = StringVar()
			ttk.Label(self.fileframe, text="Config File").grid(column=1, row=1, sticky=E, padx=50)
			ttk.Entry(self.fileframe, width=20, textvariable=self.file).grid(column=2, row=1, sticky=(W, E))
			ttk.Button(self.fileframe, width=2, text="...",
				command=self.set_by_askopenfilename(self.file)).grid(column=3, row=1, sticky=E)

		ttk.Button(self, text="Start Server", command=self.start_server).grid(column=1, row=6,
			sticky=(N, W, E, S), columnspan=2)

		for child in self.winfo_children(): child.grid_configure(padx=3, pady=3)
		for child in self.valuesframe.winfo_children(): child.grid_configure(padx=3, pady=3)
		for child in self.fileframe.winfo_children(): child.grid_configure(padx=3, pady=3)
	
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
		self.fileframe.grid_forget()

class Server():
	options = {}
	server = None
	
	def init_gui(self):
		root = Tk()
		root.title("Bullgorge")

		app = Frontend(master=root)
		app.setValues(self.args)
		app.mainloop()
		
		if not app.start:
			raise SystemExit
		
		self.hlds_path = app.hlds.get()
		self.server_path = app.server.get()
		if app.use_file:
			self.options['file'] = app.file.get()
			return
		if app.sname.get() != "":
			self.options['name'] = app.sname.get()
		else:
			self.options['name'] = "Natural Selection 2 Server"
		self.options['map'] = app.mapn.get()
		if app.ip.get() != "":
			self.options['ip'] = app.ip.get()
		self.options['port'] = app.port.get()
		self.options['limit'] = app.limit.get()
		self.options['lan'] = bool(app.lan.get())
		if app.password.get() != "":
			self.options['password'] = app.password.get()
		
		root.destroy()
	
	def init_cli(self):
		self.hlds_path = self.args.hlds
		self.server_path = self.args.server
		if self.args.file != "":
			self.options['file'] = self.args.file
			return
		if self.args.name != "":
			self.options['name'] = self.args.name
		else:
			self.options['name'] = "Natural Selection 2 Server"
		self.options['map'] = self.args.map
		if self.args.ip != "":
			self.options['ip'] = self.args.ip
		self.options['port'] = self.args.port
		self.options['limit'] = self.args.limit
		self.options['lan'] = self.args.lan
		if self.args.password != "":
			self.options['password'] = self.args.password
	
	def __init__(self, args):
		print("#### Initializing Bullgorge ####")
		self.args = args
		self.gui = not args.no_gui
		if self.gui:
			self.init_gui()
		else:
			self.init_cli()
		if self.server_path == '':
			self.server_path = '.'
		if os.name == "nt":
			self.hlds_exe = "hldsupdatetool.exe"
			self.server_exe = "server.exe"
			self.use_wine = False
			if len(self.server_path) < 1 or self.server_path[1] != ":": # assume it's a path relative to the hlds_path
				self.server_path = os.path.join(self.hlds_path, self.server_path)
		else:
			self.hlds_exe = "hldsupdatetool"
			self.server_exe = "server.exe"
			self.use_wine = True
			if self.server_path[0] != '/': # assume it's a path relative to the hlds_path
				self.server_path = os.path.join(self.hlds_path, self.server_path)
	
	def check_paths(self):
		open(os.path.join(self.hlds_path, self.hlds_exe)).close() # check if we can find the hldsupdatetool executable
		open(os.path.join(self.server_path, self.server_exe)).close() # check if we can find the ns2 server executable
	
	def construct_commandline(self):
		args = []
		if self.use_wine:
			args.append('wine')
		args.append(self.server_exe)
		args.append('-save')
		args.append('0')
		if 'file' in self.options:
			args.append('-file')
			args.append(self.options['file'])
			return args
		args.append('-name')
		args.append(self.options['name'])
		args.append('-map')
		args.append(self.options['map'])
		if 'ip' in self.options:
			args.append('-ip')
			args.append(self.options['ip'])
		args.append('-port')
		args.append(str(self.options['port']))
		args.append('-lan')
		args.append(str(int(self.options['lan'])))
		if 'password' in self.options:
			args.append('-password')
			args.append(self.options['password'])
		return args

	def initial_updates(self):
		print("## Checking for initial updates...")
		self.upd = Updatetool(srv)
		self.upd.check_updates()
		self.last_update = time.time()
		self.last_version = self.upd.version
		print("## Running Natural Selection 2 Dedicated Server v" + str(self.upd.version))
	
	def guard_server(self):
		args = self.construct_commandline()
		os.chdir(self.server_path)
		print("#### Bullgorge Initiated ####")
		print("## Ready to start guarding...")
		print("## Server commandline: " + " ".join(args))
		if not self.gui:
			print("## Terminate Bullgorge using Ctrl+C")
		while True: # this shouldn't be a problem...
			logf = None
			if not self.args.no_log:
				logfn = datetime.now().isoformat('-').replace(':', '-') + ".log"
				print("## Opening log file '" + logfn + "'")
				logf = open(logfn, 'wb')
			p = subprocess.Popen(args, stdout=logf, stderr=logf)
			while not p.poll():
				time.sleep(1)
				if self.gui:
					global cls
					if not cls.is_alive(): # if the console has been closed, we need to kill ourselves
						raise SystemExit
				if self.last_update + 300 <= time.time():
					print("## Checking for updates...")
					self.upd.check_updates()
					if self.upd.version > self.last_version:
						print("## New version detected! Shutting down server...")
						p.terminate() # This will break out of the while loop
					print("## Nothing new.")
			print("## SERVER STOPPED, code: " + str(p.returncode))
			print("## Waiting 5 seconds before restarting...")
			time.sleep(5)
			if logf:
				logf.close()
			print("## Restarting now...")

class Console(threading.Thread):
	def write(self, buf):
		for line in buf.rstrip().splitlines():
			self.view.insert(END, line.rstrip() + "\n")
	
	def callback(self):
		self.root.destroy()

	def run(self):
		self.root = Tk()
		self.root.title("Bullgorge Console")

		self.view = scrolledtext.ScrolledText(self.root)
		self.view.grid(column=1, row=1, sticky=(N, W, E, S))
		self.root.protocol("WM_DELETE_WINDOW", self.callback)

		with self.cond:
			self.cond.notify() # we're ready to go!
		self.root.mainloop()
	
	def __init__(self, cond):
		threading.Thread.__init__(self)
		self.cond = cond
		self.start()

if __name__ == '__main__':
	srv = Server(parser.parse_args())
	if srv.gui:
		condition = threading.Condition()
		condition.acquire()
		global cls
		cls = Console(condition)
		condition.wait() # wait until the console is ready for output before we connect the pipes
		sys.stdout = cls
		sys.stderr = cls
	try:
		srv.check_paths()
		srv.initial_updates()
		srv.guard_server()
	except Exception as e:
		print(e)
		print("## Mayday, mayday, we're going down!")
		if srv.server != None and srv.server.poll():
			srv.server.terminate() # make sure the server dies if we do
			srv.server.wait()
		if cls != None:
			cls.join() # just wait until the console is closed
		raise SystemExit