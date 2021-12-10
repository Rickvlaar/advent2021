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


@get_runtime
def rolf_7a():
    krabben = [1101, 1, 29, 67, 1102, 0, 1, 65, 1008, 65, 35, 66, 1005, 66, 28, 1, 67, 65, 20, 4, 0, 1001, 65, 1, 65,
               1106, 0, 8, 99, 35, 67, 101, 99, 105, 32, 110, 39, 101, 115, 116, 32, 112, 97, 115, 32, 117, 110, 101,
               32, 105, 110, 116, 99, 111, 100, 101, 32, 112, 114, 111, 103, 114, 97, 109, 10, 478, 1187, 253, 1892,
               900, 155, 20, 787, 17, 248, 1397, 407, 167, 686, 638, 1020, 960, 124, 840, 220, 1824, 700, 373, 4, 551,
               229, 294, 567, 254, 350, 1144, 679, 124, 361, 145, 483, 335, 202, 1334, 367, 60, 870, 11, 557, 482, 645,
               672, 1296, 1538, 427, 78, 542, 1135, 13, 65, 0, 140, 705, 13, 642, 187, 1085, 36, 1118, 349, 601, 382,
               584, 941, 26, 949, 200, 763, 198, 430, 204, 1352, 1135, 210, 342, 11, 1089, 830, 1523, 9, 523, 167, 762,
               254, 805, 8, 132, 29, 102, 1299, 936, 756, 59, 134, 183, 235, 316, 139, 48, 182, 44, 88, 213, 113, 93,
               169, 565, 601, 1899, 1191, 189, 796, 770, 32, 1183, 365, 374, 867, 918, 1084, 86, 75, 20, 47, 99, 1140,
               2, 99, 1024, 366, 455, 752, 556, 1220, 66, 326, 450, 213, 1, 342, 756, 49, 675, 160, 280, 68, 221, 193,
               379, 88, 179, 94, 16, 109, 570, 1145, 1207, 824, 355, 1389, 1601, 168, 86, 236, 923, 120, 759, 14, 478,
               460, 84, 167, 1723, 1005, 269, 6, 171, 861, 311, 832, 952, 701, 3, 1598, 1466, 96, 780, 57, 161, 631,
               572, 276, 105, 594, 276, 17, 405, 688, 1444, 173, 23, 199, 177, 689, 19, 565, 472, 151, 986, 76, 379,
               1430, 212, 928, 106, 25, 143, 84, 833, 942, 860, 1555, 271, 239, 720, 596, 1209, 235, 535, 361, 1794, 79,
               283, 275, 17, 342, 1687, 1434, 173, 967, 740, 217, 1370, 18, 1579, 1259, 546, 94, 623, 475, 834, 1000,
               456, 101, 520, 120, 1023, 360, 167, 213, 617, 42, 1149, 629, 760, 17, 33, 27, 1347, 414, 646, 1116, 1340,
               134, 259, 143, 407, 249, 328, 968, 677, 241, 438, 98, 313, 27, 791, 1, 634, 3, 918, 1482, 213, 123, 444,
               45, 24, 26, 26, 1203, 64, 67, 1562, 1, 4, 298, 12, 384, 32, 443, 37, 268, 674, 356, 202, 286, 694, 272,
               163, 950, 1022, 54, 59, 21, 73, 519, 462, 106, 76, 1112, 10, 72, 388, 194, 6, 120, 9, 645, 209, 1121, 75,
               599, 362, 661, 439, 69, 62, 339, 390, 23, 1247, 365, 1266, 4, 246, 511, 47, 467, 134, 276, 497, 130, 458,
               427, 669, 1191, 701, 917, 168, 1191, 294, 641, 236, 801, 375, 106, 872, 800, 87, 356, 583, 1096, 253,
               459, 951, 1331, 719, 66, 1091, 525, 15, 370, 290, 141, 1201, 30, 43, 37, 76, 1131, 616, 297, 172, 402,
               1016, 654, 301, 63, 872, 303, 69, 1195, 502, 351, 52, 1659, 86, 104, 294, 807, 166, 120, 190, 333, 60,
               283, 819, 198, 184, 144, 278, 343, 1395, 496, 103, 705, 485, 172, 642, 225, 181, 583, 188, 38, 436, 801,
               91, 5, 634, 180, 28, 20, 146, 488, 676, 121, 420, 965, 220, 1564, 1011, 241, 423, 3, 1631, 709, 106, 725,
               164, 1032, 65, 205, 503, 188, 397, 1072, 49, 121, 761, 721, 249, 418, 87, 126, 258, 712, 500, 435, 157,
               127, 681, 108, 270, 647, 504, 505, 83, 407, 212, 165, 1177, 160, 715, 1292, 491, 195, 141, 25, 829, 1316,
               242, 754, 364, 1707, 33, 594, 434, 488, 368, 298, 183, 1156, 29, 1674, 537, 378, 8, 9, 860, 240, 571,
               749, 471, 331, 501, 156, 62, 427, 1103, 52, 12, 832, 1198, 284, 388, 827, 556, 194, 288, 218, 397, 84,
               1485, 95, 401, 739, 986, 994, 305, 668, 1324, 1437, 312, 993, 15, 822, 923, 707, 135, 42, 423, 37, 1183,
               1344, 997, 19, 699, 395, 119, 7, 168, 1711, 50, 151, 38, 20, 163, 686, 1364, 21, 24, 411, 32, 335, 188,
               55, 628, 274, 1766, 439, 180, 286, 1024, 87, 15, 1498, 290, 561, 971, 32, 294, 67, 113, 219, 42, 18, 715,
               3, 664, 242, 583, 221, 1045, 236, 74, 46, 1612, 639, 325, 164, 100, 69, 518, 38, 502, 26, 329, 112, 1174,
               127, 124, 90, 144, 527, 468, 152, 1098, 800, 125, 349, 191, 290, 191, 27, 651, 446, 267, 9, 1304, 269,
               586, 64, 983, 152, 236, 512, 8, 248, 177, 109, 311, 957, 47, 126, 69, 13, 709, 204, 381, 1151, 580, 340,
               994, 865, 258, 190, 9, 1149, 930, 1128, 321, 100, 471, 0, 507, 1308, 326, 585, 813, 1088, 76, 174, 333,
               387, 631, 186, 430, 988, 24, 820, 11, 45, 173, 167, 1494, 98, 1467, 456, 167, 21, 1363, 1173, 394, 318,
               1601, 1111, 1249, 757, 282, 672, 1227, 1214, 277, 336, 815, 136, 1192, 681, 689, 431, 130, 1488, 154,
               465, 14, 709, 339, 1123, 68, 151, 1280, 143, 1797, 23, 250, 1231, 1007, 302, 1103, 2, 585, 552, 1732,
               994, 225, 771, 1495, 82, 229, 700, 910, 15, 38, 159, 1122, 316, 1044, 711, 1436, 920, 1722, 523, 1398,
               188, 443, 1032, 93, 33, 397, 272, 187, 24, 489, 53, 79, 1277, 671, 1094, 68, 1705, 984, 1096, 512, 145,
               389, 167, 161, 1174, 94, 4, 534, 1295, 648, 75, 24, 366, 995, 175, 220, 714, 843, 412, 267, 634, 1209,
               66, 1094, 125, 822, 1114, 1513, 694, 1520, 30, 676, 817, 245, 26, 77, 1146, 552, 143, 165, 39, 343, 971,
               87, 0, 90, 1434, 588, 616, 99, 297, 1034, 114, 5, 702, 917, 582, 733, 31, 54, 820, 0, 212, 192, 282, 33,
               639, 1661, 460, 75, 680, 115, 178, 194, 271, 274, 582, 1008, 89, 139, 611, 707, 0, 376, 65, 9, 161, 135,
               40, 134, 566, 66, 601, 95, 817, 745, 202, 352, 447, 322, 842, 6, 1247, 175, 468, 330, 608, 368, 139, 21,
               29, 486, 121, 9, 1293, 298, 73, 328, 302, 145, 889, 1794, 677, 56, 952, 520, 80]

    krabben = sorted(krabben)
    mediaan = (krabben[499] + krabben[500]) / 2

    antwoord = 0
    for krab in range(len(krabben)):
        antwoord = antwoord + abs(mediaan - krabben[krab])


@get_runtime
def rolf_7b():
    krabben = [1101, 1, 29, 67, 1102, 0, 1, 65, 1008, 65, 35, 66, 1005, 66, 28, 1, 67, 65, 20, 4, 0, 1001, 65, 1, 65,
               1106, 0, 8, 99, 35, 67, 101, 99, 105, 32, 110, 39, 101, 115, 116, 32, 112, 97, 115, 32, 117, 110, 101,
               32, 105, 110, 116, 99, 111, 100, 101, 32, 112, 114, 111, 103, 114, 97, 109, 10, 478, 1187, 253, 1892,
               900, 155, 20, 787, 17, 248, 1397, 407, 167, 686, 638, 1020, 960, 124, 840, 220, 1824, 700, 373, 4, 551,
               229, 294, 567, 254, 350, 1144, 679, 124, 361, 145, 483, 335, 202, 1334, 367, 60, 870, 11, 557, 482, 645,
               672, 1296, 1538, 427, 78, 542, 1135, 13, 65, 0, 140, 705, 13, 642, 187, 1085, 36, 1118, 349, 601, 382,
               584, 941, 26, 949, 200, 763, 198, 430, 204, 1352, 1135, 210, 342, 11, 1089, 830, 1523, 9, 523, 167, 762,
               254, 805, 8, 132, 29, 102, 1299, 936, 756, 59, 134, 183, 235, 316, 139, 48, 182, 44, 88, 213, 113, 93,
               169, 565, 601, 1899, 1191, 189, 796, 770, 32, 1183, 365, 374, 867, 918, 1084, 86, 75, 20, 47, 99, 1140,
               2, 99, 1024, 366, 455, 752, 556, 1220, 66, 326, 450, 213, 1, 342, 756, 49, 675, 160, 280, 68, 221, 193,
               379, 88, 179, 94, 16, 109, 570, 1145, 1207, 824, 355, 1389, 1601, 168, 86, 236, 923, 120, 759, 14, 478,
               460, 84, 167, 1723, 1005, 269, 6, 171, 861, 311, 832, 952, 701, 3, 1598, 1466, 96, 780, 57, 161, 631,
               572, 276, 105, 594, 276, 17, 405, 688, 1444, 173, 23, 199, 177, 689, 19, 565, 472, 151, 986, 76, 379,
               1430, 212, 928, 106, 25, 143, 84, 833, 942, 860, 1555, 271, 239, 720, 596, 1209, 235, 535, 361, 1794, 79,
               283, 275, 17, 342, 1687, 1434, 173, 967, 740, 217, 1370, 18, 1579, 1259, 546, 94, 623, 475, 834, 1000,
               456, 101, 520, 120, 1023, 360, 167, 213, 617, 42, 1149, 629, 760, 17, 33, 27, 1347, 414, 646, 1116, 1340,
               134, 259, 143, 407, 249, 328, 968, 677, 241, 438, 98, 313, 27, 791, 1, 634, 3, 918, 1482, 213, 123, 444,
               45, 24, 26, 26, 1203, 64, 67, 1562, 1, 4, 298, 12, 384, 32, 443, 37, 268, 674, 356, 202, 286, 694, 272,
               163, 950, 1022, 54, 59, 21, 73, 519, 462, 106, 76, 1112, 10, 72, 388, 194, 6, 120, 9, 645, 209, 1121, 75,
               599, 362, 661, 439, 69, 62, 339, 390, 23, 1247, 365, 1266, 4, 246, 511, 47, 467, 134, 276, 497, 130, 458,
               427, 669, 1191, 701, 917, 168, 1191, 294, 641, 236, 801, 375, 106, 872, 800, 87, 356, 583, 1096, 253,
               459, 951, 1331, 719, 66, 1091, 525, 15, 370, 290, 141, 1201, 30, 43, 37, 76, 1131, 616, 297, 172, 402,
               1016, 654, 301, 63, 872, 303, 69, 1195, 502, 351, 52, 1659, 86, 104, 294, 807, 166, 120, 190, 333, 60,
               283, 819, 198, 184, 144, 278, 343, 1395, 496, 103, 705, 485, 172, 642, 225, 181, 583, 188, 38, 436, 801,
               91, 5, 634, 180, 28, 20, 146, 488, 676, 121, 420, 965, 220, 1564, 1011, 241, 423, 3, 1631, 709, 106, 725,
               164, 1032, 65, 205, 503, 188, 397, 1072, 49, 121, 761, 721, 249, 418, 87, 126, 258, 712, 500, 435, 157,
               127, 681, 108, 270, 647, 504, 505, 83, 407, 212, 165, 1177, 160, 715, 1292, 491, 195, 141, 25, 829, 1316,
               242, 754, 364, 1707, 33, 594, 434, 488, 368, 298, 183, 1156, 29, 1674, 537, 378, 8, 9, 860, 240, 571,
               749, 471, 331, 501, 156, 62, 427, 1103, 52, 12, 832, 1198, 284, 388, 827, 556, 194, 288, 218, 397, 84,
               1485, 95, 401, 739, 986, 994, 305, 668, 1324, 1437, 312, 993, 15, 822, 923, 707, 135, 42, 423, 37, 1183,
               1344, 997, 19, 699, 395, 119, 7, 168, 1711, 50, 151, 38, 20, 163, 686, 1364, 21, 24, 411, 32, 335, 188,
               55, 628, 274, 1766, 439, 180, 286, 1024, 87, 15, 1498, 290, 561, 971, 32, 294, 67, 113, 219, 42, 18, 715,
               3, 664, 242, 583, 221, 1045, 236, 74, 46, 1612, 639, 325, 164, 100, 69, 518, 38, 502, 26, 329, 112, 1174,
               127, 124, 90, 144, 527, 468, 152, 1098, 800, 125, 349, 191, 290, 191, 27, 651, 446, 267, 9, 1304, 269,
               586, 64, 983, 152, 236, 512, 8, 248, 177, 109, 311, 957, 47, 126, 69, 13, 709, 204, 381, 1151, 580, 340,
               994, 865, 258, 190, 9, 1149, 930, 1128, 321, 100, 471, 0, 507, 1308, 326, 585, 813, 1088, 76, 174, 333,
               387, 631, 186, 430, 988, 24, 820, 11, 45, 173, 167, 1494, 98, 1467, 456, 167, 21, 1363, 1173, 394, 318,
               1601, 1111, 1249, 757, 282, 672, 1227, 1214, 277, 336, 815, 136, 1192, 681, 689, 431, 130, 1488, 154,
               465, 14, 709, 339, 1123, 68, 151, 1280, 143, 1797, 23, 250, 1231, 1007, 302, 1103, 2, 585, 552, 1732,
               994, 225, 771, 1495, 82, 229, 700, 910, 15, 38, 159, 1122, 316, 1044, 711, 1436, 920, 1722, 523, 1398,
               188, 443, 1032, 93, 33, 397, 272, 187, 24, 489, 53, 79, 1277, 671, 1094, 68, 1705, 984, 1096, 512, 145,
               389, 167, 161, 1174, 94, 4, 534, 1295, 648, 75, 24, 366, 995, 175, 220, 714, 843, 412, 267, 634, 1209,
               66, 1094, 125, 822, 1114, 1513, 694, 1520, 30, 676, 817, 245, 26, 77, 1146, 552, 143, 165, 39, 343, 971,
               87, 0, 90, 1434, 588, 616, 99, 297, 1034, 114, 5, 702, 917, 582, 733, 31, 54, 820, 0, 212, 192, 282, 33,
               639, 1661, 460, 75, 680, 115, 178, 194, 271, 274, 582, 1008, 89, 139, 611, 707, 0, 376, 65, 9, 161, 135,
               40, 134, 566, 66, 601, 95, 817, 745, 202, 352, 447, 322, 842, 6, 1247, 175, 468, 330, 608, 368, 139, 21,
               29, 486, 121, 9, 1293, 298, 73, 328, 302, 145, 889, 1794, 677, 56, 952, 520, 80]

    for doel in range(100):
        antwoord = 0
        for krab in range(len(krabben)):
            benzine = 0
            afstand = abs(doel + 400 - krabben[krab])
            for x in range(afstand):
                benzine = benzine + x + 1
            antwoord = antwoord + benzine


@get_runtime
def rolf_8():
    # bestand lezen en in stukjes hakken:
    bestand = open('input/day_8.txt', 'r')
    alles = bestand.readlines()
    input = []
    for x in range(len(alles)):
        alles[x] = alles[x].replace('\n', '')
    for x in range(len(alles)):
        alles[x] = alles[x].split(' | ')
    for x in range(len(alles)):
        alles[x][0] = alles[x][0].split(' ')
    for x in range(len(alles)):
        alles[x][1] = alles[x][1].split(' ')

    # antwoord op vraag A berekenen:
    legalelengtes = [2, 3, 4, 7]
    antwoord = 0
    for x in range(len(alles)):
        for y in range(4):
            for z in range(4):
                if len(alles[x][1][y]) == legalelengtes[z]:
                    antwoord = antwoord + 1
    # print(antwoord)

    # letters sorteren:
    for x in range(len(alles)):
        for y in range(2):
            for z in range(len(alles[x][y])):
                alles[x][y][z] = ''.join(sorted(alles[x][y][z]))

    # de decode code aanmaken:
    decode = []
    for x in range(len(alles)):
        decode.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # de 1,4,7,8 er in:
    for x in range(len(alles)):
        for y in range(10):
            if len(alles[x][0][y]) == 2:
                decode[x][1] = alles[x][0][y]
            elif len(alles[x][0][y]) == 4:
                decode[x][4] = alles[x][0][y]
            elif len(alles[x][0][y]) == 3:
                decode[x][7] = alles[x][0][y]
            elif len(alles[x][0][y]) == 7:
                decode[x][8] = alles[x][0][y]

    # de 069 er in:
    for x in range(len(alles)):
        nulzesnegen = []
        for y in range(10):
            if len(alles[x][0][y]) == 6:
                nulzesnegen.append(alles[x][0][y])
            if len(alles[x][0][y]) == 2:
                deeen = list(alles[x][0][y])
        for y in range(3):
            isditeenzes = False
            isditeennegen = False
            isditeennul = False
            for z in range(2):
                if deeen[z] not in nulzesnegen[y]:
                    isditeenzes = True
            for z in range(4):
                if decode[x][4][z] not in list(nulzesnegen[y]) and isditeenzes == False:
                    isditeennul = True
            if isditeennul == False and isditeenzes == False:
                isditeennegen = True
            if isditeenzes:
                decode[x][6] = nulzesnegen[y]
            if isditeennul:
                decode[x][0] = nulzesnegen[y]
            if isditeennegen:
                decode[x][9] = nulzesnegen[y]

    # de 235 er in:
    for x in range(len(alles)):
        tweedrievijf = []
        for y in range(10):
            if len(alles[x][0][y]) == 5:
                tweedrievijf.append(alles[x][0][y])
        for y in range(3):
            isditeentwee = False
            isditeendrie = False
            isditeenvijf = True
            for z in range(5):
                if tweedrievijf[y][z] not in list(decode[x][6]):
                    isditeenvijf = False
            for z in range(2):
                if decode[x][1][z] not in list(tweedrievijf[y]) and isditeenvijf == False:
                    isditeentwee = True
            if isditeentwee == False and isditeenvijf == False:
                isditeendrie = True
            if isditeentwee:
                decode[x][2] = tweedrievijf[y]
            if isditeendrie:
                decode[x][3] = tweedrievijf[y]
            if isditeenvijf:
                decode[x][5] = tweedrievijf[y]

    # oplossing uitrekenen:
    antwoord = 0

    for x in range(len(alles)):
        deze = ''
        for y in range(4):
            for z in range(10):
                if alles[x][1][y] == decode[x][z]:
                    deze = deze + str(z)
        antwoord = antwoord + int(deze)

    # print(antwoord)


if __name__ == '__main__':
    # rolf_dag_4a()
    # rolf_dag_4b()
    # rolf_5()
    # rolf_6a()
    # rolf_6b()
    # rolf_7a()
    # rolf_7b()
    rolf_8()
