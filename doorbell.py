from PicoRendezvous import PicoRendezvous
from netgrowl import GrowlRegistrationPacket, GrowlNotificationPacket, GROWL_UDP_PORT
import serial
from socket import socket, AF_INET, SOCK_DGRAM
import sys
import time

class Network(object):
    
    def __init__(self):
        self.growl_ips = []
        self.gntp_ips = []
        self.password = None
    
    def _rendezvous(self, service):
        pr = PicoRendezvous()
        pr.replies = []
        return pr.query(service)
    
    def find(self):
        self.growl_ips = self._rendezvous('_growl._tcp.local.')
        self.gntp_ips  = self._rendezvous('_gntp._tcp.local.')
    
    def start(self):
        import threading
        t = threading.Thread(target=self._run)
        t.setDaemon(True)
        t.start()
    
    def _run(self):
        while True:
            self.find()
            time.sleep(30.0)

    def send_growl_notification(self):
        growl_ips = self.growl_ips
        
        reg = GrowlRegistrationPacket(password=self.password)
        reg.addNotification()
    
        notify = GrowlNotificationPacket(title="Ding-Dong",
                    description="Someone is at the door",
                    sticky=True, password=self.password)
        for ip in growl_ips:
            addr = (ip, GROWL_UDP_PORT)
            s = socket(AF_INET, SOCK_DGRAM)
            s.sendto(reg.payload(), addr)
            s.sendto(notify.payload(), addr)

    def send_gntp_notification(self):
        growl_ips = self.growl_ips
        gntp_ips  = self.gntp_ips
        
        # don't send to gntp if we can use growl
        gntp_ips = [ip for ip in gntp_ips if (ip not in growl_ips)]
        
        for ip in gntp_ips:
            print 'gntp to: ', ip
    
    def send_notification(self):
        '''
        send notification over the network
        '''
        self.send_growl_notification()
        self.send_gntp_notification()

def listen_on_serial_port(port, network):
    ser = serial.Serial(port, 9600, timeout=1)
    try:
        while True:
            line = ser.readline()
            if line is not None:
                line = line.strip()
            if line == 'DING DONG':
                network.send_notification()
    finally:
        if ser:
            ser.close()
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please specify a serial port"
        sys.exit(-1)
    port = sys.argv[1]
    network = Network()
    network.start()
    listen_on_serial_port(port, network)
    #for i in range(10):
    #    time.sleep(4)
    #    network.send_notification()
    
