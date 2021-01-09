import sys
import platform

if platform.system() == 'Windows':
    from src.TGLBot import TGLBot
else:
    from src.TGLBot import TGLBot
    from src.pi_module import RaspPi

class TwitchGameOfLife():
    def __init__(self):
        self.tgl_bot = TGLBot()
        if platform.system() != 'Windows':
            self.pi = RaspPi()

    def run(self):
        command = self.pi.get_commands()

        while True:
            try:
                read = self.tgl_bot.irc.recv(1024).decode()
            except:
                read = ''

            if(elapsed_timer(oldtime)):
                oldtime = 
                viewers = self.tgl_bot.get_viewers()
                for each in viewers:
                    print(f'Add 10 points to {each}.')

            for line in read.split("\r\n"):
                if line == '':
                    continue
                elif 'PING' in line and 'PRIVMSG' not in line:
                    self.tgl_bot.irc.send("PONG tmi.twitch.tv\r\n".encode())
                    print("Sending PONG...")
                elif 'quit' in line:
                    sys.exit()
                else:
                    print(line)
                    user = self.tgl_bot.get_user(line)
                    msgg = self.tgl_bot.get_message(line)
                    print(f'{user}: {msgg}')
                    if msgg.upper() in command:
                        self.pi.command_list(msgg.upper())

if __name__ == "__main__":
    TGL = TwitchGameOfLife()
    TGL.tgl_bot.get_viewers()
    sys.exit()

    TGL.tgl_bot.join_chat()
    TGL.run()