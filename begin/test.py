import unittest
from unittest.mock import MagicMock, patch
from World import World
from Position import Position
from Organisms.Antylopa import Antylopa
from Organisms.Rys import Rys
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Action import Action
from ActionEnum import ActionEnum

class TestAntylopa(unittest.TestCase):
    def setUp(self):
        self.swiat = MagicMock()
        self.antylopa = Antylopa(position=Position(xPosition=5, yPosition=5), world=self.swiat)

    def test_reakcja_ucieczka(self):
        rys = MagicMock()
        rys.sign = 'R'
        rys.position = Position(xPosition=5, yPosition=6)
        
        self.swiat.getNeighboringPositions.return_value = [
            Position(xPosition=5, yPosition=4),
            Position(xPosition=5, yPosition=6),
            Position(xPosition=4, yPosition=5),
            Position(xPosition=6, yPosition=5)
        ]

        def getOrganismFromPosition(pos):
            if pos.x == 5 and pos.y == 6:
                return rys
            return None
        
        self.swiat.getOrganismFromPosition.side_effect = getOrganismFromPosition
        self.swiat.positionOnBoard.return_value = True
        
        akcje = self.antylopa.reakcja()
        self.assertEqual(len(akcje), 1)
        self.assertEqual(akcje[0].action, ActionEnum.A_MOVE)
        self.assertIn(abs(akcje[0].position.x - self.antylopa.position.x), [0, 2])
        self.assertIn(abs(akcje[0].position.y - self.antylopa.position.y), [0, 2])

class TestPlague(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10)
        self.rys = Rys(position=Position(xPosition=1, yPosition=1), world=self.world)
        self.antylopa = Antylopa(position=Position(xPosition=2, yPosition=2), world=self.world)

        self.rys.liveLength = 20
        self.antylopa.liveLength = 20
        
        self.world.addOrganism(self.rys)
        self.world.addOrganism(self.antylopa)

    def test_plaga_skraca_zycie(self):
        print("\nTEST: Plaga skraca życie istniejącym organizmom...")
        
        initial_rys = self.rys.liveLength
        initial_antylopa = self.antylopa.liveLength

        self.world.wlacz_plage()
        self.world.makeTurn() 

        expected_rys = (initial_rys // 2) - 1
        expected_antylopa = (initial_antylopa // 2) - 1
        
        self.assertEqual(self.rys.liveLength, expected_rys, f"Długość życia rysia: oczekiwano {expected_rys}, otrzymano {self.rys.liveLength}")
        self.assertEqual(self.antylopa.liveLength, expected_antylopa, f"Długość życia antylopy: oczekiwano {expected_antylopa}, otrzymano {self.antylopa.liveLength}")
        print("OK")

    def test_plaga_2_tury(self):
        print("\nTEST: Plaga kończy się po 2 turach...")
        self.world.wlacz_plage()
        self.world.makeTurn()
        self.assertTrue(self.world.plaga_aktywna, "Plaga powinna być aktywna po 1 turze")
        
        self.world.makeTurn()
        self.assertFalse(self.world.plaga_aktywna, "Plaga powinna się zakończyć po 2 turach")
        print("OK")

class TestDodajOrganizm(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10)
        self.owca = Sheep(position=Position(xPosition=1, yPosition=1), world=self.world)
        self.world.addOrganism(self.owca)

    def test_dodaj_organizm_poprawne(self):
        print("\nTEST: Poprawne dodanie organizmu...")
        trawa = Grass(position=Position(xPosition=2, yPosition=2), world=self.world)
        
        result = self.world.dodaj_organizm(trawa, Position(xPosition=2, yPosition=2))
        
        self.assertTrue(result)
        self.assertIn(trawa, self.world.organisms)
        print("OK")

    def test_dodaj_organizm_poza_plansza(self):
        print("\nTEST: Próba dodania poza planszę...")
        rys = Rys(position=Position(xPosition=11, yPosition=11), world=self.world)
        
        with patch('builtins.print') as mocked_print:
            result = self.world.dodaj_organizm(rys, Position(xPosition=11, yPosition=11))
            
            self.assertFalse(result)
            mocked_print.assert_called_with(f"Pozycja (11, 11) poza planszą!")
            self.assertNotIn(rys, self.world.organisms)
        print("OK")

    def test_dodaj_organizm_na_zajete_pole(self):
        print("\nTEST: Próba dodania na zajęte pole...")
        antylopa = Antylopa(position=Position(xPosition=1, yPosition=1), world=self.world)
        
        with patch('builtins.print') as mocked_print:
            result = self.world.dodaj_organizm(antylopa, Position(xPosition=1, yPosition=1))
            
            self.assertFalse(result)
            mocked_print.assert_called_with(f"Pozycja (1, 1) jest zajęta!")
            self.assertNotIn(antylopa, self.world.organisms)
        print("OK")


if __name__ == '__main__':
    unittest.main()