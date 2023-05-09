# echo-client.py
import socket
import numpy as np

#tiempo
time_frame = bytearray()
time_frame.append(192)  #0
time_frame.append(32)  #1
time_frame.append(32) #2
time_frame.append(16) #3
time_frame.append(2) #4
time_frame.append(1) #5
time_frame.append(1) #6
time_frame.append(1) #7
time_frame.append(128) #8
time_frame.append(5) #9
time_frame.append(1) #10
time_frame.append(219) #11
time_frame.append(221) #12
time_frame.append(192) #13
#basic_info 
basic_info_frame = bytearray()
basic_info_frame.append(192)  #0
basic_info_frame.append(32)  #1
basic_info_frame.append(32) #2
basic_info_frame.append(16) #3
basic_info_frame.append(2) #4
basic_info_frame.append(1) #5
basic_info_frame.append(1) #6
basic_info_frame.append(1) #7
basic_info_frame.append(128) #8
basic_info_frame.append(189) #9
basic_info_frame.append(1) #10
basic_info_frame.append(147) #11
basic_info_frame.append(192) #12
#basic_info_frame.append(80) #13
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

def converTime():
    global rx_var
    if readPendingDatagrams():
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
def readPendingDatagrams():
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
        udp_socket.sendto(time_frame, (ip_address, 161))
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
        converTime()
        udp_socket.close()
        break
    except OSError:
        port += 1
