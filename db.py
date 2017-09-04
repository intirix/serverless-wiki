#!/usr/bin/python

import boto3
import botocore
import logging
import json
import time
import custom_exceptions
import search

class DBS3:

	def __init__(self,bucket):
		self.log = logging.getLogger("DB.S3")
		self.bucket = bucket
		self.search = search.SearchIndex(bucket)
		self.client = boto3.client('s3')

	def getBaseKey(self,page):
		return page+".json"

	def getTimestampKey(self,page,timestamp):
		return self.getBaseKey(page) + ".json." + str(timestamp)

	def _pageFromResponse(self, response):
		contents = json.load(response["Body"])
		ret = {}
		ret["user"] = contents["user"]
		ret["contentType"] = contents["contentType"]
		ret["content"] = contents["content"]
		if "rendered" in contents:
			ret["rendered"] = contents["rendered"]
		return ret

	def doesPageExist(self,page):
		try:
			self.client.head_object(Bucket=self.bucket,Key=self.getBaseKey(page))
			return True
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "NoSuchKey":
				return False
			raise e

	def getPage(self,page):
		try:
			obj = self.client.get_object(Bucket=self.bucket,Key=self.getBaseKey(page))
			return self._pageFromResponse(obj)
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "NoSuchKey":
				raise custom_exceptions.NotFound()
			raise e

	def updatePage(self,page,user,contentType,content,html=None):
		data={}
		data["user"]=user
		data["contentType"]=contentType
		data["content"]=content
		if html!=None:
			data["rendered"]=html
		text=json.dumps(data,indent=2)
		self.search.init()
		self.search.indexPage(self.getBaseKey(page), page, content)
		self.search.close()
		self.client.put_object(Bucket=self.bucket,Body=text,ContentType="application/json",Key=self.getBaseKey(page))
		self._writeVersionedFile(page,text)
		return True

	def searchPage(self, query):
		self.search.init()
		return self.search.searchPage(query)

	def _writeVersionedFile(self,page,data):
		timestamp = int(time.time())
		self.client.put_object(Bucket=self.bucket,Body=data,ContentType="application/json",Key=self.getTimestampKey(page,timestamp))

	def listPageVersions(self, page):
		pageKey = self.getBaseKey(page)
		#Can only retrieve up to 1000 versions of a page
		page_versions = self.client.list_objects_v2(Prefix=pageKey)
		page_versions.reverse()
		return page_versions

	def getPageVersion(self, page, timestamp):
		pageKey = self.getTimestampKey(page,timestamp)
		try:
			obj = self.client.get_object(Bucket=self.bucket,Key=pageKey)
			return self._pageFromResponse(obj)
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				raise custom_exceptions.NotFound()
			raise e

class DBMemory:

	def __init__(self):
		self.log = logging.getLogger("DB.Memory")
		self.db = {}

	def updatePage(self,page,user,contentType,content,html=None):
		if not page in self.db:
			self.db[page]=[]
		obj={'user':user,'contentType':contentType,'content':content}
		if html != None:
			obj["rendered"]=html
		self.db[page].insert(0,obj)
		return True

	def getPage(self,page):
		if page in self.db:
			return self.db[page][0]
		raise custom_exceptions.NotFound()

	def doesPageExist(self,page):
		return page in self.db

	def listPageVersions(self,page):
		if not page in self.db:
			raise custom_exceptions.NotFound()

		ret = []
		ret.extend(self.db[page])
		ret.reverse()

		return ret

	def getPageVersion(self,page,version):
		if page in self.db and version<=len(self.db[page]):
			return self.db[page][len(self.db[page])-version]
		return None
