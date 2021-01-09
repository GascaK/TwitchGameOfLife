import requests
import socket
import json

class TGLBot():
    '''TGLBot Class
    TwitchGameOfLife Bot methods and control functions.
    Initialize attempts to connect to a non-blocking IRC channel with
    src/config parameters. If there is an error connecting verify the config
    file is setup correctly.

    Noteable Variables
    ---------------------------------------------
    BOT - None
    Bot name from config file.

    CHANNEL - None
    Channel name from config file.

    irc - socket()
    Socket object with connection to Twitch Channel.
    ---------------------------------------------
    '''
    def __init__(self):
        self.BOT = None
        self.CHANNEL = None

        self.irc = socket.socket()

        try:
            self.connect_bot()
        except:
            print('Unable to Connect')
        
    def connect_bot(self):
        '''connect_bot()
        Gets information from src/config.json file and loads into variables.
        Then attempts to connect to IRC channel with saves information.  This
        function does not return any objects or exceptions.  Must be handled
        at a higher level.

        Noteable Variables
        ---------------------------------------------
        SERVER - str
        Server information from json object

        PORT - str
        Port information from json object

        PASS - str
        Oauth information from json object

        OWNER - str
        Channel owner information from json object

        returns - None
        ---------------------------------------------
        '''
        with open('src/config.json') as jf:
            data = json.load(jf)
            for d in data['config']:
                SERVER = d['SERVER']
                PORT = d["PORT"]
                PASS = d["OAUTH"]
                self.BOT = d["BOT"]
                self.CHANNEL = d["CHANNEL"]
                OWNER = d["OWNER"]

        self.irc.connect((SERVER, PORT))
        self.irc.send((f"PASS {PASS}\n\
                  NICK {self.BOT}\n\
                  JOIN #{self.CHANNEL}\n").encode())
    
    def join_chat(self):
        '''join_chat()

        Noteable Variables
        ---------------------------------------------
        ---------------------------------------------
        '''
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
        '''
        Noteable Variables
        ---------------------------------------------
        ---------------------------------------------
        '''
        message_temp = f"PRIVMSG #{self.CHANNEL} :"
        self.irc.send((message_temp + message + '\n').encode())

    def get_message(self, message):
        '''
        Noteable Variables
        ---------------------------------------------
        ---------------------------------------------
        '''
        try:
            line = (message.split(":",2))[2]
        except:
            line = ""
        return line

    def get_user(self, message):
        '''
        Noteable Variables
        ---------------------------------------------
        ---------------------------------------------
        '''
        temp = message.split(':',1)
        user = temp[1].split('!',1)[0]
        return user

    def get_viewers(self):
        '''
        Noteable Variables
        ---------------------------------------------
        ---------------------------------------------
        '''
        req = requests.get(
        'http://tmi.twitch.tv/group/user/draftjoker/chatters')
        data = json.loads(req.content.decode('utf-8'))
        return data['chatters']['viewers']