#!/usr/bin/python

import unittest
import db
import lambda_functions
import logging
import os

class LambdaCommon(lambda_functions.LambdaCommon):

	def createDb(self):
		return db.DBMemory()

class TestLambdaFunctions(unittest.TestCase):

	def testCommon(self):
		obj = LambdaCommon()

	def testPageBucket(self):
		obj = LambdaCommon()
		self.assertEqual("pagebucket",obj.getPageBucket())

		os.environ["PAGE_BUCKET"] = "OVERRIDE_BUCKET"
		self.assertEqual("OVERRIDE_BUCKET",obj.getPageBucket())

	def testaddCorsHeaders(self):
		resp = lambda_functions.addCorsHeaders({"statusCode":200,"body":"{}"})
		self.assertEqual(200,resp["statusCode"])
		self.assertEqual("{}",resp["body"])
		self.assertTrue("Authorization" in resp["headers"]["Access-Control-Allow-Headers"].split(','))
		self.assertTrue("Content-Type" in resp["headers"]["Access-Control-Allow-Headers"].split(','))
		self.assertTrue("GET" in resp["headers"]["Access-Control-Allow-Methods"].split(','))
		self.assertEqual("*",resp["headers"]["Access-Control-Allow-Origin"])


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

