# echo-client.py
import socket
import numpy as np
import pandas as pd
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
ips_connected = []
def getBasicInfo():
    global rx_var
    if readPendingDatagrams(tramas.basic_info_frame,ip_address=ip_address):
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
def getDeviceInfo():
    global rx_var
    if readPendingDatagrams(tramas.device_info_frame,ip_address=ip_address):
        StrLen = 0
        temp = [0] * 64

        for i in range(0, 128, 2):
            if rx_var[i] != 0x00 or rx_var[i + 1] != 0x00:
                temp[StrLen] = (rx_var[i] << 8) | rx_var[i + 1]
                StrLen += 1
            else:
                break

        manufacturerInfoStr = ''.join([chr(temp[i]) for i in range(StrLen)])
        print(manufacturerInfoStr)
def getFases():
    global rx_var
    if readPendingDatagrams(tramas.fases_frame,ip_address=ip_address):
        PhaseSize = 32
        if 16 == rx_var[0] and rx_num == PhaseSize * 16 + 1:
            data_list = []
            for i in range(16):
                readpoint = PhaseSize * i + 1
                Number = rx_var[readpoint]
                Walk = rx_var[readpoint+1]
                PedestrianClear = rx_var[readpoint+2]
                MinimumGreen = rx_var[readpoint+3]
                Passage = rx_var[readpoint+4]
                Maximum1 = rx_var[readpoint+5]
                Maximum2 = rx_var[readpoint+6]
                YellowChange = rx_var[readpoint+7]
                RedClear = rx_var[readpoint+8]
                RedRevert = rx_var[readpoint+9]
                AddedInitial = rx_var[readpoint+10]
                MaximumInitial = rx_var[readpoint+11]
                TimeBeforeReduction = rx_var[readpoint+12]
                CarsBeforeReduction = rx_var[readpoint+13]
                TimeToReduce = rx_var[readpoint+14]
                ReduceBy = rx_var[readpoint+15]
                MinimumGap = rx_var[readpoint+16]
                DynamicMaxLimit = rx_var[readpoint+17]
                DynamicMaxStep = rx_var[readpoint+18]
                Startup = rx_var[readpoint+19]
                Ring = rx_var[readpoint+20]
                VehicleClear = rx_var[readpoint+21]
                Options = rx_var[readpoint+22]|(rx_var[readpoint+23]<<8)
                Concurrency =  rx_var[readpoint+24]|(rx_var[readpoint+25]<<8)|(rx_var[readpoint+26]<<16)|(rx_var[readpoint+27]<<24)
                ReleasePhase = rx_var[readpoint+28]|(rx_var[readpoint+29]<<8)|(rx_var[readpoint+30]<<16)|(rx_var[readpoint+31]<<24)
                
                #creamos un diccionario con los datos 
                data_fase = {
                    'number':Number,
                    'walk':Walk,
                    'pedestrianClear':PedestrianClear,
                    'minimumGreen':MinimumGreen,
                    'passage':Passage,
                    'maximun1':Maximum1,
                    'maximun2':Maximum2,
                    'yellowchange':YellowChange,
                    'redclear':RedClear,
                    'RedRevert':RedRevert,
                    'AddedInitial':AddedInitial,
                    'MaximunInitial':MaximumInitial,
                    'TimeBeforeReduction':TimeBeforeReduction,
                    'carsbeforereduction':CarsBeforeReduction,
                    'timetoreduce':TimeToReduce,
                    'reduceby':ReduceBy,
                    'minimungap':MinimumGap,
                    'dynamimaxlist':DynamicMaxLimit,
                    'dynamicmaxstep':DynamicMaxStep,
                    'startup':Startup,
                    'ring':Ring,
                    'vehicleclear':VehicleClear,
                    'options':Options,
                    'concurrency':Concurrency,
                    'releasephase':ReleasePhase
                }
                data_list.append(data_fase)
        
            df = pd.DataFrame(data_list)
            print(df)


def getSecuencia():
    global rx_var
    if readPendingDatagrams(tramas.secuence_frame,ip_address=ip_address):
        SequenceSize =(16 + 1) * 4 + 1
      
        if 16 == rx_var[0] and rx_num == SequenceSize * 16+ 1:
            readpoint = 1
            for i in range(1): 
                Num = rx_var[readpoint]
                readpoint +=1
                rings_secuency = []
                for i in range(4):
                    RingNum = rx_var[readpoint]
                    fases_ring = []
                    readpoint +=1
                    for i in range(16):
                        fase = rx_var[readpoint]
                        readpoint +=1
                        fase_data = ('paso_{calculo}'.format(calculo = i+1),fase)
                        fases_ring.append(fase_data)
                    fases_dict = dict((x, y) for x, y in fases_ring)
                    rings_secuency.append(fases_dict)
                df = pd.DataFrame(rings_secuency)
                print(df)
                    
'''
en el primer for colocar el valor de 16 para hacer referencia a las 16 posibles secuencias
'''
def getSplit():
    global rx_var
    if readPendingDatagrams(tramas.split_frame,ip_address=ip_address):
        SplitSize = 16 * 4 + 1;
        if 20 == rx_var[0] and rx_num == SplitSize * 20 + 1:
            readpoint = 1
            for i in range(1): #le dejamos en 1 para mostrar solo la tabla 1
                num = rx_var[readpoint]
                split_list = []
                readpoint +=1
                for i in range(16):
                    fase = rx_var[readpoint]
                    readpoint +=1
                    time = rx_var[readpoint]
                    readpoint +=1
                    mode = rx_var[readpoint]
                    readpoint +=1
                    coord = rx_var[readpoint]
                    readpoint +=1
                    split_dict = {
                        'fase':fase,
                        'tiempo':time,
                        'mode':mode,
                        'coord':coord
                    }
                    split_list.append(split_dict)
                df = pd.DataFrame(split_list)
                print(df)

def getAccion():
    global rx_var
    if readPendingDatagrams(tramas.action_frame,ip_address=ip_address):
        ActionSize = 4
        if 100 == rx_var[0] and rx_num == ActionSize * 100 + 1:
            readpoint = 1
            action_list = []
            for i in range(5):
                Num = rx_var[readpoint]
                readpoint +=1
                PatternNum = rx_var[readpoint]
                readpoint +=1
                Auxillary = rx_var[readpoint]
                readpoint +=1
                Special = rx_var[readpoint]
                readpoint +=1
                action_dict ={
                    'num':Num,
                    'patron': PatternNum,
                    'auxiliary':Auxillary,
                    'special':Special
                }
                action_list.append(action_dict)
            print(action_list)
            df = pd.DataFrame(action_list)
            print(df)
            pass
def getTime():
    global rx_var
    if readPendingDatagrams(tramas.time_frame,ip_address=ip_address):
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

def getPattern():
    global rx_var
    if readPendingDatagrams(tramas.pattern_frame,ip_address=ip_address):
        PatternSize = 7
        if 100 == rx_var[0] and rx_num == PatternSize * 100+ 1:
            pattern_list = []
            for i in range(16):
                readpoint = PatternSize * i + 1
                Number = rx_var[readpoint]
                CycleTime = rx_var[readpoint+1]|(rx_var[readpoint+2]<<8)
                OffsetTime = rx_var[readpoint+3]
                SplitNumber = rx_var[readpoint+4]
                SequenceNumber = rx_var[readpoint+5]
                WorkMode = rx_var[readpoint+6]
                pattern_dict = { 
                    'number':Number,
                    'cycletime':CycleTime,
                    'offsettime':OffsetTime,
                    'splitnumber':SplitNumber,
                    'sequencenumber':SequenceNumber,
                    'workmode':WorkMode,
                }
                pattern_list.append(pattern_dict)
            df = pd.DataFrame(pattern_list)
            print(df)
                
'''
la funcion de  obtencion de patrones se debe decodificar los valores del objeto para poder mapear
'''
def getScnedule():
    global rx_var
    if readPendingDatagrams(tramas.schedule_frame,ip_address=ip_address):
        schedule_size = 9
        schedule_list = []
        for i in range(5):
            readpoint = schedule_size*i +1
            number = rx_var[readpoint]
            month = rx_var[readpoint+1] | (rx_var[readpoint+2]<<8)
            day = rx_var[readpoint+3]
            date = rx_var[readpoint+4] |(rx_var[readpoint+5]<<8) |(rx_var[readpoint+6]<<16) |(rx_var[readpoint+7]<<24)
            day_plan = rx_var[readpoint+8];
            schedule_dict = {
                'number':number,
                'day_plan':day_plan,
                'month':month,
                'day':day,
                'date':date,
            }
            schedule_list.append(schedule_dict)
        df = pd.DataFrame(schedule_list)
        print(df)
'''
pendiente revisar el proceso de conversion de datos sobre todo para las variables de mes y fecha. , en la variable for se dejo por defecto
5 para no generar toda la tabla
'''

def getPlanes():
    global rx_var
    if readPendingDatagrams(tramas.plan_frame,ip_address=ip_address):
        plansize = 73
        if 16 == rx_var[0] and rx_num == (plansize * 16 + 1):
            readpoint = 1;
            for i in range(1): #le dejamos en 1 para obtener solo el primer plan
                plan = rx_var[readpoint]
                plan_list = []
                readpoint += 1
                for j in range(24):
                    num = j+1
                    hour = rx_var[readpoint]
                    readpoint += 1
                    minute = rx_var[readpoint]
                    readpoint += 1
                    accion = rx_var[readpoint]
                    readpoint += 1
                    plan_dict = {
                        'plan':plan,
                        'num':num,
                        'hour':hour,
                        'minute':minute,
                        'accion':accion
                    }
                    plan_list.append(plan_dict)
                df = pd.DataFrame(plan_list)
                print(df)
             

def readPendingDatagrams(frame,ip_address):
    global rx_var_formated 
    global udp_socket 
    global data
    global CheckSumCalc 
    global CheckSumReceive 
    global dataEndPoint 
    global port
    global rx_var
    global rx_num 
    global num
    global ips_connected
    try:
        udp_socket.sendto(frame, (ip_address, 161))
        data, sender = udp_socket.recvfrom(2048)
        ips_connected.append(sender)
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
        getPlanes()
        udp_socket.close()
        break
    except OSError:
        port += 1
