import logging
from whoosh.qparser import MultifieldParser
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED

class PageSchema(SchemaClass):
    key = ID(stored=True, unique=True)
    title = TEXT(stored=True)
    content = TEXT

class SearchIndex:
	def __init__(self,db):
		self.log = logging.getLogger("Search")
		self.db = db

	def _setupIndex(self):
		if self.db.setupIndexFiles():
			self.log.info("Reading existing index")
			return index.open_dir(self.db.indexDirectory)
		else:
			self.log.info("Creating new index")
			return index.create_in(self.db.indexDirectory, PageSchema)

	def indexPage(self, page, content):
		key = self.db.getBaseKey(page)
		ix = self._setupIndex()
		writer = ix.writer()
		writer.add_document(key=unicode(key), title=unicode(page), content=unicode(content))
		writer.commit()
		self.db.writeIndex()

	def updatePage(self, page, content):
		key = self.db.getBaseKey(page)
		ix = self._setupIndex()
		writer = ix.writer()
		writer.update_document(key=unicode(key), title=unicode(page), content=unicode(content))
		writer.commit()
		self.db.writeIndex()

	def searchPage(self, query):
		ix = self._setupIndex()
		parser = MultifieldParser(["title", "content"], schema=ix.schema)
		parsed_query = parser.parse(unicode(query))
		self.log.info("Performing search: "+str(parsed_query))
		response = []
		with ix.searcher() as s:
			results = s.search(parsed_query)
			for r in results:
				obj = {
					'key': r['key'],
					'title': r["title"]
				}
				response.append(obj)
		return response
