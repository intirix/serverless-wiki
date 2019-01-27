import logging
from whoosh.qparser import MultifieldParser
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from functools import reduce

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
		writer.add_document(key=str(key), title=str(page), content=str(content))
		writer.commit()
		self.db.writeIndex()

	def updatePage(self, page, content):
		key = self.db.getBaseKey(page)
		ix = self._setupIndex()
		writer = ix.writer()
		writer.update_document(key=str(key), title=str(page), content=str(content))
		writer.commit()
		self.db.writeIndex()

	def searchPage(self, query):
		ix = self._setupIndex()
		parser = MultifieldParser(["title", "content"], schema=ix.schema)
		parsed_query = parser.parse(str(query))
		self.log.info("Performing search: "+str(parsed_query))
		response = []
		with ix.searcher() as s:
			results = s.search(parsed_query,terms=True)
			for r in results:
				terms = [x[1] for x in r.matched_terms()]
				terms = reduce(lambda x,y: x+[y] if not y in x else x, terms,[])
				obj = {
					'key': r['key'],
					'title': r["title"],
					'terms' : terms
				}
				response.append(obj)
		return response
