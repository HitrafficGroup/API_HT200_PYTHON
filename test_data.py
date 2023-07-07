unit_data_1 = {
    "StartupFlash":6,
    "StartupAllRed":5,
    "AutomaticPedClear":2,
    "RedRevert":6,
    "BackupTime":2,
    "BackupTime2":2, #backup time al ser una variable de 16 bits se requiere descomponer en dos bytes para enviarle al controlador
    "FlowCycle":0,
    "FlashStatus":0,
    "Status":0,
    "GreenConflictDetectFlag":0,
    "RedGreenConflictDetectFlag":1,
    "RedFailedDetectFlag":0,
}
unit_data_2 = {
    "StartupFlash":5,
    "StartupAllRed":5,
    "AutomaticPedClear":2,
    "RedRevert":5,
    "BackupTime":3,
    "BackupTime2":1, #backup time al ser una variable de 16 bits se requiere descomponer en dos bytes para enviarle al controlador
    "FlowCycle":0,
    "FlashStatus":0,
    "Status":0,
    "GreenConflictDetectFlag":1,
    "RedGreenConflictDetectFlag":1,
    "RedFailedDetectFlag":0,
}

##datos para fases 
data_fases1 = [
    {
    "number":1,
    "walk":5,
    "Pedestrian Clear":6,
    "Minimun green":10,
    "passage":0,
    "maximum1":0,
    "maximum2":0,
    "yellowchange":3,
    "redclear":2,
    "redrevert":0,
    "addedinitial":0,
    "maximuninitial":0,
    "timebeforereduction":0,
    "carsbeforereduction":0,
    "timetoreduce":0,
    "reduceby":0,
    "minimumgap":0,
    "dynamicmaxlimit":0,
    "dynamicmaxstep":0,
    "startup":1,
    "ring":1,
    "vehicleclear":2,
    "options1":0,
    "options2":0,
    "concurrency1":255,
    "concurrency2":255,
    "concurrency3":0,
    "concurrency4":0,
    "releasephase1":0,
    "releasephase2":0,
    "releasephase3":0,
    "releasephase4":0,
},
    {
    "number":2,
    "walk":10,
    "Pedestrian Clear":6,
    "Minimun green":10,
    "passage":3,
    "maximum1":5,
    "maximum2":0,
    "yellowchange":3,
    "redclear":2,
    "redrevert":0,
    "addedinitial":0,
    "maximuninitial":0,
    "timebeforereduction":0,
    "carsbeforereduction":0,
    "timetoreduce":0,
    "reduceby":0,
    "minimumgap":0,
    "dynamicmaxlimit":0,
    "dynamicmaxstep":0,
    "startup":1,
    "ring":1,
    "vehicleclear":0,
    "options1":0,
    "options2":0,
    "concurrency1":255,
    "concurrency2":255,
    "concurrency3":0,
    "concurrency4":0,
    "releasephase1":0,
    "releasephase2":0,
    "releasephase3":0,
    "releasephase4":0,
},
{
    "number":3,
    "walk":5,
    "Pedestrian Clear":6,
    "Minimun green":6,
    "passage":3,
    "maximum1":30,
    "maximum2":40,
    "yellowchange":3,
    "redclear":2,
    "redrevert":0,
    "addedinitial":0,
    "maximuninitial":0,
    "timebeforereduction":0,
    "carsbeforereduction":0,
    "timetoreduce":0,
    "reduceby":0,
    "minimumgap":0,
    "dynamicmaxlimit":0,
    "dynamicmaxstep":0,
    "startup":1,
    "ring":1,
    "vehicleclear":0,
    "options1":0,
    "options2":0,
    "concurrency1":255,
    "concurrency2":255,
    "concurrency3":0,
    "concurrency4":0,
    "releasephase1":0,
    "releasephase2":0,
    "releasephase3":0,
    "releasephase4":0,
},

]

def setFases(self,data):
        gbtx = bytearray(25)
        #trama normal para escritura
        gbtx[0]=192
        gbtx[1]=32
        gbtx[2]=32
        gbtx[3]=16
        gbtx[5]= 1
        gbtx[6]= 1
        gbtx[7]= 0
        gbtx[10]= 1
        #trama que especifica que se van a grabar los datos en unit 
        gbtx[4] = 3
        gbtx[8] = 129
        gbtx[9] = 7
        gbtx[11] = 16
        temp_var = []
        num = 12;
        temp_num = 512
        for key in data:
            value = data.get(key)
            temp_var.append(value) #coegmos los datos de la api y los convertimos en una lista para posteriormente formatear y crear la trama udp
        for i in range(temp_num):
            if temp_var[i] == 0xC0:
                gbtx[num] = 0xDB
                num +=1
                gbtx[num] = 0xDC
                num +=1
            elif temp_var[i] == 0xDB:
                gbtx[num] = 0xDB
                num +=1
                gbtx[num] = 0xDD
                num +=1
            else:
                gbtx[num] = temp_var[i]
                num +=1
        CheckSumCalc = 0
        for i in range(1,num):
            CheckSumCalc += gbtx[i]
        CheckSumCalc = (CheckSumCalc % 256)
        print(CheckSumCalc)

        if CheckSumCalc == 0xC0:
            gbtx[num]= 0xDB
            num +=1
            gbtx[num]= 0xDC
            num +=1
        elif CheckSumCalc == 0xDB:
            gbtx[num]= 0xDB
            num +=1
            gbtx[num]= 0xDD
            num +=1
        else:
            gbtx[num]= CheckSumCalc
            num +=1;
        gbtx[num]= 192 #frame tail
        self.__udpsocket.sendto(gbtx, (self.ip_target,self.__port))
        data_received, sender = self.__udpsocket.recvfrom(2048)
        trama_respuesta = list(data_received)
        print(trama_respuesta)
        if trama_respuesta[8] == 132:
            return True
        else:
            return False
    
    

