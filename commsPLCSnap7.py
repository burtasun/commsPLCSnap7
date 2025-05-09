import numpy as np
import snap7
import time
import math
import snap7.util

class PLC2PC: #DB2
    idDB = 2
    startInsp = False           #bool 0.0 / 1 bit
    pulleyID = -1               #word 2.0 / 2 bytes 
_plc2pc = PLC2PC()

class PC2PLC: #DB3
    idDB = 3
    CVInspectionFinish = False  #bool 0.0 / 1 bit
    CVInspectionOK = True       #bool 0.1 / 1 bit
_pc2plc = PC2PLC()


#PLC configuration
ip = "192.168.0.2"
rack = 0
slot = 0
port = 102 #default value

#Initialize client instance and list for error handling
errorlist = []
client = snap7.client.Client()
stopRunning = False


def readBoolean(clienthandle:snap7.client.Client,db,startbyte,numbytes,byteaddress,bitaddress):
    data = clienthandle.db_read(db,startbyte,numbytes)
    boolout = snap7.util.get_bool(data,byteaddress,bitaddress)
    print(boolout)

ID_DB_PLC_2_PC = 1
ID_DB_PC_2_PLC = 3

#Connect to the PLC
try:
    client.connect(ip,rack,slot,port)
except RuntimeError:
    #Capture the exception
    list = ["No connection"]
else:
    dataWrite = client.db_read(ID_DB_PC_2_PLC,0,8)
    while stopRunning == False:
        try:
            #Read
            # data = client.db_read(ID_DB_PLC_2_PC,0,8)
            # databool = snap7.util.get_bool(data,0,0)
            # dataInt = snap7.util.get_int(data,2)
            # dataReal = snap7.util.get_real(data,4)
            # print (f'dataBool: {databool}')
            # print (f'dataInt: {dataInt}')
            # print (f'dataReal: {dataReal}')

            #Write
            # databool = True
            # dataInt = 3
            # dataReal = float(math.pi)
            # dataWrite = snap7.util.set_real(dataWrite,4,dataReal)
            # data = client.db_write(ID_DB_PC_2_PLC,0,dataWrite)
            # dataWrite = client.db_read(ID_DB_PC_2_PLC,0,8)
            # dataReal = snap7.util.get_real(dataWrite,4)
            # print (f'dataReal: {dataReal}')


        except Exception as e:
            print(f'Error {e}')
        time.sleep(1)