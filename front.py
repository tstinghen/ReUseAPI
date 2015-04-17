import webapp2
import os 

class Front(webapp2.RequestHandler):
    def get(self):
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write("Web Based API for Corvallis ReUse App Group 17\n\n")
