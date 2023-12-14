# # #working with Sample images as reference but as single not from database !!
# # #laucher use env

import cv2
import face_recognition
import serial
import time


arduino = serial.Serial('COM8', 9600) 

sample_images = ["sample1.jpg", "sample2.jpg"]
sample_face_encodings = []

# Encoding all the images from the database
for sample_image in sample_images:
    image = face_recognition.load_image_file(sample_image)
    face_encoding = face_recognition.face_encodings(image)[0]
    sample_face_encodings.append(face_encoding)

cap = cv2.VideoCapture(0)

scanning_faces = True  #face scanning->true in starting 

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    if scanning_faces:
        # Display message on the frame when scanning faces
        cv2.putText(frame, "Scanning Faces", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    face_locations = face_recognition.face_locations(frame)
    
    access_granted = False  # access_granted->False 
    
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_encodings = face_recognition.face_encodings(frame, [face_location])

        for sample_face_encoding in sample_face_encodings:
            match = face_recognition.compare_faces([sample_face_encoding], face_encodings[0])
            if match[0]:
                access_granted = True  # Update access_granted flag if a match is found
                break  

        if access_granted:
            text = "Access Granted"
            color = (0, 255, 0)  # Green
        else:
            text = "Access Denied"
            color = (0, 0, 255)  # Red
        
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


        project_info_text = "Minor Project - Jatin (Face Entry)"
        text_size = cv2.getTextSize(project_info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = frame.shape[1] - text_size[0] - 50  
        cv2.putText(frame, project_info_text, (text_x, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Sending Message to Ardunio 
    if scanning_faces:
        arduino.write(b'Scanning Faces\n')
        scanning_faces = False  #scan complete then false
    else:
        if access_granted:
            access_result = "Access Granted"
        else:
            access_result = "Access Denied"
        
        arduino.write(access_result.encode())
        time.sleep(1)  

cap.release()
cv2.destroyAllWindows()


#donedonedone