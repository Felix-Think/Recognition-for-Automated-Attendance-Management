import csv
import os, cv2
import tkinter as tk

def DetectFace(haarcasecade_path, image):
    face_cascade = cv2.CascadeClassifier(haarcasecade_path)
    #Change color to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Detect face in gray_image
    face = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    
    return face, gray_image
# Take Image of user
def TakeImage(EmployeeID, Name,haarcasecade_path,image_path):
    #Create Camera
    camera = cv2.VideoCapture(0)
    sampleNum = 0
    #Create Directory for new employee
    while True:
        #Take a image
        ret, image = camera.read()
        face, gray_image = DetectFace(haarcasecade_path, image)
        for (x, y, w, h) in face:
            #Create rectangle around detected face
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sampleNum+=1
            #Save image
            cv2.imwrite(
                    f"{image_path}/ "
                    + Name
                    + "_"
                    + EmployeeID
                    + "_"
                    + str(sampleNum)
                    + ".jpg",
                    gray_image[y : y + h, x : x + w],
                )
            #Show camera
            cv2.imshow("Image", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        elif sampleNum > 50:
            break
    camera.release()
    cv2.destroyAllWindows()
    
    
def Register(EmployeeID, Name,trainimage_path,haarcasecade_path):
    directory = EmployeeID + "_" + Name
    image_path = os.path.join(trainimage_path, directory)
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    row = [EmployeeID, Name]
    TakeImage(EmployeeID, Name,haarcasecade_path,image_path)
    with open("EmployeeDetails/employeeDetails.csv","a+",) as csvFile:
        writer = csv.writer(csvFile, delimiter=",")
        writer.writerow(row)
        csvFile.close()