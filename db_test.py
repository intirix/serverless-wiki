#!/usr/bin/python

import unittest
import db
import logging

class TestDBMemory(unittest.TestCase):

	def testCrud(self):
		obj = db.DBMemory()
		self.assertFalse(obj.doesPageExist('index'))
		obj.updatePage('index','admin','mediawiki','my body')
		self.assertTrue(obj.doesPageExist('index'))

		self.assertEquals("admin",obj.getPage('index')['user'])
		self.assertEquals("my body",obj.getPage('index')['body'])

	def testVersions(self):
		obj = db.DBMemory()
		obj.updatePage('index','admin','mediawiki','my body')
		self.assertEquals("my body",obj.getPage('index')['body'])
		self.assertEquals(1,len(obj.listPageVersions('index')))
		obj.updatePage('index','steve','mediawiki','new body')
		self.assertEquals("new body",obj.getPage('index')['body'])
		self.assertEquals(2,len(obj.listPageVersions('index')))
		self.assertEquals("my body",obj.getPageVersion('index',1)['body'])
		self.assertEquals("new body",obj.getPageVersion('index',2)['body'])


if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()

