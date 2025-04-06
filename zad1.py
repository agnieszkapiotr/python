"""Liczby pierwsze"""
def czy_pierwsza(n):
    if n < 2:
        return False
    for i in range(2, int((n**0.5)+1)):
        if n%i == 0:
            return False
    return True

def pierwsze(od, do):
    for i in range(od, do + 1):
        if czy_pierwsza(i):
            print(i)


od = int(input("Podaj dolną granicę: "))
do = int(input("Podaj górną granicę: "))
pierwsze(od, do)

