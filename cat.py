import webapp2 
from google.appengine.ext import ndb 
import db_defs 
import json 

#code adapted from CS 496 Week 4 lecture video 


#curl -- data = "name=test" -H "Accept: application/json" http://localhost:11080/cat
class Cat(webapp2.RequestHandler): 
	def post(self): 
	#creates a Cat entity 
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
		
		
		new_cat = db_defs.Cat()
		name = self.request.get('name', default_value = None)
		color = self.request.get('color', default_value = None) 
		nap_spot = self.request.get('nap_spot', default_value = None) 
		id = self.request.get('id', default_value = None)
		
		if name is None: 
			loaded_data = json.loads(self.request.body)
			name = loaded_data['name']
			color = loaded_data['color']
			nap_spot = loaded_data['nap_spot']
			
		if name: 
			new_cat.name = name 
		else: 
			self.response.status = 400 
			self.response.status_message = "Invalid Request, Name is Required" 
		if color: 
			new_cat.color = color 
		if nap_spot: 
			new_cat.nap_spot = nap_spot
		slist = [] 
		key = new_cat.put() 
		out = new_cat.to_dict() 
		slist.append(out)
		self.response.write(json.dumps(out)) 

		return 
	
	def get(self, **kwargs): 	
		if 'application/json' not in self.request.accept: 
			self.response.status = 406 
			self.response.status_message = "API only supports json type" 
			return 
		if 'id' in kwargs: 
			out = ndb.Key(db_defs.Cat, int(kwargs['id'])).get().to_dict() 
			self.response.write(json.dumps(out)) 
		else:
			q = db_defs.Cat.query() 
			cats = q.fetch()
			slist = []
			for s in cats: 
				results = {'id' : s.key.id(), 'name' : s.name, 'color': s.color, 'nap_spot': s.nap_spot} 
				slist.append(results)
			# results = {'cats' : slist} 
			self.response.write(json.dumps(slist)) 

			# for s in cats: 
				# results = {'id' : s.key.id(), 'name' : s.name, 'color': s.color, 'nap_spot': s.nap_spot} 
				# self.response.write(json.dumps(results)) 
	
