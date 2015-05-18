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
		if self.request.get('type') == 'business': 
			urlsafekey = urlsafe=self.request.get('key')
			bus_key = ndb.Key(urlsafe=self.request.get('key'))
			business = bus_key.get() 
			
			# q = db_defs.Item.query() 
			# q = q.filter(db_defs.Item.business == bus_key)
			# business_items = q.fetch()
			
			template_variables = {'urlsafe_key': urlsafekey, 'key': bus_key, 'name': business.name, 'website': business.website, 'phone': business.phone, 'address' : business.address}
			template_variables['bus_items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().filter(db_defs.Item.businesses == bus_key).fetch()]
			template_variables['all_items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().fetch()]
			render(self, 'edit_business.html', template_variables)
			
	
		
	def post(self):
		
		bus_key = ndb.Key(urlsafe=self.request.get('key'))
		this_business = bus_key.get()
		this_business.name = self.request.get('name')
		this_business.phone = self.request.get('phone')
		this_business.website = self.request.get('website')
		this_business.address = self.request.get('address')
		items = self.request.get_all('add_items[]')
		
		this_business.put()
		
		old_items = this_business.items[:]

		
		if items: 
				
				for it in items: 
					item_key = ndb.Key(db_defs.Item, int(it))
					item_obj = item_key.get()
					

					
					if item_key not in old_items: 
						this_business.items.append(item_key)
						item_obj.businesses.append(bus_key)
						item_obj.put()
						
					if item_key in old_items:
						old_items.remove(item_key) 
						
				
				

				for old in old_items:
					this_business.items.remove(old) 
					this_item = old.get() 
					if bus_key in this_item.businesses: 
						this_item.businesses.remove(bus_key)
						this_item.put()
					
					

			
			
		this_business.put() 
		
		

		render(self, 'success.html', {'message': 'Success: Updated results for ' + str(old_items) + ' in the database'})
		
		
		
	