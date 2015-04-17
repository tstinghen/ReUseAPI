import webapp2


application = webapp2.WSGIApplication([


	(r'/category', 'category.Category'),
	(r'/item', 'item.Item'),
	(r'/', 'front.Front'), 
], debug=True)
 
 
 