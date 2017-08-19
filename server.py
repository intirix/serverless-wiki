#!/usr/bin/python

import logging
import mediawiki_parser.preprocessor
import mediawiki_parser.html
import bleach

class Context:

	def __init__(self,user):
		self.user = user

class AccessDeniedException(Exception):
	pass


class Server:

	def __init__(self,db):
		self.db = db
		self.log = logging.getLogger("server")

	def init(self):
		if not self.db.doesPageExist("Index"):
			self.db.updatePage("Index","<system>","Welcome")

	def createContext(self,username):
		ctx = Context(username)
		return ctx

	def getPage(self,ctx,page):
		obj = {}

		data = self.db.getPage(page)
		obj["contentType"] = data["format"]
		obj["content"] = data["body"]
		obj["html"] = self.sanitize(self._render(data["format"],data["body"]))
		obj["lastModifiedUser"] = data["user"]

		return obj

	def updatePage(self,ctx,page,data):
		contentType = data["contentType"]
		content = data["content"]
		self.db.updatePage(self,page,ctx.user,contentType,content)
		return self.getPage(ctx,page)

	def sanitize(self,html):
		return bleach.clean(html)

	def _render(self,fmt,markup):
		if fmt=='mediawiki':
			return self._renderMediaWiki(markup)
		return markup

	def _renderMediaWiki(self,markup):
		templates = {}
		allowed_tags = []
		allowed_self_closing_tags = []
		allowed_attributes = []
		interwiki = {}
		namespaces = {}

		preprocessor = mediawiki_parser.preprocessor.make_parser(templates)

		parser = mediawiki_parser.html.make_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)

		preprocessed_text = preprocessor.parse(markup)
		output = parser.parse(preprocessed_text.leaves())
		return output.leaf()

