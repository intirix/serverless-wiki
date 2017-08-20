#!/usr/bin/python

import unittest
import server
import logging

class TestServer(unittest.TestCase):

	def testRender(self):
		obj = server.Server(None)

		self.assertEquals("<body>\n<h1> Test </h1>\n</body>",obj._renderMediaWiki("= Test =\n"))
		self.assertEquals("<body>\n<h1> Test </h1>\n</body>",obj._renderMediaWiki("= Test ="))

	def testSanitizeEvil(self):
		obj = server.Server(None)
		self.assertFalse("<script>" in obj.sanitize("<script>evil();</script>"))

	def testSanitizeSafe(self):
		obj = server.Server(None)
		self.assertEquals("<h1>Welcome</h1>",obj.sanitize("<h1>Welcome</h1>"))

	def testFailedRender(self):
		obj = server.Server(None)
		html = obj._render("mediawiki","= Welcome")
		self.assertTrue("= Welcome" in html)


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

