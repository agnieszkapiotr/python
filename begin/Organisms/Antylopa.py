from .Animal import Animal


class Antylopa(Animal):

	def __init__(self, antylopa=None, position=None, world=None):
		super(Antylopa, self).__init__(antylopa, position, world)

	def clone(self):
		return Antylopa(self, None, None)

	def initParams(self):
		self.power = 4
		self.initiative = 3
		self.liveLength = 11
		self.powerToReproduce = 5
		self.sign = 'A'

	def getNeighboringPosition(self):
		return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))
	