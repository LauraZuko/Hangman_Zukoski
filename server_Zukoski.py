'''
Laura Zukoski
CS 245 Assignment Hangman

server file for Hangman assignment
Creates a hangman game and does all the server side coding.
picks a phrase -> checks if user entered letter in client is in the phrase
if it is changes phrase to display letter guessed if not adds a piece of the 
hangman.
'''

import random
import socket

class Server:
#    Establishes connection with server
    def __init__(self,addr,port,conn_lim):
        self.setup()
        self.establish_connection(addr,port,conn_lim)
    def establish_connection(self,addr,port,conn_lim):
        self.socket = socket.socket()
        self.socket.bind((addr,port))
        self.socket.listen(conn_lim)
        [self.connection, self.address] = self.socket.accept()
    def setup(self):
        pass
    def serve(self):
        pass
    #precond: msg is what is sent to the client
    #postcond: encode as bytes and send to client
    def send(self,msg):
        self.connection.send(str.encode(msg))
    #precond: if connection is live, and contains a message with enough bytes
    #postcond: message will be brought in and decode returning string.
    def recv(self,size):
        buf = self.connection.recv(size)
        if len(buf) > 0:
            return buf.decode()
        else:
            return ""
    def close(self):
            self.connection.close()
            self.socket.close()

class Hangman_Server(Server):
    def setup(self):
#        note - when not hardcoded: run the server, enter the filename, then run the client
#        asks user for file containing phrases, opens and reads and parses file
#        chooses one phrase to be the target phrase
        fname = input("Enter the name of the file that contains the phrases: ")
#        fname = "phrases.txt"
        fvar = open(fname, "r")
        phrase = []
        for line in fvar:
            line.strip()
            phrase.append(str(line))
        choose_phrase = random.choice(phrase)
        fvar.close()
#        creates object of hangman_puzzle class and passes the target phrase
#        initializes incorrect to keep track of wrong guesses
#        creates object of sketcher to draw the hangman
        self.puzzle = Hangman_Puzzle(choose_phrase)
        self.incorrect=0
        self.draw = Hangman_Sketcher()
    def serve(self):
        print("Server initialized and connected to client.")
#        This is the communication with the client. The server sends the client messages
#        If the client recieves the message than it sends a message to the server 
#        which will print a message stating so. 
        self.send("Welcome to Hangman")
        data = self.recv(24)
        if data == 'welcome':
            print("Client Recieved Welcome.")
            self.send(self.puzzle.to_string())
            data = self.recv(24)
            if data == 'puzzle':
                print("Client Recieved puzzle.")     
#                Set done to false so that this loop is run until it changes to true
#                which only happens when the hangman is complete or the user guesses the puzzle
                done = False
                while not done:
                    letter = self.recv(1)
                    print("client entered " + letter + ".")
                    count = self.puzzle.check_letter(letter)
                    if count == 0:
                        build = "The letter you guessed was not in the puzzle."
                        self.incorrect += 1
                    else:
                        build = "Congratulations. You just guessed %d positions." % count
                    build +=  "\nYour puzzle: " + self.puzzle.to_string() + "\n\nHere is your hangman...\n" + self.draw.get_drawing(self.incorrect)
#                    These lines end the game. If the number of incorrect guesses equals 10 (amt of hangman body parts)
#                    then a failed message is sent to the client to be displayed.
#                    If the phrase the user guessed matches the target phrase (all the tiles are turned over)
#                    the server sends a congrats message to the client to display.
#                    If the number of incorrect guesses is less than 10, and the user hasn't uncovered all the blanks,
#                    the loop is still false and keeps going until either option before is met.                    
                    if self.incorrect == 10:
                        build = "You failed. Prepare to die.\nThank you for playing. Good bye."
                        done = True
                        self.send("Q")
                    elif self.puzzle.is_complete():
                        build = "Congratulations. You solved the puzzle and were spared.\nThank you for playing. Good bye."
                        done = True
                        self.send("Q")
                    else:
                        self.send("C")
                    self.send(build)
                self.close()
            
class Hangman_Puzzle():
    def __init__(self, phrase):
#        This defines a target variable that is the phrase the user must guess, also a target_upper if the user enters a lowercase
#        Places underscores for the characters in the alphabet of the phrase (so spaces are kept)
#        Has a list of characters (alphabet) the user can guess
        self.target = phrase
        phrase=phrase.upper()
        self.target_upper = phrase
        alp = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        for guess in alp:
            phrase = phrase.replace(guess, "_")
        self.phrase = phrase
#        print(self.phrase)
    def check_letter(self, letter):
#       Changes letter to uppercase to compare with alp list.
#       If letter is in the target phrase than it displays the letter in the target and continues looking until the end
#       If there is a letter count adds one each time a letter is found (is used to display positions guessed)
#       If the letter is not in the phrase than count stays zero.  count = 0 is outside loop, so that it is reset
#       for each letter the user guesses.
        letter = letter.upper()
        count = 0
        for i in range(len(self.target)):
            if letter == self.target_upper[i]:
                self.phrase=self.phrase[0: i] + self.target[i] + self.phrase[i+1:]
                count += 1
        return count
#    when the phrase matches target puzzle returns true to end game
    def is_complete(self):
        if self.phrase == self.target:
            return True
        return False
#    returns the phrase as a string to send to client
    def to_string(self):
        return self.phrase

class Hangman_Sketcher:
#    Simple method to print hangman using ascii art.
#    If the number of incorrect guesses goes up(num) a part of hangman is drawn with the base
#    Otherwise, just the base is drawn (else statements)
    def get_drawing(self, num):
        result = "----\n"
        if num >= 1:
            result = result + "|  O\n"
        else:
            result = result + "|\n"
        if num >= 2:
            result = result + "|  |\n"
        else:
            result = result + "|\n"
        if num == 3:
            result = result + "|  |\n"
        elif num == 4:
            result = result + "| -|\n"
        elif num >= 5:
            result = result + "| -|-\n"
        else:
            result = result + "|\n"
        if num >= 6:
            result = result + "|  |\n"
        else: 
            result = result + "|\n"
        if num == 7:
            result = result + "| /\n"
        elif num >= 8:
            result = result + "| / \\\n"
        else: 
            result = result + "| \n"
        if num == 9:
            result = result + "|/\n"
        elif num >= 10:
            result = result + "|/    \\\n"
        else:
            result = result + "|\n"
        return result
    

socket = Hangman_Server("localhost", 8092,1)
socket.serve()
