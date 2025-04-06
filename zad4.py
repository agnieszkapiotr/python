
def porownanie(data1, data2):
    if data1["rok"] > data2["rok"]:
        return True
    elif data1["rok"] == data2["rok"]:
        if data1["miesiac"] > data2["miesiac"]:
            return True
        elif data1["miesiac"] == data2["miesiac"]:
            if data1["dzien"] > data2["dzien"]:
                return True
    return False


def sortowanie(daty):
    liczba = len(daty)
    for i in range(liczba):
        for j in range(0, liczba-i-1):
            if porownanie(daty[j], daty[j+1]):
                daty[j], daty[j+1] = daty[j+1], daty[j]
    return [f"{d['dzien']:02d}.{d['miesiac']:02d}.{d['rok']}" for d in daty]


liczba = int(input("Podaj liczbę dat"))
daty=[]
for i in range(liczba):
    dzien = int(input("Podaj dzień: "))
    miesiac = int(input("Podaj miesiac: "))
    rok = int(input("Podaj rok: "))
    slownikdata = {"dzien": dzien, "miesiac": miesiac, "rok": rok}
    daty.append(slownikdata)

print(f"Posortowane daty: {sortowanie(daty)}")
