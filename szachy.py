import random

def generowanie_planszy(k):
    #if k>5:
        #raise ValueError("Podano nieprawidłową liczbę hetmanów.")
        

    plansza = []
    for i in range(8):
        wiersz = []
        for j in range(8):
            wiersz.append('*')
        plansza.append(wiersz)

    lista_pul = []
    for i in range(8):
        for j in range(8):
            lista_pul.append((i, j))

    wylosowane_pola = random.sample(lista_pul, k+1)

    for i in range(k):
        x,y=wylosowane_pola[i]
        plansza[x][y]='H'

    x,y=wylosowane_pola[-1]
    plansza[x][y] = 'P'

    return plansza

def pola_hetmanow(plansza):
    hetmani = []
    for i in range(8):
        for j in range(8):
            if plansza[i][j] == 'H':
                hetmani.append((i, j))
    return hetmani

def pole_pionka(plansza):
    for i in range(8):
        for j in range(8):
            if plansza[i][j]=='P':
                return (i, j)

def czy_pionek_zagrozony(hx, hy, px, py):
    return hx == px or hy == py or abs(hx - px) == abs(hy - py)

def sprawdz_ataki(plansza):
    hetmani = pola_hetmanow(plansza)
    px, py = pole_pionka(plansza)
    atakujace = []
    for hx, hy in hetmani:
        if czy_pionek_zagrozony(hx, hy, px, py):
            atakujace.append((hx, hy))
    return atakujace

def usun_hetmana(plansza):

    x = int(input("Podaj wiersz hetmana do usunięcia (0–7): "))
    y = int(input("Podaj kolumnę hetmana do usunięcia (0–7): "))
        
    if (x, y) in pola_hetmanow(plansza):
        plansza[x][y] = '*'
        print(f"Hetman na pozycji ({x}, {y}) został usunięty.")
    else:
        print("Nieprawidłowe pole hetmana.")
 


def wylosuj_nowa_pozycje_pionka(plansza):
    zajete_pola = pola_hetmanow(plansza)

    lista_pul=[]
    for i in range(8):
        for j in range(8):
            lista_pul.append((i, j))

    wolne_pola = []
    for pole in lista_pul:
        if pole not in zajete_pola:
            wolne_pola.append(pole)

    px, py = pole_pionka(plansza)
    plansza[px][py] = '*'

    px2, py2 = random.choice(wolne_pola)
    plansza[px2][py2] = 'P'
    print(f"\n♟️Nowe pole pionka: ({px2}, {py2})")


while True:
    k = int(input("Podaj liczbę hetmanów (1-5): "))
    if 1<=k<=5:
        plansza = generowanie_planszy(int(k))
        break
    print("Podano nieprawidłową liczbę hetmanów :( Spróbuj Ponownie ")

#k = int(input("Podaj liczbę hetmanów: "))
plansza = generowanie_planszy(k)
while True:
    print("\n====PLANSZA====")
    for wiersz in plansza:
        print(' '.join(wiersz))

    atakujacy_hetmani = sprawdz_ataki(plansza)

    if atakujacy_hetmani:
        print("\n!!!♟️Pionek jest zagrożony♟️!!!")
        print("Hetmani, którzy mogą go zbić: ")
        for pole in atakujacy_hetmani:
            print(f"👑 Hetman na pozycji {pole}")
        print("\nWybierz opcję:")
        print("1 - Wylosuj nową pozycję dla pionka")
        print("2 - Usuń hetmana z planszy")
        print("3 - Zakończ")
        wybor = int(input("Twój wybór: "))

        if wybor == 1:
            wylosuj_nowa_pozycje_pionka(plansza)

        elif wybor == 2: 
            usun_hetmana(plansza)

        elif wybor == 3:
            break
        else:
            print("❌Nieprawidłowy wybór❌")
    else:
        print("✅Pionek jest bezpieczny! :D✅")
        break
