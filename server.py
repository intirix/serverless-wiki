#!/usr/bin/python

import logging

class Context:

	def __init__(self,user):
		self.user = user

class AccessDeniedException(Exception):
	pass


class Server:

	def __init__(self,db):
		self.db = db
		self.log = logging.getLogger("server")

	def createContext(self,username):
		ctx = Context(username)
		return ctx

	def getPage(self,ctx,page):
		obj = {}

		data = self.db.getPage(page)
		obj["markup"] = data["body"]
		obj["lastModifiedUser"] = data["user"]

		return obj

