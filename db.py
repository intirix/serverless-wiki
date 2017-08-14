#!/usr/bin/python

import boto3
import logging
import json

class DBS3:

	def __init__(self,bucket):
		self.log = logging.getLogger("DB.S3")
		self.bucket = bucket

		self.client = boto3.client('s3')

	def updatePage(self,page,user,fmt,body):
		data={}
		data["user"]=user
		data["format"]=fmt
		data["body"]=body
		text=json.dumps(data,indent=2)
		self.client.put_object(Body=text,ContentType="application/json",Key="/"+page+".json")

class DBMemory:

	def __init__(self):
		self.log = logging.getLogger("DB.Memory")
		self.db = {}

	def updatePage(self,page,user,fmt,body):
		if not page in self.db:
			self.db[page]=[]
		self.db[page].insert(0,{'user':user,'format':fmt,'body':body})

	def getPage(self,page):
		if page in self.db:
			return self.db[page][0]
		return None

	def doesPageExist(self,page):
		return page in self.db

	def listPageVersions(self,page):
		if not page in self.db:
			return []

		ret = []
		ret.extend(self.db[page])
		ret.reverse()

		return ret

	def getPageVersion(self,page,version):
		if page in self.db and version<=len(self.db[page]):
			return self.db[page][len(self.db[page])-version]
		return None
