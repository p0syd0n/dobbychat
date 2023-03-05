import requests
import tkinter as tk
import tkinter.messagebox as tkm
from time import sleep
import tkinter.simpledialog
import random
import threading
from requests.adapters import HTTPAdapter
from urllib3.util.retry import MaxRetryError
import urllib3
import webbrowser
import pygame

# import sounddevice as sd
# import soundfile as sf
from win10toast import ToastNotifier

#server name and command character
COMMAND_CHAR = "/"
SERVER = "https://chatserver.posydon.repl.co"

def notify(title, message, timeout, icon=''):
  toast = ToastNotifier()
  toast.show_toast(
      title,
      message,
      duration = timeout,
      icon_path = icon,
      threaded = True,
  )

def play_sound(filename):
  pygame.mixer.init()
  pygame.mixer.music.load(filename)
  pygame.mixer.music.play()

def command(command): #sorting the commands, if detected
  global sound, show_ip, admin_password
  try:
    param1 = command.split("/")[2]
  except:
    param1=""
  try:
    param2 = command.split("/")[3]
  except:
    param2=""
  try:
    param3 = command.split("/")[4]
  except:
    param3=""
  command = command.split("/")[1]

  if command == "mute":
    sound = False
    messagebox.delete(0, 'end')
  elif command == "ban":
    ip = param2
    password = param1
    reason = param3
    if session.get(f"{SERVER}/ban?ip={ip}&&password={password}&&reason={reason}"
                   ).text != "403":
      pass
    else:
      tkm.showerror("!", "Ban unsuccesfull")
  elif command == "show_ip":
    admin_password = param1
    if show_ip == "true":
      show_ip = "false"
    else:
      show_ip = "true"
  messagebox.delete(0, 'end')
    
def toggle_sound():
  global sound
  if sound:
    sound = False
  else:
    sound = True

def helpp(): 
  webbrowser.open_new_tab("https://github.com/p0syd0n/dobbychat")


def about():#to lazy
  tkm.showinfo("Info", "Made by posydon using Flask and urllib")


def set_name():
  global name
  try:
    name = tkinter.simpledialog.askstring('Set Name', "Name:")
  except:
    pass


def join():
  global room, room_name
  try:
    room_name = str(tkinter.simpledialog.askstring('Join Room', "Room Name:")) + ".txt"
    if room_name.split(".")[0] == "PRIVATE":
      if tkinter.simpledialog.askstring(
          'Join Private Room', "Private Room Password:",
          show="#") == session.get(f"{SERVER}/get?room={room_name}").text.split("\n")[0].split(":")[1]:
        room = room_name
      else:
        pass
    else:
      room = room_name
  except Exception as e:
    print(e)

def rooms():
  global room
  room = 'home' # if the room is just 'home', the server will return a list of active rooms

def donothing():
  pass

def update_log():
  global messages, room, root, sounds, notification
  while True:
    if session.get(f"{SERVER}/get?room={room}&&show_ip={show_ip}&&password={admin_password}").text.strip() == messages.get(
        "1.0", "end").strip():
      pass
    else:
      messages.config(state= 'normal')
      messages.delete("1.0", "end")
      messages.insert(1.0, session.get(f"{SERVER}/get?room={room}&&show_ip={show_ip}&&password={admin_password}").text)
      messages.config(state= 'disabled')
      if root.state() == "iconic":
        if sounds:
          if notification == "toast":
            notify("activity in chat", f"Activity in {room[:-4]}", 10)
          elif notification == "tone":
            try:
              play_sound('tone.wav')
            except:
              pass
          else:
            pass
          
def send(message):
  global room, name
  if list(message)[0] == COMMAND_CHAR:
    command(message)
  else:
    session.get(f"{SERVER}/post?room={room}&&text={name}: {message}")
    messagebox.delete(0, 'end')


#0000s/roo000000
#rooms/room1.txt
def create():
  new_name = tkinter.simpledialog.askstring('Create Room', 'New Room Name:')
  if str(new_name).split(".")[0] == "PRIVATE":
    passs = tkinter.simpledialog.askstring('Create Private Room',
                                      'Private Room Password:',
                                      show="#")
    session.get(f"{SERVER}/create?name={new_name}&&password={passs}")
  else:
    session.get(f"{SERVER}/create?name={new_name}")


room = "home"
name = "anon-" + str(random.randint(0, 100))
sounds = True
show_ip = "false"
admin_password = ""
notification="tone"

try:
  with open("chat.config", "r") as file:
    content = file.read()
    lines = content.split("\n")
    geometry = lines[1].split(":")
    #ideal formatting: "geometry:300:300" for a 300x300 chat box
    chat_width = int(geometry[1])
    chat_height = int(geometry[2])
except:
  chat_width = 500
  chat_height = 500

try:
  with open("chat.config", "r") as file:
    content = file.read()
    lines = content.split("\n")
    notifications = lines[2].split(":")
    notification = notifications[1]#options: toast, tone, none
except:
  notification = "tone"

session = requests.Session()
retry = urllib3.util.retry.Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

root = tk.Tk()
root.geometry(f"{chat_width}x{chat_height}")
root.resizable(False, False)
root.title("Chat")

# root.rowconfigure(0,weight=1)
# root.columnconfigure(0,weight=1)
 
# root.rowconfigure(1,weight=1)

messagebox = tk.Entry(root)
messagebox.place(rely=1.0, relx=1.0, x=0, y=0, width=chat_width, anchor='se', height=20)
messagebox.bind(("<Return>"), lambda event: send(messagebox.get()))
messagebox.focus()

messages = tk.Text(root)
messages.place(x=0, y=0, width=chat_width, height=chat_height-20)



# messagebox.grid(row=1, column=0, sticky="NSEW")
# messages.grid(row=0, column=0, sticky="NSEW")

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="rooms", command=rooms)
filemenu.add_command(label="join", command=join)
filemenu.add_command(label="set name", command=set_name)
filemenu.add_command(label="create", command=create)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=helpp)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
update_m = threading.Thread(target=update_log, daemon=True)
update_m.start()

try:
  with open("chat.config", "r") as file:
    line_list = file.read().split('\n')
    line = line_list[0]
    room_name = line.split(":")[1]
    try:
      password = room_name.split("-")[1]
    except:
      password=""
    name_name = line.split(":")[2]
    if name_name == "default":
      name = "anon-" + str(random.randint(0, 100))
    elif name_name == "custom_random":
      prefix = line.split(":")[3]
      name = f"{prefix}-" + str(random.randint(0, 100))
    else:
      name = name_name
    if room_name.split(".")[0] == "PRIVATE":
      if password == session.get(f"{SERVER}/get?room={room_name}"
                                    ).text.split("\n")[0].split(":")[1]:
        room = room_name
      else:
        pass
    else:
      if room_name =="home":
        room="home"
      else:
        room = room_name + ".txt"
except:
  pass

root.mainloop()
#chat.config formatting:
#
#chat:room1:Arthur
#geometry:300:300
#notifiactions:toast
#
#for auto joining room1 with the name "Arthur"
#and having a window of 300x300
#and toast notifications (windows) set notifications to "tone" for a tone, and anything else for no notifications
