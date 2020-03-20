import socket
import sys
import threading
import tkinter as tk

def listenForConnection(portd, si) :
    si = socket.socket()
    si.bind(('', portd))         
    print ("socket binded to " + str(portd)) 
  
    # put the socket into listening mode 
    si.listen(5)      
    print ("socket is listening")
    c, addr = si.accept()
    print("Got a connection from ", addr)
    return c

def connectToListener(port, s, host) :
    s.connect((host, port))
    return s

def receiveData(s):
    while True:
        data = (s.recv(4096)).decode()
        data = "Friend: " + data
        if not data: sys.exit(0)
        messageList.insert(tk.END, data)
        
def sendData(s, toSend):
        sendString = toSend.get()
        sent = "You: " + sendString
        messageList.insert(tk.END, sent)
        s.sendall(sendString.encode())

def closeConnection(s):
    s.close()
    exit(0)

s = socket.socket()
#Start GUI, run this on a button press

port = int(input("Enter port no: "))
host = input("Enter host: ")

try:
    connectToListener(port, s, host)
    c = s
except:
    print("Connection failed, now listening")
    c = listenForConnection(port, s)

master = tk.Tk()
master.title('Quarantine Buddy')
messageFrame = tk.Frame(master)
scroll = tk.Scrollbar(messageFrame)
messageList = tk.Listbox(messageFrame, height = 20, width = 50, yscrollcommand = scroll.set, font= 36)
scroll.pack(side = tk.RIGHT, fill = tk.Y)
messageList.pack(side = tk.LEFT, fill = tk.BOTH)
messageList.pack()
messageFrame.pack()
messageList.insert(tk.END, "-Messages will appear here-")

toSend = tk.StringVar()
messageField = tk.Entry(master, textvariable = toSend)
sendButton = tk.Button(master, text = "Send", command = lambda: sendData(c, toSend) )
closeButton = tk.Button(master, text = "Close connection", command = lambda: closeConnection(c))
messageField.pack()
sendButton.pack()
closeButton.pack()

threading.Thread(target = receiveData, args=(c,)).start()
master.mainloop()
