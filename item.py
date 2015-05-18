import webapp2 
from google.appengine.ext import ndb 
import db_defs 
import json 

#code adapted from CS 496 Week 4 lecture video 

class Item(webapp2.RequestHandler): 
	def post(self): 
	#creates an Item entity 
	#this never fires... what the heck. 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
		
	#create a item item using the database definition	
		new_item = db_defs.Item()
	#get name from the http data 
		name = self.request.get('name', default_value = None)
	#get all items from list of item keys 
		busses = self.request.get_all('businesses[]', default_value = None)
		cats = self.request.get_all('category[]', default_value = None)

	#if JSON data, not http data...
		if name is None: 
	#fetch the JSON data
			loaded_data = json.loads(self.request.body)
	#and extract name from that data
			name = loaded_data['name']
			busses = loaded_data['businesses']
			cat = loaded_data['category']
			
		if name: 
			new_item.name = name 
		else: 
			self.response.status = 400 
			self.response.status_message = "Invalid Request, Name is Required" 
		
		if cats: 
			for cat in cats: 
				new_item.category.append(ndb.Key(db_defs.Category, int(cat)))
			
		if busses: 
		#for each item being added, append its Item object to the list of items
			for bus in busses: 
				new_item.businesses.append(ndb.Key(db_defs.Business, int(bus)))
				
	#write the new item to the DB
		key = new_item.put() 
	#create a dictionary of the new entry
		out = new_item.to_dict() 
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
		q = db_defs.Item.query() 
#fetch the results of the query into items variable
		items = q.fetch()
#create an empty list to store results
		slist = []
#for each item in Item, create a dictionary with the key and name
		for s in items: 
			results = {'id' : s.key.id(), 'name' : s.name} 
			slist.append(results)
#write out the dictionary in JSON format 
		self.response.write(json.dumps(slist)) 


		
class ItemsByCategory(webapp2.RequestHandler):
	def post(self): 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
			
		category = db_defs.Category() 
		
		category_id = self.request.get('id', default_value = None)
		
		if category_id is None: 
			loaded_data = json.loads(self.request.body)
			category_id = loaded_data['id']
			
		
		if category_id is not None: 
		
			category_obj = ndb.Key(db_defs.Category, int(category_id))
			
			q = db_defs.Item.query() 
			q = q.filter(db_defs.Item.category == category_obj)
			## Change this line so that it gets the user associated with username ##
			
			item_results = q.fetch()
			
			
					
			rlist = []
			for r in item_results: 
				
				results = {'id' : r.key.id(), 'name' : r.name} 
				rlist.append(results)
			
			self.response.write(json.dumps(rlist)) 

		return 
		
class ItemsByBusiness(webapp2.RequestHandler):
	def post(self): 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
			
		business = db_defs.Business() 
		
		business_id = self.request.get('id', default_value = None)
		
		if business_id is None: 
			loaded_data = json.loads(self.request.body)
			business_id = loaded_data['id']
			
		
		if business_id is not None: 
		
			business_obj = ndb.Key(db_defs.Business, int(business_id))
			
			q = db_defs.Item.query() 
			q = q.filter(db_defs.Item.businesses == business_obj)
			## Change this line so that it gets the user associated with username ##
			
			item_results = q.fetch()
			
			
					
			rlist = []
			for r in item_results: 
				
				results = {'id' : r.key.id(), 'name' : r.name} 
				rlist.append(results)
			
			self.response.write(json.dumps(rlist)) 

		return 
