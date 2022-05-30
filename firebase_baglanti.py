from firebase import Firebase
import os.path
import time

config = {
  "apiKey": "AIzaSyA3ABg4PSzJT--X2UZO5gtxb-MKXviKyEQ",
  "authDomain": "para-tanima.firebaseapp.com",
  "databaseURL": "https://para-tanima-default-rtdb.europe-west1.firebasedatabase.app",
  "storageBucket": "para-tanima.appspot.com"
}


firebase = Firebase(config)
storage = firebase.storage()



def resim_indir(path):
  try:
    os.mkdir("indirilenler")
  except:
    print("Klasör oluştururken hata meydana geldi.")
  print("Resimler İndiriliyor...")
  storage.child("images/"+path+"/arka_foto").download(filename="indirilenler/arka.png")
  storage.child("images/"+path+"/on_foto").download(filename="indirilenler/on.png")
  storage.child("images/"+path+"/yildiz_foto").download(filename="indirilenler/yildiz.png")
  storage.child("images/"+path+"/kare_foto").download(filename="indirilenler/kare.png")
  print("Resimler İndirildi.")

resim_indir("1348")

