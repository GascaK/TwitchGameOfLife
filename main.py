import sys
import time
import select
import platform

from src.TGLBot import TGLBot
from src.data_controller import DataController

if platform.system() != 'Windows':
    from src.pi_module import RaspPi
    SYSTEM_OS = 'PI'
else:
    SYSTEM_OS = 'WINDOWS'

class TwitchGameOfLife():
    def __init__(self):

        # Points Variability #
        self.timer_TIME = 120 # Seconds.
        self.points_ROUTINE = 100 # Amount of points to add every timer_TIME
        #////////////////////#

        self.tgl_bot = TGLBot()
        self.dc = DataController('viewers')
        self.dc.create_table('viewers')

        # Do not load PI module if not in PI.
        if SYSTEM_OS == 'PI':
            self.pi = RaspPi()

    def run(self):
        # Command Lists
        pi_commands = {'COMMANDS':
                        ['!TEST'],
                      '!TEST': 300}
        view_commands = self.dc.get_commands()
        if platform.system() != 'Windows':
            # OS is not windows. Load pi_module.
            pi_commands = self.pi.get_commands()

        # Loop Setup Variables.
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
                    # Print out readable message.
                    print(line) # delete for prettiness ?
                    user = self.tgl_bot.get_user(line)
                    msgg = self.tgl_bot.get_message(line)
                    print(f'{user}: {msgg}')

                    # Check if in Viewer Commands.
                    if msgg.upper() in view_commands:
                        info, i_retr = self.dc.command_controller(msgg.upper(), user)
                        if(info is not None):
                            # Info returned. Print and send to twitch chat.
                            print(f'{user}: {i_retr}')
                            self.tgl_bot.send_message(f'{user}: {i_retr}')

                    # Check if in Pi Commands.
                    if msgg.upper() in pi_commands['COMMANDS']:
                        avail_points, _ = self.dc.get_points(user)
                        com_cost = pi_commands[msgg.upper()]
                        if(avail_points >= com_cost):
                            self.pi.command_controller(msgg.upper())
                            self.dc.spend_points(user, com_cost)
                            print(f"{user} spent {com_cost} points on {msgg}.")
                            self.tgl_bot.send_message(f"{user} spent \
                                {com_cost} points on {msgg}.")

    def elapsed_timer(self, old_time):
        elapsed = time.time() - old_time
        if(elapsed >= self.timer_TIME):
            return True
        else:
            return False

if __name__ == "__main__":
    TGL = TwitchGameOfLife()
    TGL.tgl_bot.join_chat()
    TGL.run()