#####################################################################################################
# Program test environment
# Pyhone version:3.4.1
# Firmware version:2.8.28
# Dependent files(MacOSX):libGinkgo_Driver.dylib,libusb-0.1.4.dylib,libusb-1.0.0.dylib,ControlI2C.py
# Dependent files(Windows):Ginkgo_Driver.dll,ControlI2C.py
# Dependent files(Linux):libGinkgo_Driver.so,libusb-1.0.so,ControlI2C.py
#####################################################################################################
from ctypes import *
from time import sleep
# import USB-I2C module
import ControlI2C

# Scan device
nRet = ControlI2C.VII_ScanDevice(1)
if(nRet <= 0):
    print("No device connect!")
    exit()
else:
    print("Connected device number is:"+repr(nRet))

# Open device
nRet = ControlI2C.VII_OpenDevice(ControlI2C.VII_USBI2C,0,0)
if(nRet != ControlI2C.ERR_SUCCESS):
    print("Open device error!")
    exit()
else:
    print("Open device success!")
# Initialize device
I2C_InitConfig = ControlI2C.VII_INIT_CONFIG()
# Master mode
I2C_InitConfig.MasterMode = ControlI2C.VII_MASTER
# Hardware control
I2C_InitConfig.ControlMode = ControlI2C.VII_HCTL_MODE
# 7-bit address mode
I2C_InitConfig.AddrType = ControlI2C.VII_ADDR_7BIT
# Sub address width->1byte
I2C_InitConfig.SubAddrWidth = ControlI2C.VII_SUB_ADDR_NONE
# Clock speed (in Hz)
I2C_InitConfig.ClockSpeed = 100000
nRet = ControlI2C.VII_InitI2C(ControlI2C.VII_USBI2C,0,0,byref(I2C_InitConfig))
if(nRet != ControlI2C.ERR_SUCCESS):
    print("Initialize device error!")
    exit()
else:
    print("Initialize device success!")

# Send command
WriteData = (c_ubyte * 8)()
WriteData[0] = 0x01
nRet = ControlI2C.VII_WriteBytes(ControlI2C.VII_USBI2C,0,0,0x46,0x00,byref(WriteData),1)
if(nRet != ControlI2C.ERR_SUCCESS):
    print("Write data error! %d"%nRet)
    exit()
else:
    print("Write data success!")
# Send command
WriteData = (c_ubyte * 8)()
WriteData[0] = 0x10
nRet = ControlI2C.VII_WriteBytes(ControlI2C.VII_USBI2C,0,0,0x46,0x00,byref(WriteData),1)
if(nRet != ControlI2C.ERR_SUCCESS):
    print("Write data error! %d"%nRet)
    exit()
else:
    print("Write data success!")
# Loop measurement
while(1):
    sleep(1)
    ReadData = (c_ubyte * 2)()
    nRet = ControlI2C.VII_ReadBytes(ControlI2C.VII_USBI2C,0,0,0x46,0x00,byref(ReadData),2)
    if(nRet != ControlI2C.ERR_SUCCESS):
        print("Read data error! %d"%nRet)
        exit()
    else:
        illuminance = ((ReadData[0] << 8) | ReadData[1]) / 1.2
        print("Luminance: %.3f lx"%illuminance)
