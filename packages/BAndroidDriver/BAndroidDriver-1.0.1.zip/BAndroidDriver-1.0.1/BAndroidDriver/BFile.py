# coding=utf-8
import os

'''
 :Description:    文件自封装类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
class BFile(object):
	"""docstring for File"""
	def __init__(self):
		pass

	def GetCaseList(self,path):
		f = open(path)
		line = f.readline()
		CaseList=[]
		while line:  
			CaseList.append(line)
			line = f.readline()
		f.close()
		return CaseList


	def GetInterfaceSource(self,path):
		f = open(path)
		try:
			InterfaceSource = f.read()
		finally:
			f.close()
		return InterfaceSource


	def upInterfaceOut(self,path,json):
		f=open(path,'w')
		f.write(json)
		f.close()

	def log(self,path,string):
		f = open(path, 'a')
		f.write(string+"\n")
		f.close()


	def clear(self,path):
		f=open(path,'w+')
		f.write("")
		f.close()

	def GetDirList(self,path):
		fs = os.listdir(path)
		return fs

	def Read(self,path):
		f=open(path)
		try:
			string=f.read()
		finally:
			f.close()
		return string

	def NewDir(self,path):
		os.mkdir(path)

	def DelDir(self,path):
		os.remove(path)