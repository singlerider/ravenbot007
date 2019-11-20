# encoding=utf8
import re
import socket
import sys
import time

threshold = 5 * 60  # five minutes, make this whatever you want


class IRC:

    def __init__(self, config):
        self.sock = {}
        self.config = config
        self.ircBuffer = {}
        self.ircBuffer["whisper"] = ""
        self.ircBuffer["chat"] = ""
        self.connect("whisper")
        self.connect("chat")

    def nextMessage(self, kind):
        if "\r\n" not in self.ircBuffer[kind]:
            read = self.sock[kind].recv(1024)
            if not read:
                print("Connection was lost")
                self.sock[kind].shutdown
                self.sock[kind].close
                self.connect(kind)
            else:
                self.ircBuffer[kind] += read.decode()

        line, self.ircBuffer[kind] = self.ircBuffer[kind].split("\r\n", 1)

        if line is not None:
            if line.startswith("PING"):
                line = line.replace('PING', 'PONG')
                self.sock[kind].send(f"{line}\r\n".encode())
            return line

    def check_for_message(self, data):
        if re.match(r"^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$", data):
            return True

    def check_for_chatroom_message(self, data):
        if re.match(r"^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #chatrooms:([a-zA-Z0-9_]+):([a-zA-Z0-9\-]+) :.+$", data):
            return True
        # :singlerider!singlerider@singlerider.tmi.twitch.tv PRIVMSG #chatrooms:54411072:d7b8f612-f2ed-4c7f-815f-095989a05fde :Lorenzo is in the buiding

    def check_for_whisper(self, data):
        if re.match(r"^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) WHISPER [a-zA-Z0-9_]+ :.+$", data):
            return True

    def check_for_join(self, data):
        if re.match(r"^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) JOIN #[a-zA-Z0-9_]", data):
            return True

    def check_for_part(self, data):
        if re.match(r"^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PART #[a-zA-Z0-9_]", data):
            return True

    def check_is_command(self, message, valid_commands):
        for command in valid_commands:
            if command == message:
                return True

    def check_for_connected(self, data):
        if re.match(r"^:.+ 001 .+ :connected to TMI$", data):
            return True

    def get_logged_in_users(self, data):
        if data.find("353"):
            return True

    def check_for_ping(self, data, kind):
        last_ping = time.time()
        if data.find("PING") != -1:
            self.sock[kind].send("PONG " + data.split()[1] + "\r\n")
            last_ping = time.time()
        if (time.time() - last_ping) > threshold:
            sys.exit()

    def get_message(self, data):
        return re.match(r"^:(?P<username>.*?)!.*?PRIVMSG (?P<channel>.*?) :(?P<message>.*)", data).groupdict()

    def get_chatroom_message(self, data):
        return re.match(r"^:(?P<username>.*?)!.*?PRIVMSG #chatrooms:(?P<channel_id>.*?):(?P<chatroom_uid>.*?) :(?P<message>.*)", data).groupdict()

    def get_whisper(self, data):
        return re.match(r"^:(?P<username>.*?)!.*?WHISPER (?P<channel>.*?) :(?P<message>.*)", data).groupdict()

    def check_login_status(self, data):
        if re.match(r"^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$", data):
            return False
        else:
            return True

    def send_message(self, channel, message):
        if not message:
            return

        if isinstance(message, str):
            self.sock["chat"].send(f"PRIVMSG {channel} :{message}\r\n".encode())

        if type(message) == list:
            for line in message.decode("utf8"):
                self.send_message(channel, line)

    def send_chatroom_message(self, channel_id, chatroom_uid, message):
        if not message:
            return

        if isinstance(message, str):
            self.sock["chat"].send(":{0}!{0}@{0}.tmi.twitch.tv PRIVMSG #chatrooms:{1}:{2} :{3}\r\n".format(
                self.config["username"], channel_id, chatroom_uid, message))

        if type(message) == list:
            for line in message.decode("utf8"):
                self.send_message(channel_id, chatroom_uid, line)

    def send_whisper(self, recipient, message):
        if not message:
            return

        if isinstance(message, str):
            self.sock["whisper"].send(
                f"PRIVMSG #jtv :/w {recipient} {message}\r\n".encode())

        if type(message) == list:
            for line in message.decode("utf8"):
                self.send_message(recipient, str(time.time()))

    def connect(self, kind):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        sock.settimeout(10)
        port = 6667
        if kind == "whisper":
            server = "irc.chat.twitch.tv"
            print("Connecting to {0}:{1}".format(server, port))
            self.connect_phases(sock, server, port, kind)
            self.join_channels([], kind)
        elif kind == "chat":
            server = "irc.chat.twitch.tv"
            print("Connecting to {0}:{1}".format(server, port))
            self.connect_phases(sock, server, port, kind)
            self.join_channels(self.config["channels"], kind)

        sock.settimeout(None)

    def connect_phases(self, sock, server, port, kind):
        sock.connect((server, port))
        print("Sending Username " + self.config["username"])
        sock.send(f"USER {self.config['username']}\r\n".encode())
        print(f"USER {self.config['username']}\r\n")
        sock.send(f"PASS {self.config['oauth_password']}\r\n".encode())
        print(f"PASS {self.config['oauth_password']}\r\n")
        sock.send(f"NICK {self.config['username']}\r\n".encode())
        print(f"NICK {self.config['username']}\r\n")
        self.sock[kind] = sock
        self.nextMessage(kind)  # login message
        if kind == "chat":
            if "376" not in self.nextMessage(kind):
                pass

    def channels_to_string(self, channel_list):
        return ",".join(channel_list)

    def join_chatroom(self, channel, room):
        join_str = "{0}:{1}".format(room[0], room[1])
        self.sock["chat"].send("JOIN #chatrooms:{0}\r\n".format(join_str))
        print(f"Joined chatroom: {channel}:{join_str}")

    def join_channels(self, channels, kind):
        if kind == "chat":
            channels_str = self.channels_to_string(channels)
            print(f"Joining channels {channels_str}.")
            self.sock[kind].send(f"JOIN {channels_str}\r\n".encode())
            for channel in channels:
                if "rooms" in self.config:
                    if "#{0}".format(channel.lstrip("#")) in self.config["rooms"]:
                        for room in self.config["rooms"][channel]:
                            self.join_chatroom(channel, room)
        elif kind == "whisper":
            print("Joining whisper server")
            self.sock[kind].send("CAP REQ :twitch.tv/commands\r\n".encode())
        print("Joined channels.")

    def leave_channels(self, channels, kind):
        print("Leaving channels {channels},".encode())
        if kind == "chat":
            self.sock[kind].send(f"PART {channels}\r\n".encode())
        print("Left channels.")
