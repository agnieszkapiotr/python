import unittest
from unittest.mock import Mock
from Invoice import Invoice
from Shop import Shop
from Magazyn import Magazyn
from InvoiceRepository import InvoiceRepository


class TestSpy(unittest.TestCase):
 def test_spy_na_magazynie_przy_zwrocie(self):
    magazyn = Magazyn()
    magazyn.przyjecie("makaron", 10, 5)
    spy_magazyn = Mock(wraps=magazyn)
    spy_magazyn._inventory = magazyn._inventory
    shop = Shop(repository=InvoiceRepository(), magazyn=spy_magazyn)
    invoice = shop.buy("Jacek", ["makaron"])
    shop.returning_goods(invoice)
    spy_magazyn.wydanie.assert_called_with("makaron")
    spy_magazyn.przyjecie.assert_called_with("makaron", 1, 5)



class TestMock(unittest.TestCase):
    def test_mock_repository_dodanie_faktury(self):
        mock_repo = Mock()
        mag = Magazyn()
        mag.przyjecie("mleko", 2, 5)
        shop = Shop(repository=mock_repo, magazyn=mag)
        invoice = shop.buy("Kasia", ["mleko"])

        self.assertTrue(mock_repo.add.called)
        mock_repo.add.assert_called_once()
        dodana_faktura = mock_repo.add.call_args[0][0]
        self.assertEqual(dodana_faktura.customer, "Kasia")
        self.assertIn("mleko", dodana_faktura.items)
        self.assertEqual(dodana_faktura.items["mleko"][0], 1)

    def test_czy_przyjecie_wywolane_z_odpowiednie_argumenty(self):
        magazyn = Magazyn()
        spy_magazyn = Mock(wraps=magazyn)
        spy_magazyn.przyjecie("Kasza", 5, 15)
        spy_magazyn.przyjecie.assert_called_once_with("Kasza", 5, 15)


class TestStub(unittest.TestCase):
    def test_stub_zwraca_konkretny_numer_faktury(self):
        stub_repo = Mock()
        stub_repo.add = Mock()
        stub_repo.get_next_number = Mock(return_value=42)
        magazyn = Magazyn()
        magazyn.przyjecie("ziemniak", 10, 2)
        shop = Shop(repository=stub_repo, magazyn=magazyn)
        invoice = shop.buy("Anna", ["ziemniak"])

        self.assertEqual(invoice.number, 42)
        spy_magazyn = Mock(wraps=magazyn)
        spy_magazyn._inventory = magazyn._inventory
        shop2 = Shop(repository=stub_repo, magazyn=spy_magazyn)
        shop2.buy("Anna", ["ziemniak"])
        spy_magazyn.wydanie.assert_called_once_with("ziemniak")

if __name__ == "__main__":
    unittest.main()