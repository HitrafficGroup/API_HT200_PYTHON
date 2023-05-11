import socket
import time
import tramas
import pandas as pd
class MySocket:
    def __init__(self, ip_target):
        self.rx_var_formated = []
        self.__rx_var = bytearray(2048)
        self.__rx_num = 0
        self.__num = 11
        self.__ips_connected = []
        self.__port = 161
        self.ip_target = ip_target
        self.__udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect()
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def __connect(self):
        port = 13536
        while True:
            try:
                self.__udpsocket.bind(('0.0.0.0', port))
                break
            except OSError:
                port += 1
    def disconnect(self):
        self.__udpsocket.close()
        print('nos desconectamos !')
    def readPendingDatagrams(self,frame,ip_address):
        CheckSumCalc = 0
        CheckSumReceive = 0
        data_received = bytearray()
        try:
            self.__udpsocket.sendto(frame, (ip_address,self.__port))
            data_received, sender = self.__udpsocket.recvfrom(2048)
            self.__ips_connected.append(sender)
            array_data_received = list(data_received) #convertimos en una lista de enteros los valores recibidos por udp
            size = len(array_data_received)

            if array_data_received[size-3] == 0xDB and array_data_received[size-2] == 0xDC:
                dataEndPoint = size-4;
                CheckSumReceive = 0xC0;
                for i in range(1, dataEndPoint+1):
                    CheckSumCalc += array_data_received[i]
            elif array_data_received[size-3] == 0xDB and array_data_received[size-2] == 0xDD:
                dataEndPoint = size-4
                CheckSumReceive = 0xDB
                for i in range(1, dataEndPoint+1):
                    CheckSumCalc += array_data_received[i]
            else:
                dataEndPoint = size-3;
                CheckSumReceive = array_data_received[size-2]
                for i in range(1, dataEndPoint+1):
                    CheckSumCalc += array_data_received[i]
            #CheckSumCalc = np.uint8(CheckSumCalc)
            #CheckSumReceive = np.uint8(CheckSumReceive)
            ''''
            pendiente revisar la funcion checksum para la verificacion de valores. se podria implementar la libreria ctypes
            para mejorar la conversion de los datos.
            '''
            self.__rx_num = 0
            self.__num = 11
            while self.__num <= dataEndPoint:
                if array_data_received[self.__num] == 0xDB and array_data_received[self.__num+1] == 0xDC:
                    self.__rx_var[self.__rx_num] = 0xC0
                    self.__rx_num += 1
                    self.__num += 2
                elif array_data_received[self.__num] == 0xDB and array_data_received[self.__num+1] == 0xDD:
                    self.__rx_var[self.__rx_num] = 0xDB
                    self.__rx_num += 1
                    self.__num += 2
                else:
                    self.__rx_var[self.__rx_num] = array_data_received[self.__num]
                    self.__rx_num += 1
                    self.__num += 1
            return True
        except OSError:
            print("algo ocurrio mal")
            self.disconnect()
            return False
    def getTime(self):
        self.__rx_var
        if self.readPendingDatagrams(tramas.time_frame,ip_address=self.ip_target):
            second = self.__rx_var[0]//16*10 + self.__rx_var[0]%16 # segundo
            minute = self.__rx_var[1]//16*10 + self.__rx_var[1]%16 # minuto
            hour = self.__rx_var[2]//16*10 + self.__rx_var[2]%16 # hora
            week = self.__rx_var[3] # semana
            date = self.__rx_var[4]//16*10 + self.__rx_var[4]%16 # día del mes
            month = self.__rx_var[5]//16*10 + self.__rx_var[5]%16 # mes
            year = 2000 + self.__rx_var[6]//16*10 + self.__rx_var[6]%16 # año
            time_controler = {
            "segundos":second,
            "minutos":minute,
            "hour":hour,
            "semana":week,
            "dia":date,
            "mes":month,
            "year":year,
            }
            print(time_controler)
    def getFases(self):
        rx_var = self.__rx_var
        print('solicitando fases ....')
        if self.readPendingDatagrams(tramas.fases_frame,ip_address=self.ip_target):
            PhaseSize = 32
            if 16 == rx_var[0] and self.__rx_num == PhaseSize * 16 + 1:
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
    
    def getSecuencia(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.secuence_frame,ip_address=self.ip_target):
            SequenceSize =(16 + 1) * 4 + 1
        
            if 16 == rx_var[0] and self.__rx_num == SequenceSize * 16+ 1:
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
    def getSplit(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.split_frame,ip_address=self.ip_target):
            SplitSize = 16 * 4 + 1;
            if 20 == rx_var[0] and self.__rx_num == SplitSize * 20 + 1:
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

    def getPattern(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.pattern_frame,ip_address=self.ip_target):
            PatternSize = 7
            if 100 == rx_var[0] and self.__rx_num == PatternSize * 100+ 1:
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

    def getAccion(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.action_frame,ip_address=self.ip_target):
            ActionSize = 4
            if 100 == rx_var[0] and self.__rx_num == ActionSize * 100 + 1:
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
                df = pd.DataFrame(action_list)
                print(df)
    
    def getPlanes(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.plan_frame,ip_address=self.ip_target):
            plansize = 73
            if 16 == rx_var[0] and self.__rx_num == (plansize * 16 + 1):
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

    def getScnedule(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.schedule_frame,ip_address=self.ip_target):
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
    def getDeviceInfo(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.device_info_frame,ip_address=self.ip_target):
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

    def getBasicInfo(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.basic_info_frame,ip_address=self.ip_target):
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
            basicinfo_dict = {
            "mac_target: ":mac_addr,
            "ip_target: ":ip_server,
            "puerto_server: ":port_server,
            "zona_horaria: ":zona_horaria,
            "numero_dispositivo: ":tscNum
            }
            print(basicinfo_dict)

    def getUnit(self):
        rx_var = self.__rx_var
        if self.readPendingDatagrams(tramas.unit_frame,ip_address=self.ip_target):
            if self.__rx_num == 12:
                StartupFlash = rx_var[0]
                StartupAllRed = rx_var[1]
                AutomaticPedClear = rx_var[2]
                RedRevert = rx_var[3]
                BackupTime = rx_var[4]|(rx_var[5]<<8)
                FlowCycle = rx_var[6]
                FlashStatus = rx_var[7]
                Status = rx_var[8]
                GreenConflictDetectFlag = rx_var[9]
                RedGreenConflictDetectFlag = rx_var[10]
                RedFailedDetectFlag = rx_var[11]

                unit_dict =  {
                    "StartupFlash":StartupFlash,
                    "StartupAllRed":StartupAllRed,
                    "AutomaticPedClear":AutomaticPedClear,
                    "RedRevert":RedRevert,
                    "BackupTime":BackupTime,
                    "FlowCycle":FlowCycle,
                    "FlashStatus":FlashStatus,
                    "Status":Status,
                    "GreenConflictDetectFlag":GreenConflictDetectFlag,
                    "RedGreenConflictDetectFlag":RedGreenConflictDetectFlag,
                     "RedFailedDetectFlag":RedFailedDetectFlag
                }
                print(unit_dict)
    def getChannel(self):
        rx_var = self.__rx_var
        channel_list = []
        if self.readPendingDatagrams(tramas.chanel_frame,ip_address=self.ip_target):
            ChannelSize = 8
            if 16 == rx_var[0] and self.__rx_num == ChannelSize * 16 + 1 :
                readpoint = 1
                for i in range(16):
                    Num = rx_var[readpoint]
                    readpoint +=1
                    ControlSource = rx_var[readpoint]
                    readpoint +=1
                    ControlType = rx_var[readpoint];
                    readpoint +=1
                    Flash = rx_var[readpoint]
                    readpoint +=1
                    Dim = rx_var[readpoint]
                    readpoint +=1
                    Position = rx_var[readpoint]
                    readpoint +=1
                    Direction = rx_var[readpoint]
                    readpoint +=1
                    CountdownID = rx_var[readpoint]
                    readpoint +=1
                    channel_dict = {
                        "Num":Num,
                        "ControlSource":ControlSource,
                        "ControlType":ControlType,
                        "Flash":Flash,
                        "Position":Position,
                        "Direction":Direction,
                        "CountdownID":CountdownID,
                    }
                    channel_list.append(channel_dict)
                df = pd.DataFrame(channel_list)
                print(df)


































