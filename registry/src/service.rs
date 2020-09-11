use crate::net::{self, Message};
use std::sync::mpsc::{Sender};
use std::net::{SocketAddr};



pub trait Service {
    fn id(&self) -> u16;
    fn handle_message(&mut self, message: &mut Message) -> bool;
}


struct Network {
    id: u16,
    out: Sender<(Message, SocketAddr)>
}
impl Service for Network {
    fn id(&self) -> u16 {
        self.id
    }
    fn handle_message(&mut self, _message: &mut Message) -> bool {
        // just promote the message to the proper service = do not touch
        true
    }
}
impl Network {
    fn send(&self, message: Message, to: SocketAddr){
        self.out.send((message, to));
    }
}

struct Broadcast {
    id: u16,
    hosts: Vec<SocketAddr>,
    net: Network
}
enum BroadcastMessage {
    // nothing right now...
}
impl Service for Broadcast {
    fn id(&self) -> u16 {
        self.id
    }
    fn handle_message(&mut self, _message: &mut Message) -> bool {
        true
    }
}
impl Broadcast {
    fn broadcast(&self, message: Message) {
        for host in self.hosts.iter() {
            self.net.send(message.clone(), *host);
        }
    }
}

