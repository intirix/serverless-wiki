#!/usr/bin/python

import unittest
import server
import logging
import db

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

	def testNonRenderedPage(self):
		mydb = db.DBMemory()
		obj = server.Server(mydb)
		ctx = server.Context("<unittest>")

		mydb.updatePage("testPage","<unittest>","mediawiki","= Test =",None)
		self.assertEquals("\n<h1> Test </h1>\n",obj.getPage(ctx,"testPage")["html"])

	def testRenderedPage(self):
		mydb = db.DBMemory()
		obj = server.Server(mydb)
		ctx = server.Context("<unittest>")

		rendered = "<h1>Rendered</h1>"

		mydb.updatePage("testPage","<unittest>","mediawiki","= Test =",rendered)
		self.assertEquals(rendered,obj.getPage(ctx,"testPage")["html"])


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

