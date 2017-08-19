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
		self.assertEquals("pagebucket",obj.getPageBucket())

		os.environ["PAGE_BUCKET"] = "OVERRIDE_BUCKET"
		self.assertEquals("OVERRIDE_BUCKET",obj.getPageBucket())



if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

