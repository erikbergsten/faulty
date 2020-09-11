import service.net as net

class Broadcaster(net.Service):
    def __init__(self, hosts):
        super().__init__(0)
        self.hosts = hosts

    def on_message(self, message):
        print("[Broadcast]: Received broadcast:", message)
        # do nothing at the moment, just forward up the stack
        self.deliver(message)


    def broadcast(self, message):
        print("[Broadcast]: Broadcasting:", message, \
              "to", len(self.hosts), "hosts.")
        # append service id to message
        message.append(self.id)
        for host in self.hosts:
            net.send(message, host)

class Chat(net.Service):
    def __init__(self, broadcaster):
        super().__init__(1)
        self.broadcaster = broadcaster

    def on_message(self, message):
        print("[Chat]: Received chat message:", message.decode('utf8'))
        # return false because we DO NOT want to forward
        return False
    def say(self, message):
        # add service id to the message
        message.append(self.id)
        # send invoke broadcaster
        self.broadcaster.broadcast(message)


if __name__ == '__main__':
    vessel = net.Vessel(4444)

    broadcaster = Broadcaster(net.local_hosts(2))
    vessel.register(broadcaster)

    chat = Chat(broadcaster)
    vessel.register(chat)




