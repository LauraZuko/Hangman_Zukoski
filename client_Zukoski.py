'''
Laura Zukoski
CS 245 Assignment Hangman

Client file - contains the client side of the Hangman program
Basically establishes connection to client and allows for send and recv
or communication with the server file.
'''

import socket
class Client:
    #establishes connect and passes perform function to display hangman and 
    #phrase to user
    def __init__(self,addr,port):
        self.establish_connection(addr,port)
    def establish_connection(self,addr,port):
        self.socket = socket.socket()
        self.socket.connect((addr,port))
    def send(self,msg):
        self.socket.send(str.encode(msg))
    def recv(self,size):
        buf = self.socket.recv(size)
        if len(buf) > 0:
            return buf.decode()
        else:
            return ""
    def perform(self):
        pass
    def close(self):
        self.socket.close()


class Hangman_Client(Client):
    #Communicates with server, basic send and recv.
    #See server_Zukoski for more description Hangman_Server -> serve function
    def perform(self):
        data = self.recv(64)
        print(data)
        self.send("welcome")
        puzzle = self.recv(1024)
        print("Your puzzle: " + puzzle, end = "")
        self.send("puzzle")
        done = False
        while not done:
            letter=input("Enter your guess:\n")
            self.send(letter)
            complete = self.recv(1)
            puzzle = self.recv(1024)
            print(puzzle)
            #exits loop when the server sends 'Q' because the game is over
            if complete == "Q":
                self.close()
                done=True
         
socket = Hangman_Client("localhost", 8092)
socket.perform()
