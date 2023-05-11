import socket

class MySocket:
    def __init__(self, port, ip_target):
        self.port = port
        self.ip_target = ip_target
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        