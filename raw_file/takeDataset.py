############################################# IMPORTING ################################################
import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox as mess
# import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
# import pandas as pd
import datetime
import time

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
#####################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Ambil Gambar  >>>  2)Simpan Data"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Ambil Gambar  >>>  2)Simpan Data"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    columns = ['SERIAL NO.', '', 'NIM', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 50
            elif sampleNum > 50:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Foto diambil untuk NIM : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Masukan Nama Dengan Benar"
            message.configure(text=res)

########################################################################################

def TotalRegist():
    res=0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
                print(reader1)
        res = (res // 2) - 1
        csvFile1.close()
        return res
    else:
        res = 0
        return res

########################################################################################

def TrainImages():
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='Belum ada data', message='Silahkan Registrasi Terlebih Dahulu.')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Data Berhasil Disimpan"
    message1.configure(text=res)
    message.configure(text='Total Registrasi  : ' + str(TotalRegist()))

############################################################################################

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

        
######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }
        
        
######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#2d420a')

frame = tk.Frame(window, bg="grey")
frame.place(relx=0.3, rely=0.11, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Attendance" ,fg="white",bg="#2d420a" ,width=52 ,height=1,font=('comic', 29, ' bold '))
message3.place(x=10, y=10)

head2 = tk.Label(frame, text="                         Registrasi Wajah                          ", fg="black",bg="#00fcca" ,font=('comic', 17, ' bold ') )
head2.grid(row=0,column=0)

lbl = tk.Label(frame, text="Masukan NIM",width=20  ,height=1  ,fg="white"  ,bg="grey" ,font=('comic', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame, text="Masukan Nama",width=20  ,fg="white"  ,bg="grey" ,font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame, text="1)Ambil Gambar  >>>  2)Simpan Data" ,bg="grey" ,fg="white"  ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame, text="" ,bg="grey" ,fg="white"  ,width=37,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=3, y=450)

################# Inisialisasi Total Registrasi ###################

message.configure(text='Total Registrasi  : '+str(TotalRegist()))

###################### BUTTONS ##################################

clearButton = tk.Button(frame, text="Clear", command=clear  ,fg="black"  ,bg="#ff7221"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame, text="Clear", command=clear2  ,fg="black"  ,bg="#ff7221"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame, text="Ambil Gambar", command=TakeImages  ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame, text="Simpan Profil", command=TrainImages ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=30, y=380)
quitWindow = tk.Button(frame, text="Keluar", command=window.destroy  ,fg="black"  ,bg="#eb4600"  ,width=34 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=30, y=490)

##################### END ######################################

window.mainloop()

####################################################################################################