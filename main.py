import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# --- CONFIGURATION ---
PATH = 'images'   # Folder where student photos are stored
images = []       # List to store the image pixel data
classNames = []   # List to store the names (filenames)
all_images = os.listdir(PATH) # Get all files in the 'images' folder

print(f"1. Loading Student Database from '{PATH}'...")

# --- LOAD IMAGES ---
for cI in all_images:
    # Read the image using OpenCV
    curImg = cv2.imread(f'{PATH}/{cI}')
    images.append(curImg)
    # Extract the name (remove .jpg)
    classNames.append(os.path.splitext(cI)[0])

print(f"   Students Found: {classNames}")

# --- FUNCTION: ENCODE FACES ---
def findEncodings(images):
    encodeList = []
    for img in images:
        # OpenCV uses BGR, but face_recognition uses RGB. Convert it.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Generate the 128-number encoding
        # [0] grabs the first face found in the photo
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print(f"No face found in one of the images. Skipping.")
    return encodeList

# --- FUNCTION: MARK ATTENDANCE ---
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        
        # Get today's date 
        now = datetime.now()
        todayStr = now.strftime('%d-%m-%Y')
        
        # Check specific attendance for TODAY
        marked_today = False
        for line in myDataList:
            entry = line.split(',')
            
            if len(entry) > 1: # Safety check to ensure line isn't empty
                saved_name = entry[0]
                saved_date = entry[1]
                
                if name == saved_name and todayStr == saved_date:
                    marked_today = True
                    break
            
        # Only write if NOT marked today
        if not marked_today:
            timeStr = now.strftime('%H:%M:%S')
            # Write Name, Date, AND Time
            f.writelines(f'\n{name},{todayStr},{timeStr}')
            print(f"   [SUCCESS] Attendance Marked: {name} at {timeStr}")

# --- MAIN EXECUTION ---
print("2. Processing Encodings (This may take a moment)...")
encodeListKnown = findEncodings(images)
print(f"   Encoding Complete. System Ready.")

# Start the Webcam
cap = cv2.VideoCapture(0)
print("3. Camera Active. Press 'q' to quit.")

while True:
    # Get frame from webcam
    success, img = cap.read()
    
    # Resize to 1/4th size for speed
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Loop through all faces found in the webcam
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        # Compare with known faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        # Get the best match (lowest distance)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            # Draw Box (Scale up by 4 because we resized down by 4)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            # Log it
            markAttendance(name)
        else:
            # Optional: Mark unknown faces as RED
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Show the webcam window
    cv2.imshow('Webcam', img)
    
    # Press 'q' to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()