import webapp2 
from google.appengine.ext import ndb 
import db_defs 
import json 

#code adapted from CS 496 Week 4 lecture video 

class Category(webapp2.RequestHandler): 
	def post(self): 
	#creates a Category entity 
	#this never fires... what the heck. 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
		
	#create a category item using the database definition	
		new_cat = db_defs.Category()
	#get name from the http data 
		name = self.request.get('name', default_value = None)
	#get all items from list of item keys 
		items = self.request.get_all('items[]', default_value = None)

	#if JSON data, not http data...
		if name is None: 
	#fetch the JSON data
			loaded_data = json.loads(self.request.body)
	#and extract name from that data
			name = loaded_data['name']
			
		if name: 
			new_cat.name = name 
		else: 
			self.response.status = 400 
			self.response.status_message = "Invalid Request, Name is Required" 

			
		if items: 
		#for each item being added, append its Item object to the list of items
			for it in items: 
				new_cat.items.append(ndb.Key(db_defs.Item, int(it)))
				
	#write the new Category to the DB
		key = new_cat.put() 
	#create a dictionary of the new entry
		out = new_cat.to_dict() 
	#write the dictionary as formatted JSON
		self.response.write(json.dumps(out)) 

		return 
	
	def get(self, **kwargs): 	

	#This never fires... why?
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
	#query for all items of type Category
		q = db_defs.Category.query() 
#fetch the results of the query into cats variable
		cats = q.fetch()
#create an empty list to store results
		slist = []
#for each item in Category, create a dictionary with the key and name
		for s in cats: 
			results = {'id' : s.key.id(), 'name' : s.name} 
			slist.append(results)
#write out the dictionary in JSON format 
		self.response.write(json.dumps(slist)) 

