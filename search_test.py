#!/usr/bin/python

import unittest
import server
import logging
import db
import custom_exceptions
import search

class TestSearch(unittest.TestCase):

	def testBasicSearch(self):
		mydb = db.DBMemory()
		with mydb:
			obj = server.Server(mydb)
			ctx = server.Context("<unittest>")


			data={}
			data["contentType"]="mediawiki"
			data["content"]="= Test =\nThis is a test page to verify that search is working\n"

			obj.updatePage(ctx,"testPage",data)

			ret = obj.search(ctx,"test")
			print(ret)
			ret = obj.search(ctx,"verify")
			print(ret)


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()
