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
	# load the page with the current business data 
	def get(self): 
		template_variables = {}
		if self.request.get('type') == 'business': 
			urlsafekey = urlsafe=self.request.get('key')
			bus_key = ndb.Key(urlsafe=self.request.get('key'))
			business = bus_key.get() 
			
			#creates variables that are passed into the Jinja/HTML template
			template_variables = {'urlsafe_key': urlsafekey, 'key': bus_key, 'name': business.name, 'website': business.website, 'phone': business.phone, 'address' : business.address}
			template_variables['bus_items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().filter(db_defs.Item.businesses == bus_key).fetch()]
			template_variables['all_items'] = [{'name': x.name, 'key': x.key.id()} for x in db_defs.Item.query().fetch()]
			render(self, 'edit_business.html', template_variables)

			
	def post(self):
		#gets the key from the form, to update the existing object
		bus_key = ndb.Key(urlsafe=self.request.get('key'))
		this_business = bus_key.get()
		#gets all of the information, whether or not it was edited 
		this_business.name = self.request.get('name')
		this_business.phone = self.request.get('phone')
		this_business.website = self.request.get('website')
		this_business.address = self.request.get('address')
		items = self.request.get_all('add_items[]')
		
		this_business.put()
		#gets the list of items currently stored in the business object
		old_items = this_business.items[:]

		#if there were items entered on the edit form
		if items: 
				
				for it in items: 
					item_key = ndb.Key(db_defs.Item, int(it))
					item_obj = item_key.get()
					

				#if the item was not already associated with the business, add it to the business' items	
					if item_key not in old_items: 
						this_business.items.append(item_key)
						item_obj.businesses.append(bus_key)
						item_obj.put()
				#if the item is still associated with the business (no change) delete it from the old items list		
					if item_key in old_items:
						old_items.remove(item_key) 
						
				
				
				#for any items that were previously associated but now are not associated 
				#delete the item from the business 
				#and also delete the business from the item's business list. 
				for old in old_items:
					this_business.items.remove(old) 
					this_item = old.get() 
					if bus_key in this_item.businesses: 
						this_item.businesses.remove(bus_key)
						this_item.put()
					
					

			
			
		this_business.put() 

		
		render(self, 'success.html', {'message': 'Success: Updated results for ' + this_business.name + ' in the database'})
		
		
		
	