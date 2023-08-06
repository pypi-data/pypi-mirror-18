# coding=utf-8

'''
 :Description:    app驱动库
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
import os
import re
import time
import subprocess
import threading
import inspect
import ctypes
from BElement import BElement
import xml.etree.cElementTree as ET

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class BAndroidDriver(object):
    DeviceId=None
    DeviceName=None
    def __init__(self):
        pass

    def setDeviceId(self,ID):
        if(ID==""):
            ID=None
        self.DeviceId=ID

    def setDeviceName(self,Name):
        self.DeviceName=Name


    def Script(self,Script):
        if(self.DeviceId!=None):
           Script='adb -s '+self.DeviceId+' '+Script.split('adb')[1]
        return os.popen(Script).read()

    def GetActivitXml(self,FileName):
        adbscript = 'adb devices -l'
        self.Script('adb shell uiautomator dump /data/local/tmp/' + FileName + '.xml')
        self.Script('adb pull /data/local/tmp/' + FileName + '.xml '+PATH(FileName+'.xml'))
        self.Script('adb shell rm -r /data/local/tmp/' + FileName + '.xml')
    def Click(self,x, y):
        self.Script('adb shell input tap ' + str(x) + ' ' + str(y))
    def ClickBack(self):
        self.TapKey('KEYCODE_BACK')
    def ClickEnter(self):
        self.TapKey('KEYCODE_ENTER')
    def Swipe(self,x,y,x1,y1):
        self.Script('adb shell input swipe '+ str(x) + ' ' + str(y)+' '+str(x1) + ' ' + str(y1))
    def Input(self,text):
        self.Script('adb shell input text ' + text)
    def TapKey(self,keycode):
        self.Script('adb shell input keyevent ' + keycode)
    def IntallApp(self,apkfile):
        self.Script('adb install -r '+apkfile)
    def StopApp(self,packge):
        self.Script('adb shell am force-stop ' + packge)
    def StsrtApp(self,packge,appActivity):
        self.Script('adb shell am start '+ packge+'/'+appActivity)
    def AppClearData(self,packge):
        self.Script('adb shell pm clear '+packge)
    def ClearLog(self):
        self.Script('adb logcat -c')
    def GetDevices():
        devices=self.Script("adb shell devices -l")


    def GetPid(self,packgeName):
        Rtu=self.Script("adb shell \"ps |grep "+packgeName+" |grep -v :\"")
        if(Rtu==""):
            print packgeName+" Not have start!"
            return None
        else:
            arr=Rtu.split(' ')
            arr = filter(lambda x:x !='',arr)
            return arr[1]

    def AppLog(self,packgeName,Path):
        Pid=self.GetPid(packgeName)
        self.getLog("adb shell \"logcat |grep "+str(Pid)+"\"",Path)
    
    def getLog(self,script,Path):
        GG = ScriptThread(self,script+" >"+Path)
        GG.start()
        # ctypes.pythonapi.PyThreadState_SetAsyncExc(GG.ident, ctypes.py_object(SystemExit))
        # self.stop_thread(GG)
        return GG
        
    def GetElement(self,TypeName,TypeValue):
        self.GetActivitXml("MarketTest")
        tree = ET.ElementTree(file=PATH("MarketTest.xml"))
        ElementList = tree.iter(tag="node")
        Xpoint = 0;
        Ypoint = 0;
        for Element in ElementList:
            if Element.attrib[TypeName] == TypeValue:
                bounds = Element.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                # print bound
                Xpoint = (int(bound[0]) + int(bound[2])) / 2
                Ypoint = (int(bound[1]) + int(bound[1])) / 2
        BE=BElement()
        BE.setXY(Xpoint,Ypoint,self)
        return BE
        # return (Xpoint, Ypoint)
    

    def _async_raise(self,tid,exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)


class ScriptThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self,device,script):
        threading.Thread.__init__(self)
        self.device = device
        self.script = script
    def run(self):
        try:
            print self.device.DeviceId+"　LogCat..."
            self.device.Script(self.script)
        except Exception, e:
            print "Not have connected Device!"