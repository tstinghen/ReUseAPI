import webapp2
import time
import os 
import db_defs
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader
#from django.http import HttpResponse
#import jinja2
#code adapted from CS496 week 2 lectures 
	
#from jinja2 documentation
env = Environment(loader=PackageLoader('main', 'templates'))

template_variables = {}  

def render(self, template, template_variables={}):
		template = env.get_template(template)
		self.response.write(template.render(template_variables))

def set_temp_vals(self):
	template_variables['items'] = [{'name': x.name, 'key': x.key.urlsafe()} for x in db_defs.Item.query().fetch()]
	template_variables['categories'] = [{'name': x.name, 'key': x.key.urlsafe()} for x in db_defs.Category.query().fetch()]
	template_variables['businesses'] = [{'name': x.name, 'key': x.key.urlsafe()} for x in db_defs.Business.query().fetch()]
	return template_variables 
	
class MainPage(webapp2.RequestHandler):
	template_variables = {}  
   
	
	def get(self): 
		template_variables = set_temp_vals(self)
		render(self, 'view.html', template_variables)
		return
		