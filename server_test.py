#!/usr/bin/python

import unittest
import server
import logging

class TestServer(unittest.TestCase):

	def testRender(self):
		obj = server.Server(None)

		self.assertEquals("<body>\n<h1> Test </h1>\n</body>",obj._renderMediaWiki("= Test =\n"))


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

