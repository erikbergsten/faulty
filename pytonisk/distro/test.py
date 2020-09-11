import distro.net as net

class Chat:
    def __init__(self, broadcast, service_id):
        self.id = service_id
        self.broadcast = broadcast
        broadcast.subscribe(self)

    def handle_broadcast(self, message):
        print("Got chat message:", message)

    def say(self, message):
        self.broadcast.send(message)

vessel = net.Vessel(4444)
broadcast = net.Broadcast(vessel, 1, net.local_hosts(2))
chat = Chat(broadcast, 2)
vessel.loop()
