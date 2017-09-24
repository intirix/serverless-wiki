import BaseHTTPServer
import SimpleHTTPServer
import server
import db
import logging
import re
import os
import custom_exceptions

PORT = 8080
PATH_REGEX = r'^\/v1\/pages\/([^\/]*)$'

#class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def respond(self, statusCode, message):
		self.send_response(statusCode)
		self.end_headers()
		self.wfile.write(message)

	def do_GET(self):
		matches = re.match(PATH_REGEX, self.path)
		if matches:
			path = matches.group(1)
		elif self.path == '/web/' and self.server.apiGatewayClientUrl != None:
			f = open("web/index.html")
			html = f.read()
			f.close()
			html = html.replace('src="apiGateway-js-sdk/','src="'+self.server.apiGatewayClientUrl+'/apiGateway-js-sdk/')
			self.respond(200,html)
			return

		else:
			return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
			#return super(MyHandler,self).do_GET()
			#self.respond(404, "Not Found")
			#return
		try:
			page = self.server.serverIface.getPage('<httpserver>', path)
			self.respond(200, page["html"])
		except custom_exceptions.NotFound:
			self.respond(404, "Not Found")
		except:
			self.respond(500, "Internal Error")

	def do_POST(self):
			self.respond(501, "Not implemented")
	def do_PUT(self):
			self.respond(501, "Not implemented")

if __name__ == '__main__':
	logger = logging.getLogger('HTTPServer')
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(('127.0.0.1', PORT), MyHandler)
	if "PAGE_BUCKET" in os.environ:
		pageBucket = os.environ["PAGE_BUCKET"]
		mydb = db.DBS3(pageBucket)
	else:
		mydb = db.DBMemory()

	if "APIG_URL" in os.environ:
		httpd.apiGatewayClientUrl = os.environ["APIG_URL"]
	else:
		httpd.apiGatewayClientUrl = None
	httpd.serverIface = server.Server(mydb)
	httpd.serverIface.init()
	try:
		httpd.serve_forever()
		logger.info('Started server on port ' + PORT)
	except KeyboardInterrupt:
		pass
	httpd.server_close()
