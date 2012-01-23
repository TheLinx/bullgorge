Bullgorge
=========

Bullgorge is a watchdog and auto-updater for the dedicated server of [Natural Selection 2](http://naturalselection2.com/).

Dependencies
------------

* *Python 3.x* - Bullgorge was written in Python 3.2.2. It should be forward-compatible for a while.
* *tkinter* - Bullgorge comes with a GUI for easy usage. Unfortunately, at the moment, there is no way to use Bullgorge without having the *tkinter* module for Python installed.
* *Wine* (optional) - The NS2 dedicated server only runs on Windows at the moment. Bullgorge compensates for this by automatically running server.exe with Wine if it detects you're not on Windows.

Installation
------------

Download [bullgorge.py](https://github.com/TheLinx/bullgorge/raw/master/bullgorge.py) and put it somewhere on your server.

Usage
-----

Bullgorge can run in both GUI and command-line mode.

### Using the GUI
Open *bullgorge.py*. You should see this window:

![](http://i.imgur.com/Gu5uB.png)

The first two paths are very important. Bullgorge requires you to run the dedicated server available from HLDSUpdateTool. The first path is the directory where HLDSUpdateTool is located.

The second path is the location of NS2's *server.exe* file. This is also where server log files will end up.

You can specify server info manually, or you can tell the server.exe to load the values from a standard server.xml file.
You can switch between those choices by clicking the button that says **Values** in the image.

When you press **Start Server** a console-like window will open up, showing you Bullgorge status information. If you close this window, the NS2 server will also terminate.

### Using the command-line

Invoke *bullgorge.py* by running `python bullgorge.py`, where `python` is the Python 3.x executable.

To get a list of available command-line options, run `python bullgorge.py -h`.

The main options Bullgorge is interested in are *--hlds* and *--server*.

* *--hlds* is the absolute path of hldsupdatetool.
* *--server* is the absolute path of NS2's server.exe. It is also where server log files will end up.

The rest of the options are passed to the dedicated server as information to the server. Note that specifying a *--file* argument will override any other choices.