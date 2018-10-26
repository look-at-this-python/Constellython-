from PIL import Image
import datetime

rgbEstrella = 150
picture_stars = "Estrellas1.jpg"
picture_constellation="ARAGON.png"
img_stars = Image.open(picture_stars)
img_stars.show()


def load_stars():
    global img_stars

    # Obtener matriz de blancos
    pix = img_stars.load()
    matrix_return = []
    for i in range(0, img_stars.width):
        for j in range(0, img_stars.height):
            if (pix[i, j][0] + pix[i, j][1] + pix[i, j][2])/3 > rgbEstrella:
                matrix_return = matrix_return + [[i, j]]

    #print(matrix_return)

    #img2 = Image.new(img.mode, img.size)
    #for j in range(0, len(matriz_estrella) - 1):
    #    img2.putpixel((matriz_estrella[j][0], matriz_estrella[j][1]), (255, 255, 255))
    #img2.show()

    return matrix_return


def filtrar_estrellas(matriz_estrella):
    global matriz_descartes
    global matriz_definitiva

    for j in range(0, len(matriz_estrella)-1):
        if(j%100 == 0):
            print("Filtrando estrellas: ", j/(len(matriz_estrella)-1) * 100, "%")
        if(not existe(matriz_descartes, [matriz_estrella[j][0], matriz_estrella[j][1]])):
            matriz_definitiva = matriz_definitiva + [[matriz_estrella[j][0], matriz_estrella[j][1]]]

        existe_recursivo(matriz_estrella, matriz_estrella[j][0], matriz_estrella[j][1])

    return matriz_definitiva


def existe_recursivo(matriz_estrella, i, j):
    global matriz_descartes
    global matriz_definitiva


    if (not existe(matriz_definitiva, [i+1, j]) and  existe(matriz_estrella, [(i + 1), j])):
        matriz_descartes = matriz_descartes + [[i + 1, j]]
    if (not existe(matriz_definitiva, [i, j+1]) and existe(matriz_estrella, [i, (j+1)])):
        matriz_descartes = matriz_descartes + [[i , j+1]]
    if (not existe(matriz_definitiva, [i+1, j+1]) and existe(matriz_estrella, [(i + 1), (j+1)])):
        matriz_descartes = matriz_descartes + [[i + 1, j+1]]
    if (not existe(matriz_definitiva, [i-1, j-1]) and existe(matriz_estrella, [(i + 1), (j-1)])):
        matriz_descartes = matriz_descartes + [[i - 1, j-1]]

    if (not existe(matriz_definitiva, [i - 1, j]) and existe(matriz_estrella, [(i - 1), j])):
        matriz_descartes = matriz_descartes + [[i - 1, j]]
    if (not existe(matriz_definitiva, [i, j - 1]) and existe(matriz_estrella, [i, (j - 1)])):
        matriz_descartes = matriz_descartes + [[i, j - 1]]
    if (not existe(matriz_definitiva, [i + 1, j - 1]) and existe(matriz_estrella, [(i + 1), (j - 1)])):
        matriz_descartes = matriz_descartes + [[i + 1, j - 1]]
    if (not existe(matriz_definitiva, [i + 1, j - 1]) and existe(matriz_estrella, [(i + 1), (j - 1)])):
        matriz_descartes = matriz_descartes + [[i + 1, j - 1]]

def bordes(foto):
    img = Image.open(foto)
    pix = img.load()
    #putpixel
    borde=[]
    dentro=0
    for j in range(0, img.height):
        for i in range(0, img.width):
            if(dentro==0):
                if(pix[i,j][3]>=255):
                    borde=borde+[[i,j]]
                    dentro=1
            if(dentro==1):
                if(pix[i,j][3]!=255):
                    dentro=0
                    borde = borde + [[i, j]]
    return borde

def puntear(borde):
    factor_compresion=60
    puntos = []
    for i in range(0, int((len(borde) - 1) / factor_compresion)):
        puntos = puntos + [[borde[i * factor_compresion][0], borde[i * factor_compresion][1]]]
        puntos = puntos + [[borde[i * factor_compresion + 1][0], borde[i * factor_compresion + 1][1]]]
    return puntos


def find_constellation(contp, tamano):
    factor_compresion=20
    max=0
    #memoria=[]
    xy=[]
    print("total i:",int((tamano[0] - 1) / factor_compresion))
    print("total j:", int((tamano[1] - 1) / factor_compresion))
    for i in range(0,int((tamano[0] - 1) / factor_compresion)):
        print("Buscando constelaciones: ", i*100/int((tamano[0] - 1) / factor_compresion), "% - ",  datetime.datetime.now())
        for j in range(0,int((tamano[1] - 1) / factor_compresion)):
            volatil=[]
            for h in range(0,len(contp)-1):
                volatil=volatil + [[ contp[h][0]+i*factor_compresion, contp[h][1]+j*factor_compresion ]]
            coinc=0
            for k in range(0,len(volatil)-1):
                if(vecinos(volatil[k][0] , volatil[k][1] )):
                    coinc +=1
#            print(coinc, " - i:", i, ", j:", j, " - ",  datetime.datetime.now())
            if (coinc > max):
                max=coinc
                #memoria=volatil
                xy=[i*factor_compresion,j*factor_compresion]
                print("Coincidencias: ", coinc, ", i:", i, ", j:", j)
    #return memoria
    return xy

def vecinos(x,y):
    global matriz_definitiva
    for i in range(-5,5):
        for j in range(-5,5):
            if(existe(matriz_definitiva, [x+i,y+j])):
                return True
    return False

def existe(matrix, valor):
    try:
        matrix.index(valor)
        return True
    except:
        return False

# Enable search point of stars

matriz_descartes = []
matriz_definitiva = []

print("Paso 0 - " , datetime.datetime.now())
matrix_stars = load_stars()
matriz_definitiva = filtrar_estrellas(matrix_stars)
'''
# Matriz cargada manual para ahorrar el tiempo de filtrado
matriz_definitiva = [[2, 1146], [8, 1151], [10, 1537], [30, 1572], [33, 1583], [47, 1314], [50, 1574], [65, 1609],
                     [66, 520], [67, 517], [67, 527], [67, 818], [68, 507], [69, 815], [80, 1616], [83, 2188],
                     [86, 498], [92, 2190], [92, 2204], [93, 2188], [109, 2196], [123, 1836], [124, 1839], [132, 1843],
                     [135, 277], [137, 275], [138, 2112], [160, 1080], [175, 339], [178, 1394], [179, 1392], [182, 420],
                     [185, 418], [186, 414], [216, 2581], [274, 477], [275, 474], [296, 1410], [298, 1405], [300, 1402],
                     [344, 41], [346, 339], [383, 2632], [426, 868], [434, 2212], [447, 858], [448, 856], [541, 1094],
                     [542, 1092], [557, 1455], [558, 1440], [558, 1446], [558, 1450], [571, 3083], [605, 1199],
                     [637, 1751], [664, 2901], [665, 2898], [681, 2098], [692, 751], [692, 2642], [714, 386],
                     [719, 384], [743, 2239], [745, 2237], [749, 2235], [768, 2576], [769, 2574], [778, 1627],
                     [805, 195], [829, 1752], [845, 56], [846, 48], [846, 947], [864, 1295], [881, 1770], [895, 2746],
                     [897, 2743], [898, 2928], [899, 381], [900, 379], [936, 1305], [954, 2834], [963, 297], [998, 787],
                     [1001, 255], [1034, 893], [1077, 1401], [1082, 127], [1100, 2592], [1107, 1289], [1125, 673],
                     [1126, 670], [1127, 650], [1135, 1486], [1137, 1477], [1139, 2934], [1140, 2932], [1144, 763],
                     [1151, 1488], [1160, 934], [1216, 2174], [1219, 866], [1220, 864], [1239, 853], [1247, 434],
                     [1249, 431], [1255, 851], [1258, 1839], [1268, 473], [1275, 850], [1276, 848], [1295, 336],
                     [1336, 1586], [1336, 1592], [1337, 1584], [1343, 2441], [1344, 2439], [1352, 1006], [1352, 2290],
                     [1353, 2288], [1354, 2974], [1355, 1750], [1355, 2972], [1359, 1754], [1368, 1648], [1372, 1143],
                     [1373, 1140], [1373, 2268], [1387, 292], [1397, 280], [1399, 280], [1401, 2439], [1417, 1499],
                     [1426, 404], [1427, 399], [1427, 416], [1443, 1922], [1448, 1918], [1457, 932], [1458, 1101],
                     [1460, 541], [1465, 965], [1466, 963], [1470, 2183], [1479, 785], [1480, 783], [1481, 781],
                     [1495, 1823], [1496, 882], [1507, 272], [1513, 452], [1529, 423], [1534, 240], [1535, 237],
                     [1535, 284], [1540, 415], [1542, 422], [1551, 708], [1577, 2345], [1578, 408], [1585, 406],
                     [1591, 2389], [1594, 1728], [1595, 1726], [1595, 2396], [1596, 2380], [1596, 2382], [1596, 2390],
                     [1598, 2377], [1603, 2374], [1609, 2567], [1612, 408], [1613, 1998], [1613, 2377], [1613, 2400],
                     [1615, 1995], [1615, 2374], [1616, 407], [1616, 1993], [1617, 404], [1618, 402], [1619, 2377],
                     [1625, 2374], [1626, 1323], [1630, 404], [1640, 403], [1663, 402], [1665, 1126], [1666, 1124],
                     [1668, 905], [1675, 971], [1684, 1139], [1693, 2879], [1695, 1009], [1696, 983], [1696, 986],
                     [1698, 979], [1701, 975], [1701, 1594], [1701, 2874], [1702, 2872], [1703, 971], [1703, 1589],
                     [1703, 2869], [1704, 973], [1704, 2867], [1706, 971], [1710, 1795], [1719, 2862], [1722, 1019],
                     [1723, 1017], [1760, 90], [1761, 88], [1766, 403], [1771, 19], [1771, 2612], [1772, 2610],
                     [1778, 71], [1780, 69], [1782, 926], [1783, 924], [1784, 922], [1787, 1976], [1788, 1974],
                     [1790, 2742], [1823, 817], [1844, 1389], [1845, 1387], [1856, 36], [1863, 1574], [1886, 1243],
                     [1921, 346], [1922, 344], [1941, 2165], [1942, 2872], [1973, 500], [1973, 2909], [1974, 1518],
                     [1976, 645], [1977, 235], [1979, 2910], [2035, 197], [2036, 195], [2086, 128], [2086, 2466],
                     [2087, 2463], [2093, 2830], [2094, 1381], [2095, 875], [2095, 1379], [2110, 1212], [2115, 593],
                     [2140, 687], [2141, 641], [2141, 685], [2153, 811], [2159, 2325], [2178, 2256], [2184, 631],
                     [2231, 270], [2232, 1341], [2232, 2981], [2240, 1361], [2243, 400], [2257, 1380], [2274, 84],
                     [2275, 82], [2281, 739], [2308, 379], [2331, 87], [2334, 2383], [2339, 87], [2343, 250],
                     [2345, 2353], [2346, 85], [2369, 17], [2370, 81], [2387, 84], [2391, 85], [2408, 486], [2409, 484],
                     [2413, 3094], [2431, 1115], [2447, 219], [2462, 2168], [2490, 2918], [2491, 2916], [2498, 1563],
                     [2513, 989], [2531, 1138], [2532, 1136], [2533, 2277], [2534, 2273], [2535, 2265], [2535, 3077],
                     [2536, 2259], [2537, 2257], [2538, 2253], [2542, 2249], [2545, 2243], [2547, 2240], [2548, 2234],
                     [2548, 2238], [2550, 2229], [2551, 2303], [2552, 2247], [2561, 2278], [2562, 1631], [2562, 1740],
                     [2571, 449], [2572, 447], [2572, 2270], [2586, 687], [2603, 2259], [2604, 2257], [2605, 2254],
                     [2639, 949], [2660, 108], [2661, 547], [2662, 1927], [2678, 1405], [2708, 1291], [2712, 3017],
                     [2716, 2508], [2730, 237], [2732, 234], [2732, 1117], [2759, 675], [2772, 950], [2773, 946],
                     [2773, 1675], [2774, 1673], [2815, 889], [2816, 887], [2818, 884], [2820, 878], [2821, 873],
                     [2822, 870], [2827, 1607], [2848, 196], [2850, 199], [2855, 194], [2855, 1055], [2856, 1053],
                     [2864, 1052], [2865, 1049], [2883, 995], [2905, 2376], [2914, 701], [2918, 2211], [2922, 1952],
                     [2923, 1949], [2923, 2213], [2938, 1847], [2956, 1808], [2975, 183], [2989, 1354], [2990, 1362],
                     [2991, 1360], [3000, 1349], [3006, 3035], [3013, 3034], [3022, 1309], [3023, 1306], [3026, 1301],
                     [3027, 1299], [3028, 1295], [3029, 1292], [3033, 2554], [3035, 2747], [3043, 1341], [3044, 1550],
                     [3082, 2754], [3087, 2750], [3100, 1177], [3101, 1174], [3102, 1162], [3102, 1165], [3118, 1173],
                     [3121, 627], [3129, 635], [3139, 2638], [3140, 1526], [3141, 1524], [3142, 548], [3142, 1522],
                     [3160, 3001], [3161, 2755], [3162, 2753], [3164, 1217], [3171, 1213], [3190, 1208], [3195, 1203],
                     [3198, 387], [3207, 370], [3225, 428], [3254, 2161], [3259, 2167], [3260, 2165], [3261, 978],
                     [3265, 2150], [3268, 2146], [3272, 1236], [3273, 2150], [3275, 2144], [3284, 2171], [3300, 2150],
                     [3309, 548], [3317, 2055], [3337, 1894], [3340, 643], [3342, 2507], [3365, 529], [3368, 1842],
                     [3413, 371], [3414, 369], [3414, 3098]]
                     '''
print("Paso 1 - " , datetime.datetime.now())

border_constellation = bordes(picture_constellation)
print("Paso 2 - " , datetime.datetime.now())
points_constellation = puntear(border_constellation)
print("Paso 3 - " , datetime.datetime.now())

xy = find_constellation(points_constellation,[img_stars.height,img_stars.height])
print("Paso 4 - " , datetime.datetime.now())

for i in range(0, len(border_constellation)-1):
    img_stars.putpixel((border_constellation[i][0] + xy[0], border_constellation[i][1] + xy[1] ),(255,255,255))
for i in range(0, len(matriz_definitiva)-1):
    img_stars.putpixel((matriz_definitiva[i][0], matriz_definitiva[i][1] ),(255,0,0))

img_stars.show()