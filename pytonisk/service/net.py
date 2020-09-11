import socket
import threading
import queue


def listen(port):
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(('', port))
    listen_socket.listen(5)
    return listen_socket

def receive(listen_socket):
    (stream, _from) = listen_socket.accept()
    msg = stream.recv(4096)
    return bytearray(msg).rstrip()

def send(message, to):
    stream = socket.create_connection(to)
    stream.send(message)

def local_hosts(n):
    return [('localhost', 4000+i) for i in range(n)]


class Service:
    def __init__(self, id):
        self.id = id

    def on_message(self, message):
        print("[Service]: BASE MESSAGE HANDLER INVOKED FOR:", message)
        return False


class Vessel:
    def do_listen(self):
        while self.running:
            msg = receive(self.listen_socket)
            self.queue.put(msg)

    def start_listener(self):
        self.listen_thread = threading.Thread(target=self.do_listen, \
                                              args=())
        self.listen_thread.start()

    def __init__(self, port):
        self.listen_socket = listen(port)
        self.queue = queue.Queue()
        self.running = True
        self.services = {}

    def register(self, s_id, service):
        self.services[s_id] = service

    def start(self):
        self.start_listener()
        self.loop()

    def handle_message(self, msg):
        handling = True
        while handling:
            try:
                service_id = msg.pop()
                service = self.services[service_id]
                handling = service.on_message(msg)
            except IndexError:
                print("Popping from an empty message!")
            except KeyError:
                print("No such service:", service_id)
                print("Registered services:", self.services)

    def loop(self):
        while self.running:
            msg = self.queue.get()
            print("Got message:", msg)
            self.handle_message(msg)

