#!/usr/bin/python

import db
import logging
import server
import json
import base64


class LambdaCommon:

        def __init__(self):
                self.log = logging.getLogger("Lambda")
                self.system = system.System()

                pageBucket = "pagebucket"
                if "PAGE_BUCKET" in os.environ:
                        pageBucket = os.environ["PAGE_BUCKET"]

		self.db = db.DBMemory()
		self.server = server.Server(self.db)
		self.resp = None
		self.ctx = None

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

def single_func(event, context):
        print(json.dumps(event,indent=2))

        if matches(event,"GET","/v1/pages/{page}"):
                return get_page(event, context)

	return {"statusCode":404}


def get_page(event, context):
        obj = LambdaCommon()
        if obj.getResponse() != None:
                return obj.getResponse()

        try:
                page = event["pathParameters"]["page"]

		resp = obj.server.getPage(obj.ctx,page)

                return {"statusCode":200,"body":json.dumps(resp,indent=2)}
        except server.AccessDeniedException, e:
                obj.log.exception("Access Denied")
                return {"statusCode":403}
        except:
                obj.log.exception("Error")
                return {"statusCode":500}
        return {"statusCode":404}



FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT)

