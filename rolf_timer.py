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


@get_runtime
def rolf_5():
    bestand = open('input/day_5.txt', 'r')
    alles = bestand.readlines()
    templijst = []
    horizontaal = []
    verticaal = []

    # tekst splitsen en in getallen omzetten:
    for sliert in range(len(alles)):
        templijst.append(alles[sliert].split(" -> "))
    for sliert in range(len(templijst)):
        for ding in range(2):
            templijst[sliert][ding] = templijst[sliert][ding].split(",")
            for dong in range(2):
                templijst[sliert][ding][dong] = int(templijst[sliert][ding][dong])

    # alleen rechte slierten:
    for sliert in range(len(templijst)):
        hori = False
        verti = False
        if templijst[sliert][0][1] == templijst[sliert][1][1]:
            hori = True
        elif templijst[sliert][0][0] == templijst[sliert][1][0]:
            verti = True
        if hori == True:
            horizontaal.append(templijst[sliert])
        if verti == True:
            verticaal.append(templijst[sliert])

    # alles de goede kant op draaien:
    for sliert in range(len(horizontaal)):
        if horizontaal[sliert][0][0] > horizontaal[sliert][1][0]:
            omdraaien = horizontaal[sliert][1][0]
            horizontaal[sliert][1][0] = horizontaal[sliert][0][0]
            horizontaal[sliert][0][0] = omdraaien
    for sliert in range(len(verticaal)):
        if verticaal[sliert][0][1] > verticaal[sliert][1][1]:
            omdraaien = verticaal[sliert][1][1]
            verticaal[sliert][1][1] = verticaal[sliert][0][1]
            verticaal[sliert][0][1] = omdraaien

    # tussendingen toevoegen:
    for sliert in range(len(horizontaal)):
        for tussen in range((horizontaal[sliert][1][0] - horizontaal[sliert][0][0]) - 1):
            horizontaal[sliert].append([horizontaal[sliert][0][0] + tussen + 1, horizontaal[sliert][0][1]])
    for sliert in range(len(verticaal)):
        for tussen in range((verticaal[sliert][1][1] - verticaal[sliert][0][1]) - 1):
            verticaal[sliert].append([verticaal[sliert][0][0], verticaal[sliert][0][1] + tussen + 1])

    # antwoord uitrekenen:
    superlijst = []
    schijtlijst = []
    antwoord = 0
    for sliert in range(len(horizontaal)):
        for pixel in range(len(horizontaal[sliert])):
            if horizontaal[sliert][pixel] in superlijst:
                if horizontaal[sliert][pixel] not in schijtlijst:
                    antwoord = antwoord + 1
                    schijtlijst.append(horizontaal[sliert][pixel])
            else:
                superlijst.append(horizontaal[sliert][pixel])
    for sliert in range(len(verticaal)):
        for pixel in range(len(verticaal[sliert])):
            if verticaal[sliert][pixel] in superlijst:
                if verticaal[sliert][pixel] not in schijtlijst:
                    antwoord = antwoord + 1
                    schijtlijst.append(verticaal[sliert][pixel])
            else:
                superlijst.append(verticaal[sliert][pixel])

    print(antwoord)


vissen = [1, 2, 5, 1, 1, 4, 1, 5, 5, 5, 3, 4, 1, 2, 2, 5, 3, 5, 1, 3, 4, 1, 5, 2, 5, 1, 4, 1, 2, 2, 1, 5, 1, 1, 1,
          2, 4, 3, 4, 2, 2, 4, 5, 4, 1, 2, 3, 5, 3, 4, 1, 1, 2, 2, 1, 3, 3, 2, 3, 2, 1, 2, 2, 3, 1, 1, 2, 5, 1, 2,
          1, 1, 3, 1, 1, 5, 5, 4, 1, 1, 5, 1, 4, 3, 5, 1, 3, 3, 1, 1, 5, 2, 1, 2, 4, 4, 5, 5, 4, 4, 5, 4, 3, 5, 5,
          1, 3, 5, 2, 4, 1, 1, 2, 2, 2, 4, 1, 2, 1, 5, 1, 3, 1, 1, 1, 2, 1, 2, 2, 1, 3, 3, 5, 3, 4, 2, 1, 5, 2, 1,
          4, 1, 1, 5, 1, 1, 5, 4, 4, 1, 4, 2, 3, 5, 2, 5, 5, 2, 2, 4, 4, 1, 1, 1, 4, 4, 1, 3, 5, 4, 2, 5, 5, 4, 4,
          2, 2, 3, 2, 1, 3, 4, 1, 5, 1, 4, 5, 2, 4, 5, 1, 3, 4, 1, 4, 3, 3, 1, 1, 3, 2, 1, 5, 5, 3, 1, 1, 2, 4, 5,
          3, 1, 1, 1, 2, 5, 2, 4, 5, 1, 3, 2, 4, 5, 5, 1, 2, 3, 4, 4, 1, 4, 1, 1, 3, 3, 5, 1, 2, 5, 1, 2, 5, 4, 1,
          1, 3, 2, 1, 1, 1, 3, 5, 1, 3, 2, 4, 3, 5, 4, 1, 1, 5, 3, 4, 2, 3, 1, 1, 4, 2, 1, 2, 2, 1, 1, 4, 3, 1, 1,
          3, 5, 2, 1, 3, 2, 1, 1, 1, 2, 1, 1, 5, 1, 1, 2, 5, 1, 1, 4]


@get_runtime
def rolf_6a():
    visleeftijden = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for x in range(len(vissen)):
        visleeftijden[vissen[x]] = visleeftijden[vissen[x]] + 1

    for x in range(80):
        visleeftijden[9] = visleeftijden[0]
        visleeftijden.pop(0)
        visleeftijden[6] = visleeftijden[6] + visleeftijden[8]
        visleeftijden.append(0)

    antwoord = 0
    for x in range(9):
        antwoord = antwoord + visleeftijden[x]

    # print(antwoord)


@get_runtime
def rolf_6b():
    visleeftijden = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for x in range(len(vissen)):
        visleeftijden[vissen[x]] = visleeftijden[vissen[x]] + 1

    for x in range(256):
        visleeftijden[9] = visleeftijden[0]
        visleeftijden.pop(0)
        visleeftijden[6] = visleeftijden[6] + visleeftijden[8]
        visleeftijden.append(0)

    antwoord = 0
    for x in range(9):
        antwoord = antwoord + visleeftijden[x]

    # print(antwoord)


if __name__ == '__main__':
    # rolf_dag_4a()
    # rolf_dag_4b()
    rolf_5()
    rolf_6a()
    rolf_6b()
