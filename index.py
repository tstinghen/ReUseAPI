import webapp2
from google.appengine.api import users
from jinja2 import Environment, PackageLoader
import jinja2
	

env = Environment(loader=PackageLoader('main', 'templates'))


class MainPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html'
            template = env.get_template('index.html')
            self.response.write(template.render())
            


        else:
            self.redirect(users.create_login_url(self.request.uri))



class LogoutHandler(webapp2.RequestHandler):
    """
         Destroy user session and redirect to login
    """

    def get(self):
        
        user = users.get_current_user()
        if user:
            greeting = ('Thanks for your participation in ReUse Corvallis, %s! \n (<a href="%s">Sign Out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)
        



	