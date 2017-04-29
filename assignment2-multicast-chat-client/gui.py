import socket
import struct
import Tkinter as tk
import socket
import struct
import threading
import sys
import select
import time
import argparse

#Thread used for listening to multicast_addr
class ReceiverThread( threading.Thread ):
    def __init__(self, mult_addr, bind_addr, port, out):
        threading.Thread.__init__(self)
        self.running = True
        self.mult_addr = mult_addr
        self.bind_addr = bind_addr
        self.port = port
        self.out = out
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.showIp = False
        self.showTime = False

    def run(self):
        membership = socket.inet_aton(self.mult_addr) + socket.inet_aton(self.bind_addr)

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(3)

        self.sock.bind((self.bind_addr, self.port))

        while self.running:
            try:
                message, address = self.sock.recvfrom(messageLength)

                time, message = message.split('\n', 1)
                if self.showIp:
                    parts = message.split(':', 1)
                    if len(parts)>1:
                        message = parts[0] + "@" + address[0] + ":" + parts[1]

                if self.showTime:
                    message = time + '\n' + message

                self.out.configure(state="normal")
                self.out.insert(tk.END, message + "\n")
                self.out.configure(state="disabled")
                self.out.see(tk.END)
            except Exception as e:
                pass

    def stop(self):
        self.running = False
        self.sock.close()

    def setShowIp(self, showIp):
        self.showIp = showIp

    def setShowTime(self, showTime):
        self.showTime = showTime

#Code to broadcast to multcast address
def sendMessageEntry(self):
    sendMessageAsUser()

def sendMessageAsUser():
    if len(texin.get()) > 0:
        message = "["+ username + "]: " + texin.get()

        if len(message) > messageLength:
            tex.configure(state="normal")
            tex.insert(tk.END, "WARNING!!! Messages must be under " + str(messageLength) + " characters.\n")
            tex.configure(state="disabled")
            tex.see(tk.END)
            message = None
        else:
            texin.delete(0, 'end')
            sendMessage(message)

def sendMessage(message):
    message = time.strftime('%X') + '\n' + message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    sock.sendto(message, (args.multicast_addr, args.port))
    sock.close()

#code for setting the users name
def changeUsernameCallBack():
    return lambda : changeUsername()

def changeUsername():
    def setUsernameEntry(self):
        setUsername()

    def setUsername():
        if len(name.get()) > 0:
            global username
            if len(username) > 0:
                sendMessage(username+ " has left the chat.")
            username = name.get()
            user.config(text="Username: " + username)
            sendMessage(username + " has joined the chat.")
            window.destroy()
            top.deiconify()
            texin.focus_set()

    window = tk.Toplevel(top)
    top.withdraw()
    name = tk.Entry(window, bd =5)
    name.pack(side = tk.LEFT)
    name.focus_set()
    name.bind('<Return>', setUsernameEntry)

    b1 = tk.Button(window, text='Set Username'.format(1), command=setUsername)
    b1.pack()

#code to invoke buttons on call
def clickButton(self):
    widget = top.focus_get()
    if widget != top and widget.winfo_class() == 'Button':
        widget.invoke()

def saveChangesCallBack(showIp, showTime):
    return lambda : saveChanges(showIp, showTime)

def saveChanges(showIp, showTime):
    t1.setShowIp(showIp.get())
    t1.setShowTime(showTime.get())

if __name__ == "__main__":
    #arguments and globals
    with open('problem_statement.md', 'r') as fin:
        data = fin.read()

    parser = argparse.ArgumentParser(description=data)
    parser.add_argument('-m','--multicast_addr', type=str, default='224.0.0.1',
                        help='The multicast address to connect to.')
    parser.add_argument('-b','--bind_addr', type=str, default='0.0.0.0',
                        help='The bind address to use.')
    parser.add_argument('-p','--port', type=int, default=3000,
                        help='The port to connect to.')
    parser.add_argument('-u','--username', type=str, default = "",
                        help='The username to connect with.')

    args = parser.parse_args()
    username = args.username
    messageLength = 4096

    #Start GUI
    top = tk.Tk()

    #Sets enter to press button with focus
    top.bind("<Return>", clickButton)

    #set up text receive box
    tex = tk.Text(master=top)
    tex.insert(tk.END,"Hi!! Welcome to the chat on the: " + time.strftime('%x') +  "\n")
    tex.configure(state="disabled")
    tex.bind("<1>", lambda event: tex.focus_set())
    tex.grid(row=0,column=1)

    #start multicast_addr ReceiverThread
    t1 = ReceiverThread(args.multicast_addr, args.bind_addr, args.port, tex)
    t1.start()

    #set up message entry box
    texin = tk.Entry(master=top)
    texin.grid(row=1,column=1, sticky=tk.N+tk.S+tk.E+tk.W)
    texin.bind('<Return>', sendMessageEntry)
    texin.focus_set()

    #send message button
    send = tk.Button(top, text='Send Message'.format(1), command=sendMessage)
    send.grid(row=1,column=0)

    #left hand panel
    bop = tk.Frame()
    bop.grid(row=0,column=0)

    #show current username
    user = tk.Label(bop, text="User Name: " + username)
    user.pack()

    #change username button
    b = tk.Button(bop, text='Change Username'.format(1), command=changeUsernameCallBack())
    b.pack()

    #show ip address/time
    showIp = tk.BooleanVar()
    showTime = tk.BooleanVar()

    tk.Checkbutton(bop, text="Show IP", variable=showIp, command=saveChangesCallBack(showIp, showTime)).pack()
    tk.Checkbutton(bop, text="Show Time", variable=showTime, command=saveChangesCallBack(showIp, showTime)).pack()

    #exit button
    tk.Button(bop, text='Exit', command=top.destroy).pack(side = tk.BOTTOM)

    #Set username first
    if(len(username) == 0):
        changeUsername()
    else:
        sendMessage(username + " has joined the chat.")

    top.mainloop()

    #broadcast left on exit and kill receive thread
    t1.stop()
    sendMessage(username + " has left the chat.")
