import sqlite3
import os
from shutil import copyfile
from tkinter import *
import cv2
import glob
import numpy as np
 #create our LBPH face recognizer 
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
subjects = ["", " ", " "," "," "]   
#function to detect face using OpenCV
def detect_face(img):
    #convert the test image to gray image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')

    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4)
    
    #if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None
    
    
    #extracting the face area
    (x, y, w, h) = faces[0]
    
    #return only the face part of the image
    return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):
    
    
    dirs = os.listdir(data_folder_path)
    
    #list to hold all subject faces
    faces = []
    #list to hold labels for all subjects
    labels = []
    
    # go through each directory and read images within it
    for dir_name in dirs:
        
        
        if not dir_name.startswith("s"):
            continue;
            
        
        label = int(dir_name.replace("s", ""))
        
        #build path of directory containin images for current subject subject
        #sample subject_dir_path = "training-data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name
        
        #get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)
        
        
        for image_name in subject_images_names:
            
            #ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;
            
            #build image path
            #sample image path = training-data/s1/1.pgm
            image_path = subject_dir_path + "/" + image_name

            #read image
            image = cv2.imread(image_path)
            
            #display an image window to show the image 
            cv2.imshow("Image Search", cv2.resize(image, (400, 500)))
            cv2.waitKey(100)
            
            #detect face
            face, rect = detect_face(image)
            
            
            if face is not None:
                #add face to list of faces
                faces.append(face)
                #add label for this face
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels
def predict(test_img):
    #make a copy of the image 
    img = test_img.copy()
    #detect face from the image
    face, rect = detect_face(img)

    #predict the image using our face recognizer '
    if not face is None:
        label, confidence = face_recognizer.predict(face)
        print(confidence)

        #get name of respective label returned by face recognizer
        label_text = subjects[label]
        print("--------------"+str(label))
        return label
    
    else:
        return -1
   # return img

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def connect():
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PHOTOS(Id INTEGER PRIMARY KEY,Path text,Uname text )")
    conn.commit()
    conn.close()

def insert(filepath, uname):
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO PHOTOS VALUES(NULL,?,?)",(filepath,uname))
    conn.commit()

    conn.close()
   # create_training_folder(filepath)

def view():
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM PHOTOS")
    rows=cur.fetchall()
    conn.close()
    return rows
def delete(id):
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM PHOTOS WHERE Id=?",(id,))
    conn.commit()
    conn.close()
def ImgSearch(ID,folderpath):
    
    print(123)
    print("Preparing data...")
    faces, labels = prepare_training_data("training-data")
    print("Data prepared")
   #train our face recognizer of our training faces
    face_recognizer.train(faces, np.array(labels))
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("SELECT Path FROM PHOTOS WHERE Id=?",(ID,))
    rows=cur.fetchall()
    print
    print("Predicting images...")
    #load test images
    print(rows[0][0])
    print("folderPath"+folderpath)
    testimg=cv2.imread(rows[0][0],-1)
    imglabel=predict(testimg)
    print("img1 done")
    images=glob.glob(folderpath+"/*.jpg")
    c=1
    for image in images:
        print("new iteration")
        img=cv2.imread(image,-1)
        lbl=predict(img)
        if lbl==imglabel:
            cv2.imwrite("Results/"+str(c)+".jpg",img)
            c=c+1
        #cv2.imwrite(str(c)+".jpg",img)
    top = Tk()
    top.geometry("100x100")
    def hello():
        messagebox.showinfo("image Search", "Search Complete")

    B1 = Button(top, text = "Search Complete.", command = hello)
    B1.place(x = 35,y = 50)

    top.mainloop()
        
    

def create_training_folder(filepath):
    
    conn=sqlite3.connect("project.db")
    cur=conn.cursor()
    cur.execute("SELECT Id FROM PHOTOS WHERE Path=?",(filepath,))
    rows=cur.fetchall()
    print(rows)
    
    print(type(rows[0][0]))
    dest="training-data/s"+str(rows[0][0])
    os.mkdir(dest)
    copyfile(filepath,dest+"/"+str(rows[0][0])+".jpg")
    cur.execute("UPDATE PHOTOS SET Path=? WHERE Path=?",(filepath,dest+"/"+str(rows[0][0])+".jpg"))
    conn.close()
   

connect()

#insert("D:/CSD 301/Project/opencv-face-recognition-python-master/opencv-face-recognition-python-master/test-data/test1.jpg","Test")
#print(view())
#delete(1)
#print(view())
#create_training_folder(" D:/CSD 301")