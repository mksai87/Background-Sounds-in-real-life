
import cv2
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import random
import pygame
import threading
from deepface import DeepFace



def play_random_music(emotion):
    global previous_emotion
    pygame.mixer.init()
    while True:
        if emotion not in emotions:
            print("Invalid emotion. Please enter one of: ", emotions)
            emotion = input("Enter your current emotion: ")
            continue
        
        directory = emotion.lower()
        files = os.listdir(f'C:/Users/user/Desktop/ff/Emotion_Detection_CNN-main/{directory}')
        
        if len(files) == 0:
            print("No music files found for", emotion)
            emotion = input("Enter your current emotion: ")
            continue
        
        random_music = random.choice(files)
        print("Playing", random_music)
        pygame.mixer.music.load(f'C:/Users/user/Desktop/ff/Emotion_Detection_CNN-main/{directory}/{random_music}')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            if new_emotion_event.is_set():
                new_emotion_event.clear()
                emotion = new_emotion[0]
                if emotion != previous_emotion:
                    previous_emotion = emotion
                    break

def get_emotion():
    global new_emotion
    while True:
        emotion = input("Enter a new emotion or 'quit' to stop: ")
        if emotion.lower() == 'quit':
            new_emotion_event.set()
            break
        elif emotion.lower() in emotions:
            new_emotion[0] = emotion
            new_emotion_event.set()
        else:
            print("Invalid emotion. Please enter one of: ", emotions)

def detect_emotion(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        try:
            face_img = frame[y:y+h, x:x+w]
            analyze = DeepFace.analyze(face_img, actions=['emotion'])
            dominant_emotion = analyze[0]['dominant_emotion']
            cv2.putText(frame, dominant_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            new_emotion[0] = dominant_emotion
            new_emotion_event.set()
        except Exception as e:
            print("Error analyzing emotion:", str(e))
            print("No face detected.")

# Initialize face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Check if the cascade classifier was loaded successfully
if face_cascade.empty():
    print("Error: Failed to load the face cascade classifier.")
    exit()

# Define emotions list
emotions = ['angry', 'disgust', 'happy', 'fear', 'sad', 'surprise', 'neutral']

# Initialize pygame
pygame.mixer.init()

# Create an event to signal a new emotion
new_emotion_event = threading.Event()
new_emotion = ['']

# Variable to store previous emotion
previous_emotion = ''

# Start the emotion input thread
input_thread = threading.Thread(target=get_emotion)
input_thread.start()

# Start the music playing thread
music_thread = threading.Thread(target=play_random_music, args=('neutral',))
music_thread.start()

# Open video capture device
url='http://192.168.130.97:81/stream'
video = cv2.VideoCapture(0)

# Main loop to capture and process frames
while video.isOpened():
    _, frame = video.read()
    if frame is None:
        break
    
    # Detect faces and emotions
    detect_emotion(frame)
    
    # Display the frame
    cv2.imshow('video', frame)
    
    # Check for key press
    key = cv2.waitKey(1)
    if key == ord('o'):
        break

# Release video capture device and close all windows
video.release()
cv2.destroyAllWindows()

