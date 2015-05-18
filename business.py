import webapp2 
from google.appengine.ext import ndb 
import db_defs 
import json 

#code adapted from CS 496 Week 4 lecture video 

class Business(webapp2.RequestHandler): 
	def post(self): 
	
	#creates an Item entity 
	#this never fires... what the heck. 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
		
	#create a item item using the database definition	
		new_business = db_defs.Business()
	#get name from the http data 
		name = self.request.get('name', default_value = None)
	#get all items from list of item keys \
		phone = self.request.get('phone', default_value = None)
		website = self.request.get('website', default_value = None)
		address = self.request.get('address', default_value = None)
		items = self.request.get_all('items[]', default_value = None)


	#if JSON data, not http data...
		if name is None: 
	#fetch the JSON data
			loaded_data = json.loads(self.request.body)
	#and extract name from that data
			name = loaded_data['name']
			phone = loaded_data['phone']
			website = loaded_data['website']
			address = loaded_data['address']
			items = load_data['items']
			
		if name: 
			new_business.name = name 
		else: 
			self.response.status = 400 
			self.response.status_message = "Invalid Request, Name is Required" 
		
		if phone: 
			new_business.phone = phone 
			
		if website: 
			new_business.website = website 
			
		if address: 
			new_business.address = address 
			
		
		#for each item being added, append its Item object to the list of items
		if items: 
			for item in items: 
				new_business.items.append(ndb.Key(db_defs.Item, int(item)))
				
	#write the new item to the DB
		key = new_business.put() 
	#create a dictionary of the new entry
		out = new_business.to_dict() 
	#write the dictionary as formatted JSON
		self.response.write(json.dumps(out)) 

		return 
	
	def get(self, **kwargs): 	

	#This never fires... why?
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
#query for all items of type item
		q = db_defs.Business.query() 
#fetch the results of the query into items variable
		busses = q.fetch()
#create an empty list to store results
		slist = []
#for each item in Item, create a dictionary with the key and name
		for s in busses: 
			results = {'id' : s.key.id(), 'name' : s.name, 'phone' : s.phone, 'address' : s.address, 'website' : s.website} 
			slist.append(results)
#write out the dictionary in JSON format 
		self.response.write(json.dumps(slist)) 

		
class BusinessesByItem(webapp2.RequestHandler):
	def post(self): 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
			
		item = db_defs.Item() 
		
		item_id = self.request.get('id', default_value = None)
		
		if item_id is None: 
			loaded_data = json.loads(self.request.body)
			item_id = loaded_data['id']
			
		
		if item_id is not None: 
		
			item_obj = ndb.Key(db_defs.Item, int(item_id))
			
			q = db_defs.Business.query() 
			q = q.filter(db_defs.Business.items == item_obj)
			
			
			business_results = q.fetch()
	
					
			rlist = []
			for r in business_results: 
				
				results = {'id' : r.key.id(), 'name' : r.name, 'phone' : r.phone, 'website' : r.website, 'address' : r.address} 
				rlist.append(results)
			
			self.response.write(json.dumps(rlist)) 

		return 

