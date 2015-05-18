import webapp2


application = webapp2.WSGIApplication([


	(r'/category', 'category.Category'),
	(r'/edit_category', 'edit_category.EditPage'), 
	(r'/item', 'item.Item'),
	(r'/business', 'business.Business'),
	(r'/edit_business', 'edit_business.EditPage'), 
	(r'/', 'front.Front'), 
	(r'/add_new', 'add_new.MainPage'),
	(r'/view', 'view.MainPage'), 
	(r'/add_business', 'add_business.MainPage'),
	(r'/item_by_cat', 'item.ItemsByCategory'), 
	(r'/bus_by_item', 'business.BusinessesByItem'), 
	(r'/item_by_bus', 'item.ItemsByBusiness'), 
], debug=True)
 
 
 