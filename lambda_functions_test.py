#!/usr/bin/python

import unittest
import db
import lambda_functions
import logging

class LambdaCommon(lambda_functions.LambdaCommon):

	def createDb(self):
		return db.DBMemory()

class TestLambdaFunctions(unittest.TestCase):

	def testCommon(self):
		obj = LambdaCommon()



if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

