import cv2
import easyocr
import time
import pyttsx3

reader = easyocr.Reader(["es"], gpu=True)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'spanish')
engine.setProperty('volume', 1)

while True:
     ret, frame = cap.read()
     if ret == False:
          break
     start = time.time()
     result = reader.readtext(frame, detail = 0)
     if result != []:
        print (result)
        engine.say(result)
        engine.runAndWait()
        for i in str(result):
            if i.isalpha():
                print (i)
                engine.say(i)
                engine.runAndWait()
     
     end = time.time()
     fps = 1 / (end - start)
     cv2.putText(frame, "FPS: {:.2f}".format(fps), (20, 400), 1, 2, (0, 255, 0), 2)
     cv2.imshow("Frame", frame)
     k = cv2.waitKey(1) & 0xFF
     if k == 27:
          break

cap.release()
cv2.destroyAllWindows()
