# echo-client.py
import socket
import numpy as np
import tramas
import time
#variables de inicio
rx_var_formated = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_address = "192.168.1.122"
data = bytearray(2048)
CheckSumCalc = 0
CheckSumReceive = 0
dataEndPoint = 0
port =13536
rx_var = bytearray(2048)
rx_num = 0
num = 11
def getDeviceInfo():
    global rx_var
    if readPendingDatagrams(tramas.basic_info_frame):
        # StrLen = 0
        # temp = np.empty(64)
        # i = 0
        # while i < 128:
        #     if rx_var[i] != 0x00 or rx_var[i+1] != 0x00:
        #         temp[StrLen] = (rx_var[i]<<8)|rx_var[i+1]
        #         StrLen += 1
        #         i += 2
        #     else:
        #         break 
        #InterInfoStr = ''.join([chr(temp[i]) for i in range(StrLen)])
        mac_addr = bytearray([rx_var[i] for i in range(142, 148)])
        mac_addr = mac_addr.hex().upper()
        mac_addr = ':'.join([mac_addr[i:i+2] for i in range(0, 12, 2)])
        ip_server = "{oct_1}.{oct_2}.{oct_3}.{oct_4}".format(oct_1 = rx_var[148],oct_2 = rx_var[149],oct_3 = rx_var[150],oct_4 = rx_var[151])
        port_server = "{port_s}".format(port_s = (rx_var[152]<<8)|rx_var[153])
        zona_horaria = ((rx_var[156]<<16)|(rx_var[157]<<8)|rx_var[158])/3600.0;
        tscNum = (rx_var[159]<<24)|(rx_var[160]<<16)|(rx_var[161]<<8)|rx_var[162]
        print("mac_target: ",mac_addr)
        print("ip_target: ",ip_server)
        print("puerto_server: ",port_server)
        print("zona_horaria: ",zona_horaria)
        print("numero_dispositivo: ",tscNum)

def getTime():
    global rx_var
    if readPendingDatagrams(tramas.time_frame):
        second = rx_var[0]//16*10 + rx_var[0]%16 # segundo
        minute = rx_var[1]//16*10 + rx_var[1]%16 # minuto
        hour = rx_var[2]//16*10 + rx_var[2]%16 # hora
        week = rx_var[3] # semana
        date = rx_var[4]//16*10 + rx_var[4]%16 # día del mes
        month = rx_var[5]//16*10 + rx_var[5]%16 # mes
        year = 2000 + rx_var[6]//16*10 + rx_var[6]%16 # año
        print("segundos: ",second)
        print("minutos: ",minute)
        print("hour: ",hour)
        print("semana: ",week)
        print("dia: ",date)
        print("mes: ",month)
        print("year: ",year)
def readPendingDatagrams(frame):
    global rx_var_formated 
    global udp_socket 
    global ip_address 
    global data
    global CheckSumCalc 
    global CheckSumReceive 
    global dataEndPoint 
    global port
    global rx_var
    global rx_num 
    global num
    try:
        udp_socket.sendto(frame, (ip_address, 161))
        data, sender = udp_socket.recvfrom(2048)
        array = list(data)
        size = len(array)

        if array[size-3] == 0xDB and array[size-2] == 0xDC:
            dataEndPoint = size-4;
            CheckSumReceive = 0xC0;
            for i in range(1, dataEndPoint+1):
                CheckSumCalc += array[i]
        elif array[size-3] == 0xDB and array[size-2] == 0xDD:
            dataEndPoint = size-4
            CheckSumReceive = 0xDB
            for i in range(1, dataEndPoint+1):
                CheckSumCalc += array[i]
        else:
            dataEndPoint = size-3;
            CheckSumReceive = array[size-2]
            for i in range(1, dataEndPoint+1):
                CheckSumCalc += array[i]
        #CheckSumCalc = np.uint8(CheckSumCalc)
        #CheckSumReceive = np.uint8(CheckSumReceive)
        ''''
        pendiente revisar la funcion checksum para la verificacion de valores. se podria implementar la libreria ctypes
        para mejorar la conversion de los datos.
        '''
        while num <= dataEndPoint:
            if array[num] == 0xDB and array[num+1] == 0xDC:
                rx_var[rx_num] = 0xC0
                rx_num += 1
                num += 2
            elif array[num] == 0xDB and array[num+1] == 0xDD:
                rx_var[rx_num] = 0xDB
                rx_num += 1
                num += 2
            else:
                rx_var[rx_num] = array[num]
                rx_num += 1
                num += 1
        rx_var_formated = list(rx_var)
        return True
    
    except OSError:
        print("algo ocurrio mal")
        return False

while True:
    try:
        udp_socket.bind(('0.0.0.0', port))
        getTime()
        time.sleep(5)
        getDeviceInfo()
        udp_socket.close()
        break
    except OSError:
        port += 1
