import socket
import json

class TGLBot():
    def __init__(self):
        self.BOT = None
        self.CHANNEL = None

        self.irc = socket.socket()

        try:
            self.connect_bot()
        except:
            print('Unable to Connect')
        
    def connect_bot(self):    
        with open('src/config.json') as jf:
            data = json.load(jf)
            for d in data['config']:
                SERVER = d['SERVER']
                PORT = d["PORT"]
                PASS = d["PASS"]
                self.BOT = d["BOT"]
                self.CHANNEL = d["CHANNEL"]
                OWNER = d["OWNER"]

        self.irc.connect((SERVER, PORT))
        self.irc.send((f"PASS {PASS}\n\
                  NICK {self.BOT}\n\
                  JOIN #{self.CHANNEL}\n").encode())
    
    def join_chat(self):
        done = False
        while not done:
            buffer_join = self.irc.recv(1024)
            buffer_join = buffer_join.decode()
            for line in buffer_join.split("\n")[0:-1]:
                print(line)
                if("End of /NAMES list" in line):
                    print(f"{self.BOT} has joined the chat.")
                    self.send_message("Chat room joined!")
                    done = True

    def send_message(self, message):
        message_temp = f"PRIVMSG #{self.CHANNEL} :"
        self.irc.send((message_temp + message + '\n').encode())

    def get_message(self, message):
        try:
            line = (message.split(":",2))[2]
        except:
            line = ""
        return line

    def get_user(self, message):
        temp = message.split(':',1)
        user = temp[1].split('!',1)[0]
        return user