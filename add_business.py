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
	template_variables['items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().fetch()]
	template_variables['categories'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Category.query().fetch()]
	return template_variables 
	
class MainPage(webapp2.RequestHandler):
	template_variables = {}  
   
	#renders form page 
	def get(self): 
		template_variables = set_temp_vals(self)
		render(self, 'add_business.html', template_variables)
		return
		
	#accepts form data and creates a new business	
	def post(self):
		new_bus = db_defs.Business()
		new_bus.name = self.request.get('name')
		new_bus.phone = self.request.get('phone')
		new_bus.address = self.request.get('address')
		new_bus.website = self.request.get('website')
		#gets a list of items that are associated with the business
		items = self.request.get_all('add_items[]')
		#gets a list of the categories that are associated with the business 
		categories = self.request.get_all('add_categories[]')

		if categories: 
			#for each category of item that the business accepts
			for c in categories: 
				cat_obj = ndb.Key(db_defs.Category, int(c)) 
				q = db_defs.Item.query()
				q = q.filter(db_defs.Item.category == cat_obj)
				cat_items = q.fetch() 
				
				#add each item in each category to the business
				for i in cat_items: 
					new_bus.items.append(i.key)
					
				
		
		
		bus_key = new_bus.put() 
		#for each item in each category
		if categories: 
		
			for c in categories: 
				cat_obj = ndb.Key(db_defs.Category, int(c)) 
				q = db_defs.Item.query()
				q = q.filter(db_defs.Item.category == cat_obj)
				cat_items = q.fetch() 
			#associate the business with the category also	
				for i in cat_items:
					i.businesses.append(bus_key)
					i.put()
				
		render(self, 'success.html',{'message': 'Success: Saved results for ' + new_bus.name + ' to the database', 'return': '/add_business'})
