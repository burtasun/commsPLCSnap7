import numpy as np
import snap7
import time
import math
import snap7.util
from bitarray.util import int2ba


ID_DB_PC_2_PLC = 1
ID_DB_PLC_2_PC = 2

class PLC2PC:
    StartInspection = False     #bool 0.0 / 1 bit
_plc2pc = PLC2PC()

class PC2PLC:
    CVInspectionFinish = False  #bool 0.0 / 1 bit
    CVInspectionOK = False      #bool 0.1 / 1 bit
    IAInspectionFinish = False  #bool 0.2 / 1 bit
    IAInspectionOK = False      #bool 0.3 / 1 bit
_pc2plc = PC2PLC()


#PLC configuration
ip = "192.168.0.1"
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


#Connect to the PLC
try:
    client.connect(ip,rack,slot,port)
except RuntimeError:
    #Capture the exception
    list = ["No connection"]
else:
    dataWrite = client.db_read(ID_DB_PC_2_PLC,0,1)
    counter = 0
    while stopRunning == False:
        try:
            print(snap7.util.get_bool(dataWrite,0,0))
            client.db_read(ID_DB_PLC_2_PC,0,1)
            dataPLC2PC = client.db_read(ID_DB_PLC_2_PC,0,1)
            _plc2pc.StartInspection = snap7.util.get_bool(dataPLC2PC,0,0)
            print (f'_plc2pc.StartInspection: {_plc2pc.StartInspection}')

            bitarr = int2ba(counter,4)
            print(f'counter: {counter},   {bitarr}')
            _pc2plc.CVInspectionFinish=int(bitarr[0])
            _pc2plc.CVInspectionOK=int(bitarr[1])
            _pc2plc.IAInspectionFinish=int(bitarr[2])
            _pc2plc.IAInspectionOK=int(bitarr[3])

            #Write
            dataWrite = snap7.util.set_bool(dataWrite,0,0,_pc2plc.CVInspectionFinish)
            dataWrite = snap7.util.set_bool(dataWrite,0,1,_pc2plc.CVInspectionOK)
            dataWrite = snap7.util.set_bool(dataWrite,0,2,_pc2plc.IAInspectionFinish)
            dataWrite = snap7.util.set_bool(dataWrite,0,3,_pc2plc.IAInspectionOK)
            data = client.db_write(ID_DB_PC_2_PLC,0,dataWrite)

            
        except Exception as e:
            print(f'Error {e}')

        counter+=1
        counter = counter%16
        time.sleep(1)
        # break