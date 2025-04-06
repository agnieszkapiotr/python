def sumadzielnikow(liczba):
    suma=0
    for i in range(1, liczba):
        if liczba%i==0:
            suma+=i
    return suma

def czyzaprzyjaznione(liczba1, liczba2):
    if sumadzielnikow(liczba1) == liczba2 and sumadzielnikow(liczba2) == liczba1:
        return True
    return False

liczba1 = int(input("Podaj pierwszą liczbę: "))
liczba2 = int(input("Podaj drugą liczbę: "))
if czyzaprzyjaznione(liczba1, liczba2):
    print(f"Liczby {liczba1} i {liczba2} są zaprzyjaźnione")
else:
    print(f"Liczby {liczba1} i {liczba2} nie są zaprzyjaźnione")

