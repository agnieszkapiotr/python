import unittest
from InvoiceRepository import InvoiceRepository
from Shop import Shop
from Invoice import Invoice
from Magazyn import Magazyn, OutOfStore


class ShopTests(unittest.TestCase):

    def test_tresc_faktury_po_zakupie(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        mag.przyjecie("papier", 10, 19)
        customer = "Marian Mariusz"
        items = ["papier"]
        invoice = shop.buy(customer, items)
        self.assertEqual(invoice.number, 1)
        self.assertEqual(invoice.customer, "Marian Mariusz")
        self.assertEqual(invoice.items, {"papier": (1, 19)})


    def test_magazyn_po_zakupie_dwa_razy_tego_samego_produktu(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        customer = "Marian Mariusz"
        mag.przyjecie("papier", 3, 19)
        items = ["papier", "papier"]
        shop.buy(customer, items)
        self.assertEqual(mag.inventory["papier"], (1, 19))

    def test_czy_ilosc_produktu_spada_do_0_po_zakupie_calej_ilosci(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        customer = "Marian Mariusz"
        mag.przyjecie("papier", 1, 19)
        items = ["papier"]
        shop.buy(customer, items)
        self.assertEqual(mag.inventory["papier"], (0, 19))

    def test_proba_zakupu_produktu_ktorego_ilosc_wynosi_0(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        customer = "Marian Mariusz"
        mag.przyjecie("papier", 0, 19)
        items = ["papier"]
        with self.assertRaises(OutOfStore) as context: 
            shop.buy(customer, items)


    def test_zakup_produktu_ktorego_nie_ma_w_magazynie(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        customer = "Marian Mariusz"
        items = ["papier"]
        with self.assertRaises(OutOfStore) as context: 
            shop.buy(customer, items)
        self.assertIn("papier", str(context.exception)) 
        


    def test_wydanie_produktu_z_magazynu_po_zakupie(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        mag.przyjecie("kasza", 10, 15)
        mag.przyjecie("ziemniak", 60, 2)
        mag.przyjecie("kurczak", 10, 20)
        customer = "Marian Mariusz"
        items = ["ziemniak", "kurczak"]
        shop.buy(customer, items)
        self.assertEqual(mag.inventory["ziemniak"], (59, 2))
        self.assertEqual(mag.inventory["kurczak"], (9, 20))

    def test_magazyn_po_zwrocie_calej_faktury(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        mag.przyjecie("ziemniak", 10, 2)
        customer = "Marian Mariusz"
        items = ["ziemniak"]
        invoice = shop.buy(customer, items)
        self.assertEqual(mag.inventory["ziemniak"], (9, 2))
        shop.returning_goods(invoice)
        self.assertEqual(mag.inventory["ziemniak"], (10, 2))

    def test_magazyn_po_czesciowym_zwrocie(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        mag.przyjecie("ziemniak", 10, 2)
        mag.przyjecie("cukinia", 5, 8)
        customer = "Marian Mariusz"
        items = ["ziemniak", "ziemniak", "ziemniak", "cukinia", "cukinia"]
        invoice = shop.buy(customer, items)
        self.assertEqual(mag.inventory["ziemniak"], (7, 2))
        self.assertEqual(mag.inventory["cukinia"], (3, 8))
        shop.czesciowy_zwrot(invoice, ["ziemniak", "cukinia", "cukinia"])
        self.assertEqual(mag.inventory["ziemniak"], (8, 2))
        self.assertEqual(mag.inventory["cukinia"], (5, 8))

    def test_proba_zwrotu_produktu_ktorego_nie_ma_na_fakturze(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        mag.przyjecie("ziemniak", 10, 2)
        customer = "Marian Mariusz"
        items = ["ziemniak"]
        invoice = shop.buy(customer, items)
        with self.assertRaises(Exception) as context: 
            shop.czesciowy_zwrot(invoice, ["cebula"])
        self.assertIn("cebula", str(context.exception)) 



    def test_czy_faktury_maja_unikalne_rosnace_numery(self):
        repo = InvoiceRepository()
        mag = Magazyn()
        shop = Shop(repository=repo, magazyn = mag)
        mag.przyjecie("ziemniak", 10, 2)
        customer = "Robert Lewandowski"
        faktury = []
        for i in range(6):
            invoice = shop.buy(customer, ["ziemniak"])
            faktury.append(invoice.number)
        self.assertEqual(len(faktury), len(set(faktury)))
        self.assertEqual(faktury, sorted(faktury))

    


class TestMagazyn(unittest.TestCase):

    def test_przyjecie_produktu_do_magazynu(self):
        magazyn = Magazyn()
        magazyn.przyjecie("Kasza", 5, 15)
        self.assertIn("Kasza", magazyn.inventory)
        self.assertEqual(magazyn.inventory["Kasza"], (5, 15))

    def test_przyjecie_dwa_razy_tego_samego_produktu(self):
        magazyn = Magazyn()
        magazyn.przyjecie("ogórek", 1, 4)
        magazyn.przyjecie("ogórek", 1, 4)
        self.assertEqual(magazyn.inventory["ogórek"], (2, 4))

    def test_przyjecie_produktu_z_ujemna_iloscia(self):
        magazyn = Magazyn()
        with self.assertRaises(Exception) as context:
            magazyn.przyjecie("ogórek", -5, 4)

    def test_przyjecie_produktu_z_ujemna_cena(self):
        magazyn = Magazyn()
        with self.assertRaises(Exception) as context:
            magazyn.przyjecie("ogórek", 5, -4)


    def test_wydanie_produktu_z_magazynu(self):
        magazyn = Magazyn()
        magazyn.przyjecie("ziemniak", 10, 5)
        magazyn.wydanie("ziemniak")
        self.assertEqual(magazyn.inventory["ziemniak"], (9, 5))

    def test_wydanie_produktu_z_magazynu_gdy_ilosc_jest_0(self):
        magazyn = Magazyn()
        magazyn.przyjecie("ziemniak", 0, 5)
        with self.assertRaises(OutOfStore) as context: 
            magazyn.wydanie("ziemniak")
        
        



if __name__ == "__main__":
    unittest.main()