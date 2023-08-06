# coding=utf-8

'''
 :Description:    控件类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
class BElement(object):
	Xpoint=None
	Ypoint=None
	device=None
	def __init__(self):
		pass
	def setXY(self,x,y,device):
		self.Xpoint=x
		self.Ypoint=y
		self.device=device
	def click(self):
		self.device.Click(self.Xpoint,self.Ypoint)

	def Input(self,Str):
		self.device.Click(self.Xpoint,self.Ypoint)
		self.device.Input(Str)