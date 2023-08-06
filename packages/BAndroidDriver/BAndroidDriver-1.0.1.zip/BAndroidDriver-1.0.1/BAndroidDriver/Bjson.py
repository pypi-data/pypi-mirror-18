# coding=utf-8
import json
import types

'''
 :Description:    json自封装类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
class Bjson(object):
	def __init__(self):
		pass

	def getValue(self,json,keypath):
		for key in keypath:
			if(type(key)==types.UnicodeType):
				key=str(key)
			json=json[key]
		return json

	def upValue(self,json,keypath,value):
		tarr=keypath[::-1]
		temp=self.getValue(json,tarr[:0:-1])
		keyname=tarr[0]
		if(type(keyname)==types.UnicodeType):
			keyname=str(keyname)
		temp[keyname]=value
		for i in range(1,len(tarr)):
			a=i
			keyname=tarr[i]
			if(type(keyname)==types.UnicodeType):
				keyname=str(keyname)
			temp_a=self.getValue(json,tarr[:a:-1])
			temp_a[keyname]=temp
			temp=temp_a
		return temp

	def delKey(self,json,keypath):
		jsontemp=json
		for i in range(0,len(keypath)-1):
			keyname=keypath[i]
			if(type(keyname)==types.UnicodeType):
				keyname=str(keyname)
			# print keyname
			jsontemp=jsontemp[keyname]
			# print jsontemp
		# print len(keypath)
		del jsontemp[keypath[len(keypath)-1]]
		return json

