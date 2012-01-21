import argparse

parser = argparse.ArgumentParser(description='Guard a NS2 server from crashes.',
	usage='%(prog)s [-h] [--no-gui] [server arguments]')
parser.add_argument('--no-gui', help='suppress the GUI', action='store_true')
parser.add_argument('--hlds', help='path of hldsupdatetool', default='.')
parser.add_argument('--server', help='path of NS2 server executable', default='ns2')
parser.add_argument('--name', help='server name to be shown in server browser', default='')
parser.add_argument('--map', help='map to load', default='ns2_summit')
parser.add_argument('--ip', help='ip address to bind to', default='')
parser.add_argument('--port', help='port to use', type=int, default='27015')
parser.add_argument('--limit', help='player slots', type=int, default=12)
parser.add_argument('--lan', help='show server in server browser', action='store_true')
parser.add_argument('--password', help='require a password to join', default='')

if __name__ == '__main__':
	args = parser.parse_args()
	if not args.no_gui:
		from tkinter import *
		from tkinter.ttk import *
		root = Tk()
		root.title("Bullgorge")

		mainframe = Frame(root, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)

		hlds = StringVar()
		hlds.set(args.hlds)
		Label(mainframe, text="HLDSUpdateTool Path").grid(column=1, row=1, sticky=E)
		Entry(mainframe, width=20, textvariable=hlds).grid(column=2, row=1, sticky=(W, E))

		server = StringVar()
		server.set(args.server)
		Label(mainframe, text="Server Executable Path").grid(column=1, row=2, sticky=E)
		Entry(mainframe, width=20, textvariable=server).grid(column=2, row=2, sticky=(W, E))

		name = StringVar()
		name.set(args.name)
		Label(mainframe, text="Server Name").grid(column=1, row=3, sticky=E)
		Entry(mainframe, width=20, textvariable=name).grid(column=2, row=3, sticky=(W, E))

		mapn = StringVar()
		mapn.set(args.map)
		Label(mainframe, text="Map Name").grid(column=1, row=4, sticky=E)
		Entry(mainframe, width=20, textvariable=mapn).grid(column=2, row=4, sticky=(W, E))

		ip = StringVar()
		ip.set(args.ip)
		Label(mainframe, text="IP").grid(column=1, row=5, sticky=E)
		Entry(mainframe, width=20, textvariable=ip).grid(column=2, row=5, sticky=(W, E))

		port = IntVar()
		port.set(args.port)
		Label(mainframe, text="Port").grid(column=1, row=6, sticky=E)
		Entry(mainframe, width=20, textvariable=port).grid(column=2, row=6, sticky=(W, E))

		limit = IntVar()
		limit.set(args.limit)
		Label(mainframe, text="Player Limit").grid(column=1, row=7, sticky=E)
		Entry(mainframe, width=20, textvariable=limit).grid(column=2, row=7, sticky=(W, E))

		lan = BooleanVar()
		lan.set(args.lan)
		Label(mainframe, text="LAN").grid(column=1, row=8, sticky=E)
		Checkbutton(mainframe, width=20, variable=lan).grid(column=2, row=8, sticky=(W, E))

		password = StringVar()
		password.set(args.password)
		Label(mainframe, text="Password").grid(column=1, row=9, sticky=E)
		Entry(mainframe, width=20, textvariable=password).grid(column=2, row=9, sticky=(W, E))

		for child in mainframe.winfo_children(): child.grid_configure(padx=3, pady=3)
		root.mainloop()