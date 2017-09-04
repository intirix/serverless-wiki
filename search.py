import os
import boto3
import botocore
import logging
import shutil
from whoosh.qparser import MultifieldParser
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED

class PageSchema(SchemaClass):
    key = ID(stored=True, unique=True)
    title = TEXT(stored=True)
    content = TEXT

class SearchIndex:
	directory="/tmp/pageIndex"

	def __init__(self,bucket):
		self.log = logging.getLogger("Search")
		self.bucket = bucket
		self.client = boto3.client('s3')

	def init(self):
		self.ix = self._setupIndex()

	def _setupIndex(self):
		if os.path.exists(self.directory):
			shutil.rmtree(self.directory)
		os.makedirs(self.directory)
		index_files = self.client.list_objects_v2(Bucket=self.bucket, Prefix="pageIndex/")
		if 'Contents' not in index_files:
		 	return self._makeIndex()
		else:
			for object in index_files['Contents']:
				key = object['Key']
				self.client.download_file(Bucket=self.bucket, Key=key,Filename='/tmp/' + key )
			return index.open_dir(self.directory)

	def _makeIndex(self):
		if os.path.exists(self.directory):
			shutil.rmtree(self.directory)
		os.makedirs(self.directory)
		return index.create_in(self.directory, PageSchema)

	def indexPage(self, key, page, content):
		writer = self.ix.writer()
		writer.add_document(key=key, title=page, content=content)
		writer.commit()

	def updatePage(self, key, page, content):
		writer = self.ix.writer()
		writer.update_document(key=key, title=page, content=content)
		writer.commit()

	def searchPage(self, query):
		parser = MultifieldParser(["title", "content"], schema=self.ix.schema)
		parsed_query = parser.parse(query)
		response = []
		with self.ix.searcher() as s:
			results = s.search(parsed_query)
			for r in results:
				obj = {
					'key': r['key'],
					'title': r["title"]
				}
				response.append(obj)
		return response

	def close(self):
		for root,dirs,files in os.walk(self.directory):
			for file in files:
				self.client.upload_file(os.path.join(root,file),self.bucket, "pageIndex/" + file)
