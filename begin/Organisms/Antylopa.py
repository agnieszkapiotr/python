from Action import Action
from ActionEnum import ActionEnum
from Position import Position
from .Animal import Animal
from .Rys import Rys


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

	def move(self):
		wynik_reakcji = self.reakcja()
		if wynik_reakcji:
			return wynik_reakcji
		else:
			return super().move()

	def reakcja(self):
		sasiednie_pola = self.world.getNeighboringPositions(self.position)
		ryś = None

		for pole in sasiednie_pola:
			organizm = self.world.getOrganismFromPosition(pole)
			if organizm and organizm.sign == 'R':
				ryś = organizm
				break

		if not ryś:
			return []

		roznica_x = self.position.x - ryś.position.x
		roznica_y = self.position.y - ryś.position.y

		pola_ucieczki = []

		if roznica_x != 0:
			nowe_x = self.position.x + (2 if roznica_x < 0 else -2)
			nowe_pole = Position(xPosition=nowe_x, yPosition=self.position.y)
			if self.world.positionOnBoard(nowe_pole):
				pola_ucieczki.append(nowe_pole)

		if roznica_y != 0:
			nowe_y = self.position.y + (-2 if roznica_y < 0 else 2)
			nowe_pole = Position(xPosition=self.position.x, yPosition=nowe_y)
			if self.world.positionOnBoard(nowe_pole):
				pola_ucieczki.append(nowe_pole)

		for pole in pola_ucieczki:
			if self.world.getOrganismFromPosition(pole) is None:
				print(f"[ANTYLOPA] Ryś wykryty na {ryś.position} → ucieczka na {pole}")
				return [Action(ActionEnum.A_MOVE, pole, 0, self)]

		print(f"[ANTYLOPA] Ryś wykryty na {ryś.position} → brak drogi ucieczki, walczę")
		return [Action(ActionEnum.A_REMOVE, None, 0, ryś)]
