from pdiFun import *
import os


def recorte(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convertir al espacio HSV
    h, s, v = cv2.split(hsv)  # Dividir las capas
    ss = s.copy()  # Copia de la capa de saturación
    #cv2.imshow('capa', ss)
    kernel = np.ones((6, 6), np.uint8)  # Kernel


    img_med_f = cv2.medianBlur(ss, 1)  # Filtrado medio

    img_bin2 = binFun(img_med_f)  # Binarizado

    mask2 = bwareaopen(img_bin2, 3500)  # Aplicar mascara
    mask_t = erodeFun(kernel, mask2, 2)  # Suaviza el contorno

    img[mask_t == 0] = 0  # Eliminar fondo de la imagen
    #cv2.imshow('recorte', img)
    return img  # retorna la imagen sin fondo y suavizada

def save_photos(lista, input_images_path, folder_path, folder_path_write, files_names):
    if len(lista) != 0:
        for i in lista:
            img = cv2.imread(input_images_path + folder_path + "foto" + str(i) + ".jpg")
            img = recorte(img)
            cv2.imwrite(input_images_path + folder_path_write + 'foto'
                        + str(i) + '.JPG', img)
    else:
        for file_name in files_names:
            image_path = input_images_path + folder_path + file_name
            index = int(image_path[len(input_images_path) + len(folder_path) + len("foto"):-4])
            img = cv2.imread(image_path)
            img = recorte(img)
            cv2.imwrite(input_images_path + folder_path_write + 'foto' + str(
                index) + '.JPG', img)


#input_images_path = "/home/sistemic/Documents/12vo_Semestre/FundamentosIC/Avance2/frutas/"
input_images_path = "/home/sistemic/Documents/12vo_Semestre/FundamentosIC/Avance2/frutas_valid/"
#folder_path_list = ["Aguacate/","Banano/","Fresa/","Limon/","Mango/","Manzana/","Pera/","Tomate/","Uchuva/","Uva/"]
#folder_path_write_list = ["AguacateRecorte/","BananoRecorte/","FresaRecorte/","LimonRecorte/","MangoRecorte/","ManzanaRecorte/","PeraRecorte/","TomateRecorte/",
#                          "UchuvaRecorte/","UvaRecorte/"]

folder_path_list = ["Uva/"]
folder_path_write_list = ["UvaRecorte/"]


lista = []
if len(lista) == 0:
    for folder_path in folder_path_list:
        folder_path_write = folder_path_write_list[folder_path_list.index(folder_path)]
        files_names = os.listdir(input_images_path + folder_path)
        save_photos(lista, input_images_path, folder_path, folder_path_write, files_names)
        
else:
    folder_path = folder_path_list[2]
    folder_path_write = folder_path_write_list[2]
    files_names = os.listdir(input_images_path + folder_path)
    save_photos(lista, input_images_path, folder_path, folder_path_write, files_names)


print("fin")   