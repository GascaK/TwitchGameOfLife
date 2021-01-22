import requests
import socket
import json

class TGLBot():
    '''TGLBot Class
    TwitchGameOfLife Bot methods and control functions.
    Initialize attempts to connect to a non-blocking IRC channel with
    src/config parameters. If there is an error connecting verify the config
    file is setup correctly.
    '''
    def __init__(self):
        '''__init__()

        Noteable Variables
        ---------------------------------------------
        BOT - None
        Bot name from config file.

        CHANNEL - None
        Channel name from config file.

        irc - socket()
        Socket object with connection to Twitch Channel.

        command_list - list
        Commands available to viewers.
        ---------------------------------------------
        '''
        self.BOT = None
        self.CHANNEL = None

        self.irc = socket.socket()

        try:
            self.connect_bot()
        except:
            print('Unable to Connect')

        self.command_list = []
        
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
        Join chat room and wait until end configuration messages are complete.

        Noteable Variables
        ---------------------------------------------
        buffer_join - bit
        Information retrieved from twitch to be parsed.
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
        '''send_message(message)
        Send message to channel.

        Noteable Variables
        ---------------------------------------------
        message_temp - str
        Information header needed to send to channel.

        message - str
        Information to send to channel appended to message_temp.
        ---------------------------------------------
        '''
        message_temp = f"PRIVMSG #{self.CHANNEL} :"
        self.irc.send((message_temp + message + '\n').encode())

    def get_message(self, message):
        '''get_message(message)
        Message retrieved from twitch irc channel message.

        Noteable Variables
        ---------------------------------------------
        line - str
        Attempt to split message from an input message. If no message available
        return empty str.
        ---------------------------------------------

        returns message split
        '''
        try:
            line = (message.split(":",2))[2]
        except:
            line = ""

        return line

    def get_user(self, message):
        '''get_user(message)
        Username retrieved from twitch irc channel message.

        Noteable Variables
        ---------------------------------------------
        user - str
        Attempt to extract username information from twitch irc message if
        none available return empty str.
        ---------------------------------------------

        returns user
        '''
        try:
            temp = message.split(':',1)
            user = temp[1].split('!',1)[0]
        except:
            user = ""

        return user

    def get_viewers(self):
        '''get_viewers()
        Get all listed viewers in a set viewlist.

        Noteable Variables
        ---------------------------------------------
        data - json
        Json object from requested site tmi.twitch.tv.
        ---------------------------------------------

        returns viewers list or None on err
        '''
        req = requests.get(
        'http://tmi.twitch.tv/group/user/draftjoker/chatters')
        #data = json.loads(req.content.decode('utf-8'))
        try:
            data = req.json()
            return data['chatters']['viewers']
        except:
            return None

    def get_commands(self):
        '''get_commands()
        Return command list.

        Noteable Variables
        ---------------------------------------------
        ---------------------------------------------

        returns command_list
        '''
        return self.command_list