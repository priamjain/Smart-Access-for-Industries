import cv2 
import numpy as np 
import pandas as pd 

from npwriter import f_name 
from sklearn.neighbors import KNeighborsClassifier 
from collections import Counter

def fun():
    
    # reading the data 
    data = pd.read_csv(f_name).values 

    # data partition 
    X, Y = data[:, 1:-1], data[:, -1] 

    print(X, Y) 

    # Knn function calling with k = 5 
    model = KNeighborsClassifier(n_neighbors = 5) 

    # fdtraining of model 
    model.fit(X, Y) 

    cap = cv2.VideoCapture(0) 

    classifier = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml") 

    f_list = []
    names=[]

    while True: 

            ret, frame = cap.read() 

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

            faces = classifier.detectMultiScale(gray, 1.5, 5) 

            X_test = []
      


            # Testing data 
            for face in faces: 
                    x, y, w, h = face 
                    im_face = gray[y:y + h, x:x + w] 
                    im_face = cv2.resize(im_face, (100, 100)) 
                    X_test.append(im_face.reshape(-1)) 

            if len(faces)>0: 
                    response = model.predict(np.array(X_test))
                    names.append(response[0])
                    
                    # prediction of result using knn 

                    for i, face in enumerate(faces): 
                            x, y, w, h = face 

                             
                            cv2.rectangle(frame, (x, y), (x + w, y + h), 
                                                                       (255, 0, 0), 3) 

                             
                            cv2.putText(frame, response[i], (x-50, y-50), 
                                                            cv2.FONT_HERSHEY_DUPLEX, 2, 
                                                                                    (0, 255, 0), 3)
                            
            
            
            cv2.imshow("full", frame) 

            if(len(names)>100):
                break
            
            key = cv2.waitKey(1) 

            if key & 0xFF == ord("q"):
                break
            
            
    cap.release() 
    cv2.destroyAllWindows()

    c=Counter(names)
    most_occur=c.most_common(4)
    return(most_occur[0][0])
    

if (__name__=='__main__'):
    fun()
    
