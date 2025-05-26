from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Rys import Rys
from Organisms.Antylopa import Antylopa
import os


if __name__ == '__main__':
	pyWorld = World(10, 10)

	newOrg = Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Sheep(position=Position(xPosition=2, yPosition=2), world=pyWorld)
	pyWorld.addOrganism(newOrg)


	newOrg = Rys(position=Position(xPosition=4, yPosition=4), world=pyWorld)
	pyWorld.addOrganism(newOrg)

	newOrg = Antylopa(position=Position(xPosition=5, yPosition=4), world=pyWorld)
	pyWorld.addOrganism(newOrg)



	print(pyWorld)

	for _ in range(50):
		komenda = input("Naciśnij Enter by kontynuować, 'P' by włączyć plagę, 'D' by dodać organizm: ").strip().upper()
		
		if komenda == 'P':
			pyWorld.wlacz_plage()
		elif komenda == 'D':
			typ = input("Podaj literkę organizmu (G- Grass, S - Sheep, R - Rys, A - Antylopa): ").strip().upper()
			
			typy_org = {"G": Grass, "S": Sheep, "R": Rys, "A": Antylopa}
			
			if typ not in typy_org:
				print("Nieznany typ organizmu!")
			else:
				x = int(input("Podaj współrzędną x: "))
				y = int(input("Podaj wspołrzędną y: "))
				
				nowy_org = typy_org[typ](position=Position(xPosition=x, yPosition=y), world=pyWorld)
				pyWorld.dodaj_organizm(nowy_org, Position(xPosition=x, yPosition=y))
		else:
			os.system('cls')
			pyWorld.makeTurn()
			print(pyWorld)

