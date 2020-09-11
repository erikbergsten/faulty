use std::result;
use std::error::Error;
use std::net::{SocketAddr, IpAddr, Ipv4Addr};
mod net;
use net::{Message};
mod service;

public interface Service {
    fn id(&self) -> u16;
    fn handle_message(&mut self, message: &mut Message) -> bool;
}

HashMap<u16, Service>

//use std::sync::mpsc::{channel, Receiver, Sender};
//use std::time::Duration;
//use std::thread::{self};
//
type Result<T> = result::Result<T, Box<dyn Error>>;

fn p2h(port: u16) -> SocketAddr {
    SocketAddr::new(IpAddr::V4(Ipv4Addr::new(0, 0, 0, 0)), port)
}
fn p2l(port: u16) -> SocketAddr {
    SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), port)
}
fn main() {
    //let (message_write, message_queue) = channel();
    let out = net::start_send_thread();
    let (messages_out, messages_in) = net::start_recv_thread(4000).unwrap();
    let msg = Message::from_bytes("hello world".as_bytes());
    out.send((msg, p2l(4444)));
    //thread::sleep(Duration::new(5, 0));
    loop {
        let (mut msg, from) = messages_in.recv().unwrap();
        let protocol = msg.pop_u16();
        println!("Protocol #{}", protocol);
        println!("Forwarding: {:?} from {:?}", msg, from);
        out.send((msg, p2l(4444)));
    }
}
