def getDevicesConnected():
    global ips_connected
    if readPendingDatagrams(tramas.search_ips_frame,ip_address='0.0.0.0'):
        print("ips_connected: ",ips_connected)
        pass