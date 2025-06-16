import unittest
from unittest.mock import Mock
from Invoice import Invoice
from Shop import Shop
from Magazyn import Magazyn
from InvoiceRepository import InvoiceRepository

class DummyRepository:
    pass

class TestDummy(unittest.TestCase):
    def test_dummy_repository_przekazany_do_shop(self):
        dummy = DummyRepository()
        mag = Magazyn()
        shop = Shop(repository=dummy, magazyn=mag)
        mag.przyjecie("chleb", 5, 3)
        self.assertIn("chleb", mag.inventory)


class StubRepository:
    def find_by_number(self, number):
        return Invoice(number=number, customer="Stub", items={"chleb": (1, 2)})

class TestStub(unittest.TestCase):
    def test_stub_repository_zwraca_fakture(self):
        stub = StubRepository()
        mag = Magazyn()
        shop = Shop(repository=stub, magazyn=mag)
        invoice = stub.find_by_number(999)
        self.assertEqual(invoice.customer, "Stub")
        self.assertEqual(invoice.items, {"chleb": (1, 2)})
    
    def test_stub_zwraca_konkretny_numer_faktury(self):
        stub_repo = Mock()
        stub_repo.add = Mock()
        stub_repo.get_next_number = Mock(return_value=42)  # dokładnie ta metoda jest wywoływana
        magazyn = Magazyn()
        magazyn.przyjecie("ziemniak", 10, 2)
        shop = Shop(repository=stub_repo, magazyn=magazyn)
        invoice = shop.buy("Anna", ["ziemniak"])
        self.assertEqual(invoice.number, 42)

class FakeRepository:
    def __init__(self):
        self._faktury = {}

    def add(self, invoice):
        self._faktury[invoice.number] = invoice

    def find_by_number(self, number):
        return self._faktury.get(number)

class TestFake(unittest.TestCase):
    def test_fake_repository_dziala_jak_maly_storage(self):
        repo = FakeRepository()
        inv = Invoice(1, "Test", {"woda": (1, 5)})
        repo.add(inv)
        self.assertEqual(repo.find_by_number(1), inv)
        self.assertIsNone(repo.find_by_number(2))

    def test_fake_faktury_maja_rosnace_numery(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn=mag)
        mag.przyjecie("ziemniak", 10, 2)
        faktury = [shop.buy("Robert", ["ziemniak"]).number for _ in range(3)]
        self.assertEqual(faktury, [1, 2, 3])

class TestSpy(unittest.TestCase):
    def test_spy_na_magazynie_przy_zwrocie(self):
        magazyn = Magazyn()
        magazyn.przyjecie("makaron", 10, 5)
        spy_magazyn = Mock(wraps=magazyn)
        spy_magazyn._inventory = magazyn._inventory
        shop = Shop(repository=InvoiceRepository(), magazyn=spy_magazyn)
        invoice = shop.buy("Jacek", ["makaron"])
        shop.returning_goods(invoice)
        spy_magazyn.wydanie.assert_called()
        spy_magazyn.przyjecie.assert_called()


class TestMock(unittest.TestCase):
    def test_mock_repository_dodanie_faktury(self):
        mock_repo = Mock()
        mag = Magazyn()
        shop = Shop(repository=mock_repo, magazyn=mag)
        mag.przyjecie("mleko", 2, 5)
        shop.buy("Kasia", ["mleko"])
        self.assertTrue(mock_repo.add.called)
        mock_repo.add.assert_called_once()

    def test_czy_przyjecie_wywolane_z_odpowiednie_argumenty(self):
        magazyn = Magazyn()
        spy_magazyn = Mock(wraps=magazyn)
        spy_magazyn.przyjecie("Kasza", 5, 15)
        spy_magazyn.przyjecie.assert_called_once_with("Kasza", 5, 15)

if __name__ == "__main__":
    unittest.main()