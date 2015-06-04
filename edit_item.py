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
		if self.request.get('type') == 'item': 
			urlsafekey = urlsafe=self.request.get('key')
			it_key = ndb.Key(urlsafe=self.request.get('key'))
			item = it_key.get() 
			
			# q = db_defs.Item.query() 
			# q = q.filter(db_defs.Item.category == cat_key)
			# category_items = q.fetch()
			
			template_variables = {'urlsafe_key': urlsafekey, 'key': it_key, 'name': item.name, 'category': item.category}
			template_variables['this_cat'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Category.query().filter(db_defs.Category.items == it_key).fetch()]
			template_variables['all_cats'] = [{'name': x.name, 'key': x.key.id(), 'obj': x.key} for x in db_defs.Category.query().fetch()]
			render(self, 'edit_item.html', template_variables)
			
	
		
	def post(self):
		
		it_key = ndb.Key(urlsafe=self.request.get('key'))
		item = it_key.get()
		item.name = self.request.get('name')
		category = self.request.get('add_category')
		
		old_category = item.category[:]

		if category: 
			new_cat_key = ndb.Key(db_defs.Category, int(category))
			item.category = [new_cat_key]
			
			# cat_key = ndb.Key(db_defs.Category, int(category))
			
			for old_key in old_category:
				old = old_key.get()
				if old: 
					if it_key in old.items: 
						old.items.remove(it_key)
						old.put()
			
	
			
		item.put() 
		
		

		render(self, 'success.html', {'message': 'Success: Updated results for ' + item.name + ' in the database'})
		
		
		
	