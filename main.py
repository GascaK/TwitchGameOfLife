import sys
import time
import select
import platform

if platform.system() == 'Windows':
    from src.TGLBot import TGLBot
else:
    from src.TGLBot import TGLBot
    from src.pi_module import RaspPi

from src.data_controller import DataController

class TwitchGameOfLife():
    def __init__(self):
        self.timer_TIME = 20
        self.points_ROUTINE = 100

        self.tgl_bot = TGLBot()
        self.dc = DataController('viewers')
        self.dc.create_table('viewers')

        # Do not load PI module if not in PI.
        if platform.system() != 'Windows':
            self.pi = RaspPi()

    def run(self):
        #command = self.pi.get_commands()
        if platform.system() != 'Windows':
            command = self.pi.get_commands()
        else:
            command = []
        oldtime = time.time()

        #Main non-blocking IRC Loop.
        while True:

            # Socket wait function. Will wait for 5 seconds then continue.
            ready = select.select([self.tgl_bot.irc], [], [], 5)

            try:
                if ready[0]:
                    read = self.tgl_bot.irc.recv(1024).decode()
                else:
                    read = ''
            except:
                read = ''

            if(self.elapsed_timer(oldtime)):
                print('Dispersing coin.')
                oldtime = time.time()
                viewers = self.tgl_bot.get_viewers()
                for each in viewers:
                    self.dc.add_points(each, 100)

            for line in read.split("\r\n"):
                if line == '':
                    continue
                elif 'PING' in line and 'PRIVMSG' not in line:
                    self.tgl_bot.irc.send("PONG tmi.twitch.tv\r\n".encode())
                    print('Sending PONG...')
                elif 'quit' in line:
                    sys.exit()
                else:
                    print(line)
                    user = self.tgl_bot.get_user(line)
                    msgg = self.tgl_bot.get_message(line)
                    print(f'{user}: {msgg}')
                    if msgg.upper() in command:
                        self.pi.command_list(msgg.upper())
    
    def elapsed_timer(self, old_time):
        elapsed = time.time() - old_time
        if(elapsed >= self.timer_TIME):
            return True
        else:
            return False

if __name__ == "__main__":

    #dc = DataController("viewers")
    #dc.create_table("viewers")
    #dc.add_points('draftjoker', 100)
    
    TGL = TwitchGameOfLife()
    # views = TGL.tgl_bot.get_viewers()
    # print(views)

    # for each in views:
    #     dc.add_points(each, 100)
    # sys.exit()

    TGL.tgl_bot.join_chat()
    TGL.run()