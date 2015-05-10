import webapp2


application = webapp2.WSGIApplication([


	(r'/category', 'category.Category'),
	(r'/item', 'item.Item'),
	(r'/business', 'business.Business'),
	(r'/', 'front.Front'), 
	(r'/add_new', 'add_new.MainPage'),
], debug=True)
 
 
 