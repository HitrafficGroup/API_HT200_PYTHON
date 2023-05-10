import socket
import tramas

def buscar_ips():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
    port =13536
    while True:
        try:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            udp_socket.bind(('0.0.0.0', port))
            udp_socket.sendto(tramas.search_ips_frame, ('255.255.255.255', 161))
            data, sender = udp_socket.recvfrom(2048)
            print(sender)
            udp_socket.close()
            break
        except OSError:
            port += 1
buscar_ips()
