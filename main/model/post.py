class Post():
	def __init__(self, city, catagories, sub_City, price, image_filename, 
		description, contact_information, kebele, video_filename  ):
		self.city =city
		self.catagories = catagories
		self.sub_City= sub_City
		self.price = price
		self.image_filename = image_filename
		self.description = description
		self.contact_information = contact_information
		self.kebele = kebele
		self.video_filename = video_filename

	def fromJson(self, mapa):
		for listing in mapa:
	        listing_info = {'city': listing.city, 
	        'catagories': listing.catagories, 
	        'sub_City': listing.sub_City, 
	        'price': listing.price, 'image_filename': listing.image_filename, 'description': listing.description, 'contact_information': listing.contact_information, 'kebele': listing.kebele, 'video_filename': listing.video_filename}
	    return listing_info