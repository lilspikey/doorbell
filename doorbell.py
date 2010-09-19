from PicoRendezvous import PicoRendezvous
from netgrowl import GrowlRegistrationPacket, GrowlNotificationPacket, GROWL_UDP_PORT
from socket import socket, AF_INET, SOCK_DGRAM

def send_grow_notification(password=None):
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


if __name__ == '__main__':
    # test we can send growl notifications
    # to all net growl services on network
    send_grow_notification()
