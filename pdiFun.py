import numpy as np
import cv2
import copy
from scipy import ndimage as ndi
from skimage.feature import match_template

""" 
*******************************************************************************
--------- 1.Funciones ---------------------------------------------------------
*******************************************************************************
"""

"""Fun algoritmo bwareaopen tomado de 
#       https://stackoverflow.com/questions/2348365/matlab-bwareaopen-equivalent-function-in-opencv
"""


def bwareaopen(img, min_size, connectivity=8):
    """Remove small objects from binary image (approximation of 
    bwareaopen in Matlab for 2D images).
    
    Args:
        img: a binary image (dtype=uint8) to remove small objects from
        min_size: minimum size (in pixels) for an object to remain in the image
        connectivity: Pixel connectivity; either 4 (connected via edges) or 8 (connected via edges and corners).
    
    Returns:
        the binary image with small objects removed
    """

    # Find all connected components (called here "labels")
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        img, connectivity=connectivity)

    # check size of all connected components (area in pixels)
    for i in range(num_labels):
        label_size = stats[i, cv2.CC_STAT_AREA]

        # remove connected components smaller than min_size
        if label_size < min_size:
            img[labels == i] = 0

    return img


"""Función para pasar a escala de Grises"""


def grayFun(a):
    b = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    return b


"""Función para Binarizar con Othsu"""


def binFun(a):
    ret, binary = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


"""Funcion para Aplicar Erosion"""


def erodeFun(kernel, img, i):
    erode = cv2.erode(img, kernel, iterations=i)
    return erode


"Funcion clase en dataframe para frutas"


def clase_fruta(index):
    if (index >= 0 and index <= 15):
        clase = 'Banano'
    elif (index > 15 and index <= 26):
        clase = 'Tomate'
    elif (index > 26 and index <= 37):
        clase = 'Manzana'
    elif (index > 37 and index <= 48):
        clase = 'Pera'
    elif (index > 48 and index <= 68):
        clase = 'Limon'
    elif (index > 68 and index <= 89):
        clase = 'Uchuva'
    elif (index > 89 and index <= 109):
        clase = 'Uva'
    elif (index > 109):
        clase = 'Fresa'
    return clase


def translate(lista):
    fruta = ''
    for i in lista:
        if i == 0:
            fruta = 'aguacate'
        if i == 1:
            fruta = 'banano'
        if i == 2:
            fruta = 'fresa'
        if i == 3:
            fruta = 'limon'
        if i == 4:
            fruta = 'mango'
        if i == 5:
            fruta = 'manzana'
        if i == 6:
            fruta = 'pera'
        if i == 7:
            fruta = 'tomate'
        if i == 8:
            fruta = 'uchuva'
        if i == 9:
            fruta = 'uva'
    return fruta


def class_fruit(index):
    if 0 <= index < 250:
        class_df = 0 #Aguacate
        print("Aguacate")
    elif 250 <= index < 500:
        class_df = 1 #Banano
        print("Banano")
    elif 500 <= index < 750:
        class_df = 2 # Fresa
        print("Fresa")
    elif 750 <= index < 1000:
        class_df = 3 # Limon
        print("Limon")
    elif 1000 <= index < 1250:
        class_df = 4 # Mango
        print("Mango")
    elif 1250 <= index < 1500:
        class_df = 5 # Manzana
        print("Manzana")
    elif 1500 <= index < 1750:
        class_df = 6 # Pera
        print("Pera")
    elif 1750 <= index < 2000:
        class_df = 7  # Tomate
        print("Tomate")
    elif 2000 <= index < 2250:
        class_df = 8  # Uchuva
        print("Uchuva")
    elif 2250 <= index < 2500:
        class_df = 9  # Uva
        print("Uva")
    return class_df

def class_fruit_valid(index):
    if 0 <= index < 30:
        class_df = 0 #Aguacate
        print("Aguacate")
    elif 30 <= index < 60:
        class_df = 1 #Banano
        print("Banano")
    elif 60 <= index < 90:
        class_df = 2 # Fresa
        print("Fresa")
    elif 90 <= index < 120:
        class_df = 3 # Limon
        print("Limon")
    elif 120 <= index < 149:
        class_df = 4 # Mango
        print("Mango")
    elif 149 <= index < 178:
        class_df = 5 # Manzana
        print("Manzana")
    elif 178 <= index < 208:
        class_df = 6 # Pera
        print("Pera")
    elif 208 <= index < 240:
        class_df = 7  # Tomate
        print("Tomate")
    elif 240 <= index < 275:
        class_df = 8  # Uchuva
        print("Uchuva")
    elif 275 <= index < 305:
        class_df = 9  # Uva
        print("Uva")
    return class_df