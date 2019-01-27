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

		self.assertEqual("admin",obj.getPage('index')['user'])
		self.assertEqual("my body",obj.getPage('index')['content'])

	def testVersions(self):
		obj = db.DBMemory()
		obj.updatePage('index','admin','mediawiki','my body')
		self.assertEqual("my body",obj.getPage('index')['content'])
		self.assertEqual(1,len(obj.listPageVersions('index')))
		obj.updatePage('index','steve','mediawiki','new body')
		self.assertEqual("new body",obj.getPage('index')['content'])
		self.assertEqual(2,len(obj.listPageVersions('index')))
		self.assertEqual("my body",obj.getPageVersion('index',1)['content'])
		self.assertEqual("new body",obj.getPageVersion('index',2)['content'])

	def testNotFound(self):
		obj = db.DBMemory()
		self.assertEqual(False, obj.doesPageExist('doesNotExist'))
		with self.assertRaises(custom_exceptions.NotFound):
			obj.getPage('doesNotExist')

if __name__ == '__main__':
	#FORMAT = "%(asctime)-15s %(message)s"
	#logging.basicConfig(format=FORMAT)
	unittest.main()
