use std::net::{TcpListener, TcpStream, SocketAddr, IpAddr, Ipv4Addr};
use std::io::{Write, Read};
use std::result;
use std::error::Error;
use std::sync::mpsc::{channel, Receiver, Sender};
use std::thread::{self};

type Result<T> = result::Result<T, Box<dyn Error>>;
#[derive(Debug, Clone)]
pub struct Message(Vec<u8>);
impl Message {
    pub fn empty() -> Self {
        Message(Vec::new())
    }
    pub fn from_bytes(text: &[u8]) -> Self {
        Message(text.to_vec())
    }
    pub fn from_string(text: String) -> Self {
        Message(text.into_bytes())
    }
    pub fn push_u16(&mut self, value: u16) {
        let [b1, b2] = value.to_be_bytes();
        self.0.push(b1);
        self.0.push(b2);
    }
    pub fn pop_u16(&mut self) -> u16 {
        let b2 = self.0.pop().unwrap();
        let b1 = self.0.pop().unwrap();
        u16::from_be_bytes([b1, b2])
    }
}
pub fn listen(port: u16) -> Result<TcpListener> {
    let addr = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(0, 0, 0, 0)), port);
    let socket = TcpListener::bind(addr)?;
    Ok(socket)
}
pub fn receive(socket: &TcpListener) -> Result<(Message, SocketAddr)> {
    let mut buffer: [u8; 4096] = [0; 4096];
    let (mut stream, from) = socket.accept()?;
    let n = stream.read(&mut buffer)?;
    Ok((Message(buffer[..n].to_vec()), from))
}
pub fn send(data: &Message, to: SocketAddr) -> Result <()> {
    let mut stream = TcpStream::connect(to)?;
    stream.write(&data.0)?;
    Ok(())
}

pub fn start_send_thread() -> Sender<(Message, SocketAddr)> {
    let (sender, receiver) = channel();
    thread::spawn(move || {
        loop {
            let (message, address) = receiver.recv().unwrap();
            println!("Sending: {:?} to: {:?}", message, address);
            send(&message, address);
        }
    });
    sender
}
pub fn start_recv_thread(port: u16) -> Result<(Sender<(Message, SocketAddr)>,Receiver<(Message, SocketAddr)>)> {
    let (sender, receiver) = channel();
    let listen_socket = listen(port)?;
    let sender_clone = Sender::clone(&sender);
    thread::spawn(move || {
        loop {
            let (message, address) = receive(&listen_socket).unwrap();
            println!("Got: {:?} from: {:?}", message, address);
            sender_clone.send( (message, address) );
        }
    });
    Ok((sender, receiver))
}
