## Importar librerias
import math
import pandas as pd
from pdiFun import *
from skimage import filters, measure
import matplotlib.pyplot as plt
import os

def extraer_caracteristicas(img):
    img_med_f = cv2.medianBlur(img, 51)  # Filtrado medio
    gris = grayFun(img_med_f)  # Escala de grises
    img_bin = binFun(gris)  # binarizada 0 - 255
    b, g, r = cv2.split(img)  # Separar
    bb = b.copy()
    bb[img_bin == 0] = 0
    edges = cv2.Canny(image=r, threshold1=20, threshold2=10)  # Canny Edge Detection
    # Canny Edge Detection para el perimetro
    borde = cv2.Canny(image=b, threshold1=100, threshold2=200)  # Canny Edge Detection
    rgbs = np.concatenate((b,g,r), axis=1) #Visualizar capas
    """Redimensionar para visualización"""
    scale_percent = 50 # percent of original size
    width  = int(rgbs.shape[1] * scale_percent / 100)
    height = int(rgbs.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    rgbs = cv2.resize(rgbs, dim, interpolation = cv2.INTER_AREA)
    w = b.shape[1]
    h = b.shape[0]
    area_foto = w * h
    area = (np.sum(img_bin))  # Area de fruta en sumas de 255 por pixel
    area_pixel = area / 255  # Area de fruta en sumas de 1 por pixel
    p_area = area_pixel / area_foto  # Area de la fruta respecto al tamaño de la foto
    azul = np.sum(b)
    verde = np.sum(g)
    rojo = np.sum(r)
    p_azul = azul / area
    p_verde = verde / area
    p_rojo = rojo / area

    borde = bwareaopen(borde, p_area * 5000)

    perimetro = (borde.sum()) / 1000

    label_img = measure.label(img_bin)
    regions = measure.regionprops(label_img)
    props = measure.regionprops_table(label_img, properties=('centroid',
                                                             'orientation',
                                                             'major_axis_length',
                                                             'minor_axis_length'))
    props1 = props.copy()
    for props in regions:
        y0, x0 = props.centroid
        orientation = props.orientation
        x1 = x0 + math.cos(orientation) * 0.5 * props.minor_axis_length
        y1 = y0 - math.sin(orientation) * 0.5 * props.minor_axis_length
        x2 = x0 - math.sin(orientation) * 0.5 * props.major_axis_length
        y2 = y0 - math.cos(orientation) * 0.5 * props.major_axis_length

        minr, minc, maxr, maxc = props.bbox
        bx = (minc, maxc, maxc, minc, minc)
        by = (minr, minr, maxr, maxr, minr)


    dt = pd.DataFrame(props1).head()
    major_axis = dt.iloc[0, 3]
    minor_axis = dt.iloc[0, 4]
    textura = edges.sum() / area  # Pondera el total de texturas en el area de la fruta

    # Relacion de ejes
    axis_ratio = minor_axis / major_axis

    return p_azul,p_verde,p_rojo,p_area,axis_ratio,textura,perimetro   # retorna dataset con las caracteristicas extraidas

frutas = ['Aguacate','Banano','Fresa','Limon','Mango','Manzana','Pera','Tomate','Uchuva','Uva']
for fruta in frutas:
    input_images_path = "/home/sistemic/Documents/12vo_Semestre/FundamentosIC/Avance2/frutas/"+fruta+"Recorte"
    #input_images_path = "/home/sistemic/Documents/12vo_Semestre/FundamentosIC/Avance2/frutas_valid/"+fruta+"Recorte"
    dataf = pd.DataFrame(columns=['index', 'clase', 'azul', 'verde', 'rojo', 'area', 'ratio', 'textura','perimetro'])
    files_names = os.listdir(input_images_path)
    log = False
    cont = 0
    for file_name in files_names:
        image_path = input_images_path + "/" + file_name
        # print(image_path)
        # image_path = image_path_test
        index = int(image_path[len(input_images_path) + 1 + len("imagen"):-4])
        print(f'index: {index}')
        clase = class_fruit(index)
        img = cv2.imread(image_path)

        azul, verde, rojo, p_area, ratio, textura, perimetro = extraer_caracteristicas(img)

        """Guardar Caracteristicas"""
        '''if cont != 0:
            #print(f'datos{dataf.loc[cont-1].area}')
            azul = (azul+dataf.loc[cont-1].azul)/2
            verde = (verde+dataf.loc[cont-1].verde)/2
            rojo = (rojo+dataf.loc[cont-1].rojo)/2
            p_area = (p_area+dataf.loc[cont-1].area)/2
            ratio = (ratio+dataf.loc[cont-1].ratio)/2
            textura = (textura+dataf.loc[cont-1].textura)/2
            perimetro = (perimetro+dataf.loc[cont-1].perimetro)/2'''
        dataf.loc[cont] = [index, clase, azul, verde, rojo, p_area, ratio, textura, perimetro]
        cont += 1
        print(cont)

    dataf[['index']] = dataf[['index']].astype('int')
    dataf[['clase']] = dataf[['clase']].astype('int')
    dataf.set_index('index', inplace=True)
    dataf.reset_index(drop=True, inplace=True)
    dataf.to_excel('/home/sistemic/Documents/12vo_Semestre/FundamentosIC/Avance2/frutas_valid/'+fruta+'.xlsx') # Save DataFrame in xlsx
    print(dataf)