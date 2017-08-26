#!/usr/bin/python

import unittest
import db
import logging
import custom_exceptions

class TestDBMemory(unittest.TestCase):

	def testCrud(self):
		obj = db.DBMemory()
		self.assertFalse(obj.doesPageExist('index'))
		obj.updatePage('index','admin','mediawiki','my body')
		self.assertTrue(obj.doesPageExist('index'))

		self.assertEquals("admin",obj.getPage('index')['user'])
		self.assertEquals("my body",obj.getPage('index')['content'])

	def testVersions(self):
		obj = db.DBMemory()
		obj.updatePage('index','admin','mediawiki','my body')
		self.assertEquals("my body",obj.getPage('index')['content'])
		self.assertEquals(1,len(obj.listPageVersions('index')))
		obj.updatePage('index','steve','mediawiki','new body')
		self.assertEquals("new body",obj.getPage('index')['content'])
		self.assertEquals(2,len(obj.listPageVersions('index')))
		self.assertEquals("my body",obj.getPageVersion('index',1)['content'])
		self.assertEquals("new body",obj.getPageVersion('index',2)['content'])

	def testNotFound(self):
		obj = db.DBMemory()
		self.assertEquals(False, obj.doesPageExist('doesNotExist'))
		with self.assertRaises(custom_exceptions.NotFound):
			obj.getPage('doesNotExist')

if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()
