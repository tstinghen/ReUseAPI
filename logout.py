import webapp2
from google.appengine.api import users
from jinja2 import Environment, PackageLoader
import jinja2
#code adapted from CS496 week 2 lectures 
	

env = Environment(loader=PackageLoader('main', 'templates'))


class MainPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html'
            template = env.get_template('logout.html')
            self.response.write(template.render())
 

        else: 
        	self.redirect(users.create_login_url(self.request.uri))
