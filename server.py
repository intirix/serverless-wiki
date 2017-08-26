#!/usr/bin/python

import logging
import mediawiki_parser.preprocessor
import mediawiki_parser.html
import bleach
import cgi
import time
import boto3
import glob
import zipfile
import shutil
import StringIO
import custom_exceptions

class Context:

	def __init__(self,user):
		self.user = user

class AccessDeniedException(Exception):
	pass


class Server:

	def __init__(self,db):
		self.db = db
		self.log = logging.getLogger("server")
		self.prerender = True
		self.attrs = {
			"*": ['class'],
			"a": ["href", "rel"],
			"img": ["alt"]
		}
		self.allowedTags = ["a","img","h1","h2","h3","h4","h5","b","font","br"]

	def init(self):
		if not self.db.doesPageExist("Index"):
			self.db.updatePage("Index","<system>","mediawiki","= Welcome =")

	def getUserFromContext(self,ctx):
		if ctx == None:
			return "<unknown>"
		return ctx.user

	def createContext(self,username):
		ctx = Context(username)
		return ctx

	def getPage(self,ctx,page):
		obj = {}

		t1 = time.time()
		data = self.db.getPage(page)
		t2 = time.time()
		obj["contentType"] = data["contentType"]
		obj["content"] = data["content"]
		obj["lastModifiedUser"] = data["user"]

		rendered = None
		if "rendered" in data:
			rendered = data["rendered"]
		else:
			rendered = self._render(data["contentType"],data["content"])
		t3 = time.time()
		obj["html"] = self.sanitize(rendered)
		t4 = time.time()
		obj["time_get"] = int(1000 * ( t2 - t1 ))
		obj["time_render"] = int(1000 * ( t3 - t2 ))
		obj["time_sanitize"] = int(1000 * ( t4 - t3 ))

		return obj

	def updatePage(self,ctx,page,data):
		contentType = data["contentType"]
		content = data["content"]

		html = None
		if self.prerender:
			html = self._render(contentType,content)

		self.db.updatePage(page,self.getUserFromContext(ctx),contentType,content,html)
		return self.getPage(ctx,page)

	def sanitize(self,html):
		return bleach.clean(html,tags=self.allowedTags,attributes=self.attrs)

	def _render(self,fmt,markup):
		try:
			if fmt=='mediawiki':
				return self._renderMediaWiki(markup)
		except Exception, e:
			return self._renderText(str(e))
		return self._renderText(markup)

	def _renderText(self,markup):
		return cgi.escape(markup).encode('ascii', 'xmlcharrefreplace')

	def _renderMediaWiki(self,markup):
		templates = {}
		allowed_tags = []
		allowed_self_closing_tags = []
		allowed_attributes = []
		interwiki = {}
		namespaces = {}

		preprocessor = mediawiki_parser.preprocessor.make_parser(templates)

		parser = mediawiki_parser.html.make_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)

		preprocessed_text = preprocessor.parse(markup+"\n")
		output = parser.parse(preprocessed_text.leaves())
		return output.leaf()

	def copyWebsiteToWebpageBucket(self,bucket,restApi,stage):
		client = boto3.client('s3')
		for filename in glob.glob('web/*.html'):
			print(filename)
			f = open(filename)
			key = self._getWebpageKey(filename)
			print("Uploading s3://"+bucket+'/'+key)
			client.put_object(Bucket=bucket,ContentType="text/html",Key=key,Body=f)
			f.close()
		for filename in glob.glob('web/js/*.js'):
			print(filename)
			f = open(filename)
			key = self._getWebpageKey(filename)
			print("Uploading s3://"+bucket+'/'+key)
			client.put_object(Bucket=bucket,ContentType="application/javascript",Key=key,Body=f)
			f.close()
		for filename in glob.glob('web/css/*.css'):
			print(filename)
			f = open(filename)
			key = self._getWebpageKey(filename)
			print("Uploading s3://"+bucket+'/'+key)
			client.put_object(Bucket=bucket,ContentType="text/css",Key=key,Body=f)
			f.close()


		client2 = boto3.client('apigateway')
		print("Deploying latest API")
		resp = client2.create_deployment(restApiId=restApi,stageName=stage)
		print(resp)


		print("Downloading sdk")
		resp = client2.get_sdk(restApiId=restApi,stageName=stage,sdkType='javascript')

		buf = StringIO.StringIO()
		shutil.copyfileobj(resp["body"],buf)

		z = zipfile.ZipFile(buf)

		for zfile in z.namelist():
			print(zfile)
			zif = z.open(zfile)
			zbuf = StringIO.StringIO()
			shutil.copyfileobj(zif,zbuf)
			zif.close()
			print("Uploading s3://"+bucket+"/"+zfile)
			client.put_object(Bucket=bucket,Key=zfile,Body=zbuf.getvalue())


	def _getWebpageKey(self,f):
		return f.replace("web/","")
