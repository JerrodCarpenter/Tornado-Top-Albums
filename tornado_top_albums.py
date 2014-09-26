# Jerrod Carpenter
# WWW
# The following is a synchronous approach.

# import tornado.httpserver
# import tornado.httpclient
# import tornado.ioloop
# import tornado.web

# import urllib
# import json

# class IndexHandler(tornado.web.RequestHandler): 
# 	def get(self):
# 		artist = self.get_argument('artist')
# 		client = tornado.httpclient.HTTPClient()
# 		response = client.fetch("http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&api_key=APIKEYHERE&limit=5&format=json&" + \
# 								urllib.urlencode({"artist": artist
# 								})) 
	
# 		body = json.loads(response.body)
# 		albums = body['topalbums']['album']

# 		self.write("""
# 			<div style="text-align: center">
# 			<h1 style="font: 72px Futura">%s</h1>
# 			""" % (artist))

# 		for album in albums:
# 			self.write("""
# 				<div style="font: 18px monaco">Album: %s</div>
# 				<div style="font: 18px monaco">Plays: %s</div>
# 				""" % (album['name'], album['playcount']))

# 		self.write("""</div>""")

# if __name__ == "__main__":
# 	app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
# 	http_server = tornado.httpserver.HTTPServer(app)
# 	http_server.listen(8000) 
# 	tornado.ioloop.IOLoop.instance().start()

# The following is an Asynchronous approach
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.gen

import urllib
import json

class IndexHandler(tornado.web.RequestHandler):
	
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		artist = self.get_argument('artist')
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield tornado.gen.Task(client.fetch,
										  "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&api_key=APIKEYHERE&limit=5&format=json&" + \
										  urllib.urlencode({"artist": artist}))
	
		body = json.loads(response.body)
		albums = body['topalbums']['album']

		self.write("""
			<div style="text-align: center">
			<h1 style="font: 72px Futura">%s</h1>
			""" % (self.get_argument('artist')))

		for album in albums:
			self.write("""
				<div style="font: 18px monaco">Album: %s</div>
				<div style="font: 18px monaco">Plays: %s</div>
				""" % (album['name'], album['playcount']))

		self.write("""</div>""")
		self.finish()

# Is main, port is set to 8000, this is for development
if __name__ == "__main__":
	app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8000) 
	tornado.ioloop.IOLoop.instance().start()
