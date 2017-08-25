#!/usr/bin/python

import db
import logging
import server
import json
import base64
import os

class LambdaCommon:

        def __init__(self):
                self.log = logging.getLogger("Lambda")

		self.db = self.createDb()
		self.server = server.Server(self.db)
		self.server.init()
		self.resp = None
		self.ctx = None

	def getPageBucket(self):
                pageBucket = "pagebucket"
                if "PAGE_BUCKET" in os.environ:
                        pageBucket = os.environ["PAGE_BUCKET"]
		return pageBucket

	def createDb(self):
                pageBucket = self.getPageBucket()

		return db.DBS3(pageBucket)

	def getResponse(self):
		return self.resp

def get_body(event):
        if not "body" in event:
                return None

        if event["body"]==None:
                return None

        if "isBase64Encoded" in event and event["isBase64Encoded"]==True:
                return base64.b64decode(event["body"])

        return event["body"]

def matches(event,meth,path):
        log = logging.getLogger("Lambda")
        if event==None:
                return False

        if not "httpMethod" in event or meth != event["httpMethod"]:
                return False

        if "requestContext" in event and "resourcePath" in event["requestContext"]:
                if path == event["requestContext"]["resourcePath"]:
                        log.info("Matched "+meth+" to "+path)
                        return True

        return False

def addCorsHeaders(resp):
	headers={}
	headers["Access-Control-Allow-Headers"] = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
	headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
	headers["Access-Control-Allow-Origin"] = "*"
	if not "headers" in resp:
		resp["headers"] = {}

	for key in headers.keys():
		if not key in resp["headers"]:
			resp["headers"][key]=headers[key]
	return resp


def single_func(event, context):
        print(json.dumps(event,indent=2))

	if event==None or not "body" in event:
		obj = LambdaCommon()
		obj.server.copyWebsiteToWebpageBucket(os.environ["WEBSITE_BUCKET"])
		return

        if matches(event,"GET","/v1/pages/{page}"):
                return get_page(event, context)
        if matches(event,"POST","/v1/pages/{page}"):
                return update_page(event, context)
        if matches(event,"PUT","/v1/pages/{page}"):
                return update_page(event, context)

	return {"statusCode":404}


def get_page(event, context):
        obj = LambdaCommon()
        if obj.getResponse() != None:
                return obj.getResponse()

        try:
                page = event["pathParameters"]["page"]

		resp = obj.server.getPage(obj.ctx,page)

                return addCorsHeaders({"statusCode":200,"body":json.dumps(resp,indent=2)})
        except server.AccessDeniedException, e:
                obj.log.exception("Access Denied")
                return addCorsHeaders({"statusCode":403})
        except:
                obj.log.exception("Error")
                return addCorsHeaders({"statusCode":500})
        return addCorsHeaders({"statusCode":404})

def update_page(event, context):
        obj = LambdaCommon()
        if obj.getResponse() != None:
                return obj.getResponse()

        try:
                page = event["pathParameters"]["page"]
		body = json.loads(get_body(event))

		resp = obj.server.updatePage(obj.ctx,page,body)

                return addCorsHeaders({"statusCode":200,"body":json.dumps(resp,indent=2)})
        except server.AccessDeniedException, e:
                obj.log.exception("Access Denied")
                return addCorsHeaders({"statusCode":403})
        except:
                obj.log.exception("Error")
                return addCorsHeaders({"statusCode":500})
        return addCorsHeaders({"statusCode":404})



FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT)

