
# import socket library
import socket
 
# import threading library
import threading

from tkinter import *
from tkinter import font
from tkinter import ttk
import sys


# Choose a port that is free
PORT = 33662
 
# An IPv4 address is obtained
# for the server.  
SERVER = "192.168.1.36";#socket.gethostbyname(socket.gethostname())
 
# Address is stored as a tuple
ADDRESS = (SERVER, PORT)
 
# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"
 
# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []
 
# Create a new socket for
# the server

 
# function to start the connection
class GUI:
    # constructor method
    def __init__(self):
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        stop_threads = False
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Server")
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 400)
        # create a Label
       
        # create a Label
        self.labelName = Label(self.login,
                               text = "Ip: " + SERVER + "\n"+"Port: "+str(PORT),
                               font = "Helvetica 12")
         
        self.labelName.place(relheight = 0.2,
                             relx = 0.35,
                             rely = 0.05)

        self.conNum = Label(self.login,
                               text = "",
                               font = "Helvetica 12")
         
        self.conNum.place(relheight = 0.2,
                             relx = 0.35,
                             rely = 0.3)
        # create a entry box for
        # tyoing the message
        
        # set the focus of the cursor
        
        self.running = False
       
        # create a Continue Button
        # along with action
        self.btnText = "START"
        self.go = Button(self.login,
                         text="START",
                         font = "Helvetica 14 bold",
                         command = lambda: self.run())
       
        self.go.place(relx = 0.4,
                      rely = 0.20)
                      
        self.exit = False

        self.textCons = Text(self.login,
                             width = 20,
                             height = 0.5,
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.55,
                            relwidth = 1,
                            rely = 0.5)
        self.textCons.config(cursor = "arrow")
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
        self.Window.mainloop()
    def run(self):
        self.running = not self.running
        
        if not self.running : 
            self.go.config(text="START")
            self.conNum.config(text="")
            #if self.textCons.see(0):
            self.textCons.config(state = NORMAL)
            self.textCons.delete('1.0', END)
            for client in clients :
                if not self.running :
                    client.send(f"server has closed...".encode(FORMAT))
                client.close()

            server.close()

            '''self.Window.destroy()
            server.close()
            
            server.close()
            sys.exit()
            self.rcv.ex'''
        else :
          
            rcv = threading.Thread(target=self.startChat)
            rcv.start()
    def startChat(self):
        
        
          
            global server
            server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
 
            # bind the address of the
            # server to the socket
            server.bind(ADDRESS)
            server.listen()
            self.go.config(text="END")
            while True:
                
                # accept connections and returns
                # a new connection to the client
                #  and  the address bound to it
        
                try :
                    conn, addr =  server.accept()
                    conn.send("NAME".encode(FORMAT))
                except :
    
                    
                    sys.exit()
                    break
                # 1024 represents the max amount
                # of data that can be received (bytes)
                name = conn.recv(1024).decode(FORMAT)
                
                # append the name and client
                # to the respective list
                names.append(name)
                clients.append(conn)
                
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, str(f"{name} has joined the chat!".encode(FORMAT))[2:]+"\n\n")
                            
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                
                # broadcast message
                self.broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
                
                conn.send('Connection successful!'.encode(FORMAT))
                
                # Start the handling thread
                thread = threading.Thread(target = self.handle,
                                        args = (conn, addr))
                thread.start()
                
                # no. of clients connected
                # to the server
                self.conNum.config(text=f"active connections {threading.activeCount()-2}")
                #print(f"active connections {threading.activeCount()-2}")
        
    # method to handle the
    # incoming messages
    def handle(self,conn, addr):
    
   
        connected = True
        
        while connected:
            # receive message

            try :
                message = conn.recv(1024)
                self.broadcastMessage(message)
            except :
                conn.close()
                self.conNum.config(text=f"active connections {threading.activeCount()-3}")
                connected = False
                if conn in clients:
                    name = names[clients.index(conn)]
                    names.remove(name)
                    if self.running :
                        self.textCons.config(state = NORMAL)
                        self.textCons.insert(END, str(f"{name} quit the chat!".encode(FORMAT))[2:]+"\n\n")
                                    
                        self.textCons.config(state = DISABLED)
                        self.textCons.see(END)
                    clients.remove(conn)
                    for client in clients:
                        try :
                            if self.running :
                                client.send(f"{name} disconnect...".encode(FORMAT))
                            
                        except :
                            client.close()
                            clients.remove(client)
                sys.exit()
                    
                
                    

        
            # broadcast message
        
        
        # close the connection
        conn.close()
    
    # method for broadcasting
    # messages to the each clients
    def broadcastMessage(self,message):
        for client in clients:
            try :
                client.send(message)
            except :
                client.close()
                clients.remove(client)

 
# call the method to
# begin the communication
G = GUI()