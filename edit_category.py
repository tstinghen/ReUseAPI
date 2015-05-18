import webapp2
import time
import os 
import db_defs
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader

#####REPEATED CODE FROM SURVEY.PY#####
env = Environment(loader=PackageLoader('main', 'templates'))

template_variables = {}  

def render(self, template, template_variables={}):
		template = env.get_template(template)
		self.response.write(template.render(template_variables))
######END REPEATED SECTION#####	
		
class EditPage(webapp2.RequestHandler):
	
	def get(self): 
		template_variables = {}
		if self.request.get('type') == 'category': 
			urlsafekey = urlsafe=self.request.get('key')
			cat_key = ndb.Key(urlsafe=self.request.get('key'))
			category = cat_key.get() 
			
			# q = db_defs.Item.query() 
			# q = q.filter(db_defs.Item.category == cat_key)
			# category_items = q.fetch()
			
			template_variables = {'urlsafe_key': urlsafekey, 'key': cat_key, 'name': category.name, 'items': category.items}
			template_variables['cat_items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().filter(db_defs.Item.category == cat_key).fetch()]
			template_variables['all_items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().fetch()]
			render(self, 'edit_category.html', template_variables)
			
	
		
	def post(self):
		
		cat_key = ndb.Key(urlsafe=self.request.get('key'))
		category = cat_key.get()
		category.name = self.request.get('name')
		items = self.request.get_all('add_items[]')
		
		old_items = category.items[:]

		
		if items: 
				
				for it in items: 
					item_key = ndb.Key(db_defs.Item, int(it))
					item_obj = item_key.get()
					

					
					if item_key not in old_items: 
						x = 0
						category.items.append(item_key)
						item_obj.category.append(cat_key)
						item_obj.put()
						
					if item_key in old_items:
						old_items.remove(item_key) 
						
				
				
				for old in old_items:
					category.items.remove(old) 
					this_item = old.get() 
					if cat_key in this_item.category: 
						this_item.category.remove(cat_key)
						this_item.put()
						
					

			
			
		category.put() 
		
		

		render(self, 'success.html', {'message': 'Success: Updated results for ' + str(old_items) + ' in the database'})
		
		
		
	