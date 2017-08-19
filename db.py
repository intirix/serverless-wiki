#!/usr/bin/python

import boto3
import botocore
import logging
import json

class DBS3:

	def __init__(self,bucket):
		self.log = logging.getLogger("DB.S3")
		self.bucket = bucket

		self.client = boto3.client('s3')

	def getBaseKey(self,page):
		return page+".json"

	def doesPageExist(self,page):
		try:
			self.client.head_object(Bucket=self.bucket,Key=self.getBaseKey(page))
			return True
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				return False
			raise e

	def getPage(self,page):
		try:
			obj = self.client.get_object(Bucket=self.bucket,Key=self.getBaseKey(page))
			contents = json.load(obj["Body"])
			ret = {}
			ret["user"] = contents["user"]
			ret["contentType"] = contents["contentType"]
			ret["content"] = contents["content"]
			return ret
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				return None
			raise e

	def updatePage(self,page,user,contentType,content):
		data={}
		data["user"]=user
		data["contentType"]=contentType
		data["content"]=content
		text=json.dumps(data,indent=2)
		self.client.put_object(Bucket=self.bucket,Body=text,ContentType="application/json",Key=self.getBaseKey(page))
		return True

class DBMemory:

	def __init__(self):
		self.log = logging.getLogger("DB.Memory")
		self.db = {}

	def updatePage(self,page,user,contentType,content):
		if not page in self.db:
			self.db[page]=[]
		self.db[page].insert(0,{'user':user,'contentType':contentType,'content':content})
		return True

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
