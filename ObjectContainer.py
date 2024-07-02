class ObjectContainer:
	def __init__(self):
		self.objects = []
		self.deleted = []
		self.count   = 0
		self.lastOperation = None
		
	def add(self, WHO):
		if len(self.deleted) > 0:
			id = self.deleted.pop()
			self.objects[id] = WHO
			self.count += 1
			self.lastOperation = "add({}) with ID: {}".format(WHO, id)
			return id
		else:
			self.objects.append( WHO )
			self.count += 1
			self.lastOperation = "add({}) with ID: {}".format(WHO, len(self.objects) - 1)
			return len(self.objects) - 1
		
	def remove(self, ID):
		if self.objects[ID]:
			self.lastOperation = "remove({})".format(ID)
			self.objects[ID] = None
			self.deleted.append( ID )
			self.count -= 1
			if self.count == 0:
				self.deleted.clear()
				self.objects.clear()
			return len(self.objects)
	
	def getCount(self):
		return self.count
	
	def debug(self):
		print("\n---- OBJECTCONTAINER ----")
		print("COUNT:", self.count)
		print("DELETED:", self.deleted)
		print("OBJECTS:", self.objects)
		print("LAST OPERATION:", self.lastOperation)