def zolnierze(a):
    bezpieczny=0

    for i in range(1, a+1):
        bezpieczny = (bezpieczny+2)%i
    return bezpieczny + 1

a=int(input("Podaj ilość żołnierzy: "))
print(f"{zolnierze(a)}")

