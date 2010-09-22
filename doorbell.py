from PicoRendezvous import PicoRendezvous
from netgrowl import GrowlRegistrationPacket, GrowlNotificationPacket, GROWL_UDP_PORT
import serial
from socket import socket, AF_INET, SOCK_DGRAM
import sys

def send_growl_notification(password=None):
    reg = GrowlRegistrationPacket(password=password)
    reg.addNotification()
    
    notify = GrowlNotificationPacket(title="Ding-Dong",
                description="Someone is at the door",
                sticky=True, password=password)
    pr = PicoRendezvous()
    for ip in pr.query('_growl._tcp.local.'):
        addr = (ip, GROWL_UDP_PORT)
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(reg.payload(), addr)
        s.sendto(notify.payload(), addr)

def listen_on_serial_port(port):
    ser = serial.Serial(port, 9600, timeout=1)
    try:
        while True:
            line = ser.readline()
            if line is not None:
                line = line.strip()
            if line == 'DING DONG':
                send_growl_notification()
    finally:
        if ser:
            ser.close()
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please specify a serial port"
        sys.exit(-1)
    port = sys.argv[1]
    listen_on_serial_port(port)
