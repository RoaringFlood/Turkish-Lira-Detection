from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import os
import shutil


model = load_model('../paratanima/para_tanima_model.h5')
size = (224, 224)

path = 'deneme_set'
orb = cv2.ORB_create(nfeatures=2000)

images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    classNames.append(os.path.splitext(cl)[0])

indexler = {
    0: "10",
    1: "100",
    2: "20",
    3: "200",
    4: "5",
    5: "50"
}

indexler_2 = {
    "1": "5",
    "2": "5",
    "3": "5",
    "4": "5",
    "5": "5",
    "6": "5",
    "7": "10",
    "8": "10",
    "9": "10",
    "10": "10",
    "11": "10",
    "12": "10",
    "13": "20",
    "14": "20",
    "15": "20",
    "16": "20",
    "17": "20",
    "18": "20",
    "19": "50",
    "20": "50",
    "21": "50",
    "22": "50",
    "23": "50",
    "24": "50",
    "25": "100",
    "26": "100",
    "27": "100",
    "28": "100",
    "29": "100",
    "30": "100",
}

def normalize_image(image,data):
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    return data

def tahmin_et(image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data = normalize_image(image,data)
    prediction = model.predict(data)
    #print(prediction)
    #print(image)
    #image.show()
    result = np.where(prediction[0] == max(prediction[0]))
    indexler[result[0][0]]
    return indexler[result[0][0]]

def findDes(images):
    desList=[]
    for img in images:
        kp,des = orb.detectAndCompute(img,None)
        desList.append(des)
    return desList

def findId(img, desList, thres=20):
    kp2 , des2 = orb.detectAndCompute(img,None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
        #print(matchList)
    except:
        pass
    print(matchList) ###gereksiz çıktıyı kapamak için sil
    if len(matchList)!=0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
    return finalVal

on_path = "indirilenler/on.png"
arka_path = "indirilenler/arka.png"
yildiz_path = "indirilenler/yildiz.png"
kare_path = "indirilenler/kare.png"

def is_exist():
    on_exists = os.path.exists(on_path)
    arka_exists = os.path.exists(arka_path)
    yildiz_exists = os.path.exists(yildiz_path)
    kare_exists = os.path.exists(kare_path)

    print("Fotoğrafların olma durumu :", on_exists, arka_exists, yildiz_exists, kare_exists)

    calisma_durumu = 0
    if (on_exists and arka_exists) == True:
        calisma_durumu = 1
    if (yildiz_exists and kare_exists) == True and calisma_durumu == 1:
        calisma_durumu = 2
    print("Çalışma Durumu : ",calisma_durumu)
    return calisma_durumu


def tahmin():
    calisma_durumu = is_exist()
    if calisma_durumu == 0 :
        return "Fotoğraflar eksik veya bir sorun oluştu."
    else:
        on = Image.open(on_path)
        arka = Image.open(arka_path)
        sonuc_on = tahmin_et(on)
        sonuc_arka = tahmin_et(arka)
        if sonuc_on == sonuc_arka:
            mesaj = "Paranin tutarı : "+str(sonuc_on)+"TL dir."
            if calisma_durumu == 2:
                yildiz = cv2.imread(yildiz_path)
                yildiz = cv2.cvtColor(yildiz, cv2.COLOR_BGR2GRAY)
                kare = cv2.imread(kare_path)
                kare = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)

                desList = findDes(images)
                yildiz_id = findId(yildiz, desList)
                kare_id = findId(kare, desList)

                sonuc_yildiz = indexler_2[classNames[yildiz_id]]
                sonuc_kare = indexler_2[classNames[kare_id]]

                if sonuc_yildiz == sonuc_kare:
                    mesaj = str(mesaj) + " Paranin gerçek olduğu düşünülüyor."
                else:
                    mesaj = str(mesaj) + " Paranin gerçek olduğu düşünülmüyor."
                shutil.rmtree('indirilenler')
                return str(mesaj)
            else:
                shutil.rmtree('indirilenler')
                return str(mesaj)
        else:
            mesaj = "Paranız tanımlanamıyor..."
            return str(mesaj)





