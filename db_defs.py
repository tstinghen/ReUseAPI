from google.appengine.ext import ndb 

class Model(ndb.Model): 
	def to_dict(self): 
		d = super(Model, self).to_dict() 
		d['key'] = self.key.id() 
		return d

		
class Category(Model):
	name = ndb.StringProperty(required = True) 
	items = ndb.KeyProperty(repeated = True) 
	
	def to_dict(self): 
		d = super(Category, self).to_dict() 
		d['items'] = [s.id() for s in d['items']]
		return d
	
class Business(Model): 
	name = ndb.StringProperty(required = True)
	phone = ndb.StringProperty(required = True)
	website = ndb.StringProperty(required = True)
	address = ndb.StringProperty(required = True)
	items = ndb.KeyProperty(repeated = True) 
	 
	def to_dict(self): 
		d = super(Business, self).to_dict() 
		d['items'] = [s.id() for s in d['items']]
		return d
		
class Item(Model):
	name = ndb.StringProperty(required = True)
	category = ndb.KeyProperty (repeated = True) 
	businesses = ndb.KeyProperty(repeated = True) 
	
	def to_dict(self): 
		d = super(Item, self).to_dict() 
		d['category'] = [x.id() for x in d['category']]
		d['businesses'] = [s.id() for s in d['businesses']]
		return d
	
		

	
