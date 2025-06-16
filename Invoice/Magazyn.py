""" 
Rozszerzyć implementację o magazyn produktów, który podobnie jak repozytorium faktur będzie parametrem konstrukcji sklepu.
Magazyn powinien posiadać wiedzę o dostęnych produktach, ich ilościach i cenach. 
Dodatkowo powinien oferować operacje przyjęcia na magazym oraz wydania z magazynu. 
Próba wydania z magazynu produktu o zerowym stanie mgazynowym powinna generować wyjątek OutOfStore. 
W sklepie powinna być dostępna operacja zwrotu częściowego towarów z danej faktury.
Każda sprzedaż oraz zwrot prócz repozytorium faktur zmieniają również stany magazynowe."""

class Magazyn:
    def __init__(self, inventory = None):
        if inventory is None:
            inventory = {}
        self._inventory = inventory

    def przyjecie(self, produkt, ilosc, cena):
        if ilosc < 0:
            raise ValueError(f"Produkt nie może mieć ujemnej ilości.")
        if cena < 0:
            raise ValueError(f"Produkt nie może mieć ujemnej ceny.")
        if produkt in self._inventory:
            aktualna_ilosc, aktualna_cena = self._inventory[produkt]
            if aktualna_cena != cena:
                raise ValueError(f"Produkt '{produkt}' ma różne ceny: {aktualna_cena} i {cena}")
            else:
                self._inventory[produkt] = (aktualna_ilosc + ilosc, cena)
        else:
            self._inventory[produkt] = (ilosc, cena)

    def wydanie(self, produkt):
        if produkt not in self._inventory:
            raise OutOfStore(f"Produkt '{produkt}' nie istnieje w magazynie.")
        ilosc, cena = self._inventory[produkt]
        if ilosc > 0:
            self._inventory[produkt] = (ilosc -1, cena)
        else: 
            raise OutOfStore(f"Produkt '{produkt}' jest niedostępny.")
        
    @property
    def inventory(self):
        return self._inventory
        

        
class OutOfStore(Exception):
    def __init__(self, message = "Brak podanego produktu w magazynie."):
        self.message = message
        super().__init__(self.message)
    


