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
	template_variables['businesses'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Business.query().fetch()]
	return template_variables 
	
class MainPage(webapp2.RequestHandler):
	template_variables = {}  
   
	
	def get(self): 
		template_variables = set_temp_vals(self)
		render(self, 'add_new.html', template_variables)
		return
		
			
	def post(self):
	
		form_id = self.request.get('form_id')
		if form_id == 'add_category' : 
			new_cat = db_defs.Category()
			new_cat.name = self.request.get('name')
			items = self.request.get_all('add_items[]')

			if items: 
			#for each item being added, append its Item object to the list of items
				
				for it in items: 
					item_key = ndb.Key(db_defs.Item, int(it))
					new_cat.items.append(item_key)

			
			
			cat_key = new_cat.put() 
			
			if items: 
			#for each item being added, append its Item object to the list of items
				
				for i in items: 
					item_key = ndb.Key(db_defs.Item, int(i))					
					this_item = item_key.get() 
					this_item.category.append(cat_key)
					this_item.put()
					
			render(self, 'success.html', {'message': 'Success: Saved results for ' + new_cat.name + ' to the database'})

		if form_id == 'add_item' : 
			new_item = db_defs.Item()
			new_item.name = self.request.get('name')
			category = self.request.get_all('add_category[]')
			businesses = self.request.get_all('add_businesses[]')
			
			if category: 
			#for each item being added, append its Item object to the list of items
				
				for cat in category: 
					new_item.category.append(ndb.Key(db_defs.Category, int(cat)))
			
			if businesses: 
			#for each item being added, append its Item object to the list of items
				
				for bus in businesses: 
					new_item.businesses.append(ndb.Key(db_defs.Business, int(bus)))
			
			item_key = new_item.put() 		

			if category: 
		#for each item being added, append its Item object to the list of items			
				for c in category: 
					cat_key = ndb.Key(db_defs.Category, int(c))					
					this_cat = cat_key.get() 
					this_cat.items.append(item_key)
					this_cat.put()
				
			if  businesses: 
				
		#for each item being added, append its Item object to the list of items			
				for b in businesses: 
					bus_key = ndb.Key(db_defs.Business, int(b))					
					this_bus = bus_key.get() 
					this_bus.items.append(item_key)
					this_bus.put()
				
			render(self, 'success.html', {'message': 'Success: Saved results for ' + str(this_bus) + ' to the database', 'return': '/add_new'})
					