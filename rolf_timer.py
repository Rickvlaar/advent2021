from util import console, get_runtime


@get_runtime
def rolf_dag_4a():
    bestand = open('input/day_4.txt', 'r')
    alles = bestand.readlines()
    kaarten = []
    bingo = False

    nummers = [25, 8, 32, 53, 22, 94, 55, 80, 33, 4, 63, 14, 60, 95, 31, 89, 30, 5, 47, 66, 84, 70, 17, 74, 99, 82, 21,
               35,
               64, 2, 76, 9, 90, 56, 78, 28, 51, 86, 49, 98, 29, 96, 23, 58, 52, 75, 41, 50, 13, 72, 92, 83, 62, 37, 18,
               11,
               34, 71, 91, 85, 27, 12, 24, 73, 7, 77, 10, 93, 15, 61, 3, 46, 16, 97, 1, 57, 65, 40, 0, 48, 69, 6, 20,
               68,
               19, 45, 42, 79, 88, 44, 26, 38, 36, 54, 81, 59, 43, 87, 39, 67]

    for kaart in range(100):
        dezekaart = []
        for regel in range(5):
            dezekaart.append(alles[(kaart * 6) + regel].split())
        for nummeren in range(5):
            for dinges in range(5):
                dezekaart[nummeren][dinges] = int(dezekaart[nummeren][dinges])
        kaarten.append(dezekaart)
    winnaar = 0
    volgende = 0
    while bingo == False:
        for kaart in range(100):
            for regel in range(5):
                for getal in range(5):
                    if nummers[volgende] == kaarten[kaart][regel][getal]:
                        kaarten[kaart][regel][getal] = 'B'

                        horicheck = True
                        hori = 0
                        while horicheck == True:
                            if kaarten[kaart][regel][hori] != 'B':
                                horicheck = False
                            else:
                                hori = hori + 1
                            if hori == 5:
                                bingo = True
                                print("bingo!")
                                winnaar = kaart
                                horicheck = False

                        verticheck = True
                        verti = 0
                        while verticheck == True:
                            if kaarten[kaart][verti][getal] != 'B':
                                verticheck = False
                            else:
                                verti = verti + 1
                            if verti == 5:
                                bingo = True
                                verticheck = False

        volgende = volgende + 1

    som = 0
    for x in range(5):
        for y in range(5):
            if isinstance(kaarten[winnaar][x][y], int):
                som = som + kaarten[winnaar][x][y]
    # print(som)
    antwoord = som * nummers[volgende - 1]

    # print(antwoord)


@get_runtime
def rolf_dag_4b():
    bestand = open('input/day_4.txt', 'r')
    alles = bestand.readlines()
    kaarten = []
    bingo = 0
    winnaars = []

    nummers = [25, 8, 32, 53, 22, 94, 55, 80, 33, 4, 63, 14, 60, 95, 31, 89, 30, 5, 47, 66, 84, 70, 17, 74, 99, 82, 21,
               35, 64, 2, 76, 9, 90, 56, 78, 28, 51, 86, 49, 98, 29, 96, 23, 58, 52, 75, 41, 50, 13, 72, 92, 83, 62, 37,
               18, 11, 34, 71, 91, 85, 27, 12, 24, 73, 7, 77, 10, 93, 15, 61, 3, 46, 16, 97, 1, 57, 65, 40, 0, 48, 69,
               6, 20, 68, 19, 45, 42, 79, 88, 44, 26, 38, 36, 54, 81, 59, 43, 87, 39, 67]

    for kaart in range(100):
        dezekaart = []
        for regel in range(5):
            dezekaart.append(alles[(kaart * 6) + regel].split())
        for nummeren in range(5):
            for dinges in range(5):
                dezekaart[nummeren][dinges] = int(dezekaart[nummeren][dinges])
        kaarten.append(dezekaart)

    volgende = 0
    while bingo < 99:
        gewonnen = False
        for kaart in range(len(kaarten)):
            for regel in range(5):
                for getal in range(5):
                    if nummers[volgende] == kaarten[kaart][regel][getal]:
                        kaarten[kaart][regel][getal] = 'B'

                        horicheck = True
                        horiwin = False
                        hori = 0
                        while horicheck == True:
                            if kaarten[kaart][regel][hori] != 'B':
                                horicheck = False
                            else:
                                hori = hori + 1
                            if hori == 5:
                                bingo = bingo + 1
                                gewonnen = True
                                winnaars.append(kaart)
                                horicheck = False
                                horiwin = True

                        verticheck = False
                        if horiwin == False:
                            verticheck = True
                        verti = 0
                        while verticheck == True:
                            if kaarten[kaart][verti][getal] != 'B':
                                verticheck = False
                            else:
                                verti = verti + 1
                            if verti == 5:
                                bingo = bingo + 1
                                gewonnen = True
                                winnaars.append(kaart)
                                verticheck = False
        if gewonnen == True:
            for x in range(len(winnaars)):
                kaarten.pop(winnaars[len(winnaars) - 1 - x])
            gewonnen = False
            winnaars = []
        volgende = volgende + 1

    for regel in range(5):
        for getal in range(5):
            if nummers[volgende] == kaarten[0][regel][getal]:
                kaarten[0][regel][getal] = 'B'

    som = 0
    for x in range(5):
        for y in range(5):
            if isinstance(kaarten[0][x][y], int):
                som = som + kaarten[0][x][y]

    antwoord = som * nummers[volgende]

    # print(antwoord)


if __name__ == '__main__':
    rolf_dag_4a()
    rolf_dag_4b()
