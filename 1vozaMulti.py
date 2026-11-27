import cv2
import multiprocessing
import speech_recognition as sr
import pyttsx3
import os

# image path 
# dir_name = r'C:\Users\vhugo\Documents\ProyectosPython\Mediapipe\handlandmarks\lenguajeDeSenas\alfabetoSenas'
dir_name = r'.\alfabetoSenas'

engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'spanish')
engine.setProperty('volume', 1)
 
def video_capture(queue):
    last_text = "   "
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        #windowWidth=frame.shape[1]
        #windowHeight=frame.shape[0]
        #print(windowWidth)
        #print(windowHeight)
        # Check if there's a new message to display
        if not queue.empty():
            text = queue.get()
            #cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            #cv2.putText(frame, "Traduciendo lo hablado...", (20, 440), 1, 2, (0, 255, 0), 2)
            last_text = text
            if text == "salir":
                break
        else:
            #cv2.putText(frame, last_text, (20, 460), 1, 2, (0, 255, 0), 2
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
            cv2.putText(frame, last_text, (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
            #image = cv2.rectangle(frame, (windowWidth-100, 0), (windowWidth, 100), (255, 255, 255), -1)
            #cv2.imshow("Frame", image)
            suffix = '.png'
            if last_text.isalpha():
                if last_text == "á":
                    last_text = "a"
                elif last_text == "é":
                    last_text = "e"
                elif last_text == "í":
                    last_text = "i"
                elif last_text == "ó":
                    last_text = "o"
                elif last_text == "ú":
                    last_text = "u"
                elif last_text == "ñ":
                    last_text = "n"
                    
                file_name = os.path.join(dir_name, last_text + suffix)
                #print(file_name)
                image = cv2.imread(file_name)
                cv2.imshow("LSM", image) 
            
        cv2.imshow("Frame", frame)
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            queue.put("salir")
            break

    cap.release()
    cv2.destroyAllWindows()

def speech_to_text(queue):
    last_text = "   "
    recognizer = sr.Recognizer()
    mic = sr.Microphone(1)

    while True:
        with mic as source:
            print("Habla al microfono!...")
            audio = recognizer.record(source, duration=3)
        
        try:
            text = recognizer.recognize_google(audio,language="es-ES")
            print(f"Reconocido: {text}")
            #queue.put(text)
            if text == "salir":
                queue.put(text)
                break
            engine.say(text)
            engine.runAndWait()
            for i in str(text):
                if i.isalpha():
                    print (i)
                    queue.put(i)
                    engine.say(i)
                    engine.runAndWait()
            last_text = text
            #queue.put(text)
            
            
        except sr.UnknownValueError:
            print("Lo siento, no entiendo lo que dices!")
        except sr.RequestError:
            print("No se pudo realizar la traduccion!!!; {0}")
            
        if not queue.empty():
            text = queue.get()
            if text == "salir":
                break

if __name__ == "__main__":
    # Create a queue to share data between processes
    queue = multiprocessing.Queue()

    # Create a process for video capture and another for speech recognition
    video_process = multiprocessing.Process(target=video_capture, args=(queue,))
    speech_process = multiprocessing.Process(target=speech_to_text, args=(queue,))

    # Start the processes
    video_process.start()
    speech_process.start()

    # Wait for both processes to finish
    video_process.join()
    speech_process.join()
