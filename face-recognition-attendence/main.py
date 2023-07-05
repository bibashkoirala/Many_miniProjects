import csv
import os
import face_recognition as fr
import cv2
import numpy as np
import time

video_capture = cv2.VideoCapture(0)

# Load Known faces
known_face_names = {"Bibash"}

known_face_encodings = []
for name in known_face_names:
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "faces", f"{name}.jpg"))
    image = fr.load_image_file(image_path)
    encoding = fr.face_encodings(image)[0]
    known_face_encodings.append(encoding)

# List of expected students
students = known_face_names.copy()

face_locations = []
face_encodings = []

# Get the current date and time
current_date = time.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

unknown_face_count = 0  # Counter for unknown faces
last_known_name = None  # Track the last known name
last_known_name_time = time.time()  # Timestamp for the last known name appearance

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognize faces
    face_locations = fr.face_locations(rgb_small_frame)
    face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

    face_names = []  # Detected face names in the current frame

    for face_encoding in face_encodings:
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        face_distance = fr.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if matches[best_match_index]:
            name = list(known_face_names)[best_match_index]
            face_names.append(name)

            # Add the text if a person is present
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottom_left_corner_of_text = (10, 100)
            font_scale = 1.5
            font_color = (255, 0, 0)
            thickness = 3
            line_type = 2
            cv2.putText(frame, "You are " + name, bottom_left_corner_of_text, font, font_scale, font_color,
                        thickness, line_type)
            
            if name in students:
                students.remove(name)
                current_time = time.strftime("%H:%M:%S")
                lnwriter.writerow([name, current_time])

            last_known_name = name
            last_known_name_time = time.time()

            if last_known_name is not None:
                # Check if the last known face is no longer detected
                if last_known_name not in face_names:
                    # Display "not reachable, you will be signed out in 5 seconds"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottom_left_corner_of_text = (10, 100)
                    font_scale = 1.5
                    font_color = (255, 0, 0)
                    thickness = 3
                    line_type = 2
                    cv2.putText(frame, " verifing after lost connection", bottom_left_corner_of_text,
                                font, font_scale, font_color, thickness, line_type)

                    # Check if 5 seconds have passed since the last known face disappeared
                    if time.time() + last_known_name_time > 5:
                        break
                else:
                    cv2.putText(frame, "Scanning in progress...", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3, 2)
                    cv2.imshow("Attendance", frame)
                    cv2.waitKey(1)


        elif unknown_face_count >= 5:
            print("No match found. Please input a photo.")
            # Code to handle inputting photo and display "not verified"
            end_time = time.time() + 20
            while time.time() < end_time:
                _, frame = video_capture.read()
                cv2.putText(frame, "Not Verified. Please add Photo", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                            (255, 0, 0), 3, 2)
                cv2.imshow("Attendance", frame)
                cv2.waitKey(1)
                break

    if len(face_names) == 0:
        unknown_face_count += 1
    else:
        unknown_face_count = 0

    
   
    # Check termination conditions
    if last_known_name is not None and (time.time() - last_known_name_time) > 10:
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
