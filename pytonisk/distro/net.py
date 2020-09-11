import socket
import threading


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

class Vessel:
    def __init__(self, port):
        self.listen_socket = listen(port)
        self.dispatch = {}

    def subscribe(self, service):
        print("Subscribing on", service.id)
        self.dispatch[service.id] = service

    def handle_message(self, message):
        service_id = message.pop()
        try:
            service = self.dispatch[service_id]
        except KeyError:
            print("Unknown service:", service_id)
        
        service.handle_message(message)

    def send(self, service, message, to):
        message.push(service.id)
        send(message, to)

    def send_to_all(self, service, message, to):
        message.push(service.id)
        for address in to:
            try:
                # OBS! not self.send, actually calling the non-member function
                # send here (see above))
                send(message, address)
            except:
                pass



    def loop(self):
        while True:
            msg = receive(self.listen_socket)
            self.handle_message(msg)

class Broadcast:
    SEND = 0
    def __init__(self, vessel, service_id, hosts):
        self.id = service_id
        self.hosts = hosts
        self.dispatch = {}
        self.vessel = vessel
        vessel.subscribe(self)

    def subscribe(self, service):
        self.dispatch[service.id] = service

    def handle_message(self, message):
        print("Broadcast handling:", message)
        message_type = message.pop()
        print("Broadcast handling:", message)
        if message_type == Broadcast.SEND:
            service_id = message.pop()
            service = self.dispatch[service_id]
            service.handle_broadcast(message)

    def send(self, message):
        vessel.send_to_all(self, message, self.hosts)

