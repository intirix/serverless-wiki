#!/usr/bin/python

import unittest
import server
import logging
import db
import custom_exceptions

class TestServer(unittest.TestCase):

	def testRender(self):
		obj = server.Server(None)

		self.assertEqual("<body>\n<h1> Test </h1>\n</body>",obj._renderMediaWiki("= Test =\n"))
		self.assertEqual("<body>\n<h1> Test </h1>\n</body>",obj._renderMediaWiki("= Test ="))

	def testSanitizeEvil(self):
		obj = server.Server(None)
		self.assertFalse("<script>" in obj.sanitize("<script>evil();</script>"))

	def testSanitizeSafe(self):
		obj = server.Server(None)
		self.assertEqual("<h1>Welcome</h1>",obj.sanitize("<h1>Welcome</h1>"))

	def testFailedRender(self):
		obj = server.Server(None)
		html = obj._render("mediawiki","= Welcome")
		self.assertTrue("= Welcome" in html)

	def testNonRenderedPage(self):
		mydb = db.DBMemory()
		obj = server.Server(mydb)
		ctx = server.Context("<unittest>")

		mydb.updatePage("testPage","<unittest>","mediawiki","= Test =",None)
		page = obj.getPage(ctx,"testPage")
		self.assertEqual("= Test =",page["content"])
		self.assertTrue(page["html"].find("<h1> Test </h1>")>=0)

	def testRenderedPage(self):
		mydb = db.DBMemory()
		obj = server.Server(mydb)
		ctx = server.Context("<unittest>")

		rendered = "<h1>Rendered</h1>"

		mydb.updatePage("testPage","<unittest>","mediawiki","= Test =",rendered)
		self.assertEqual(rendered,obj.getPage(ctx,"testPage")["html"])

	def testNoFound(self):
		mydb = db.DBMemory()
		obj = server.Server(mydb)
		ctx = server.Context("<unittest>")
		self.assertEqual(False, mydb.doesPageExist("doesNotExist"))
		with self.assertRaises(custom_exceptions.NotFound):
			obj.getPage(ctx, "doesNotExist")

	def testInvalidInput(self):
		mydb = db.DBMemory()
		obj = server.Server(mydb)
		ctx = server.Context("<unittest>")
		with self.assertRaises(custom_exceptions.InvalidInput):
			obj.updatePage(ctx,"Index",{})
		with self.assertRaises(custom_exceptions.InvalidInput):
			obj.updatePage(ctx,"Index",{"contentType":"mediawiki","content":{}})


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()
