from abc import ABC
from Invoice import Invoice
from Magazyn import OutOfStore

"""
W sklepie powinna być dostępna operacja zwrotu częściowego towarów z danej faktury.
Każda sprzedaż oraz zwrot prócz repozytorium faktur zmieniają również stany magazynowe.

"""

class Shop(ABC):
    def __init__(self, repository=None, magazyn=None):
        self.__invoice_repository = repository
        self._magazyn = magazyn

    def buy(self, customer, items_list):
        invoice_items = {}
        for item in items_list:

            try:
                self._magazyn.wydanie(item)
            except OutOfStore as e:
                print(f"Nie można zakupić produktu: {e}")
                raise  
            if item in invoice_items:
                ilosc_faktura, cena_faktura = invoice_items[item]
                invoice_items[item] = (ilosc_faktura + 1, cena_faktura)
            else:
                _, cena = self._magazyn._inventory[item]
                invoice_items[item] = (1, cena)  

        invoice = Invoice(number=self.invoice_repository.get_next_number(), customer=customer, items= invoice_items)
        self.invoice_repository.add(invoice)
        return invoice

    def returning_goods(self, invoice):
        if self.invoice_repository.find_by_number(invoice.number):
            for produkt, (ilosc, cena) in invoice.items.items():
                self._magazyn.przyjecie(produkt, ilosc, cena)
            self.invoice_repository.delete(invoice)
            return True
        else:
            return False
    def czesciowy_zwrot(self, invoice, produkty):
        if self.invoice_repository.find_by_number(invoice.number):
            for produkt in produkty:
                if produkt in invoice.items:
                    ilosc, cena = invoice.items[produkt]
                    self._magazyn.przyjecie(produkt, 1, cena)
                    invoice.items[produkt] = (ilosc - 1, cena)
                else: 
                    raise ValueError(f"Na fakturze nie ma produktu: {produkt}")
            return True
        else:
            return False
        


    @property
    def invoice_repository(self):
        return self.__invoice_repository
