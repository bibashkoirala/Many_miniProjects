import csv
import os
import face_recognition as fr
import cv2
import numpy as np
import time

video_capture = cv2.VideoCapture(0)

# Load known faces
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
scanning_start_time = None  # Timestamp for the start of scanning

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
            cv2.putText(frame, "Congratulations " + name, bottom_left_corner_of_text, font, font_scale, font_color,
                        thickness, line_type)

            if name in students:
                students.remove(name)
                current_time = time.strftime("%H:%M:%S")
                lnwriter.writerow([name, current_time])

            last_known_name = name
            last_known_name_time = time.time()
            scanning_start_time = None

    if len(face_names) == 0:
        if scanning_start_time is None:
            scanning_start_time = time.time()
        else:
            scanning_duration = time.time() - scanning_start_time
            if scanning_duration >= 30:
                print("No one found for 30 seconds. Exiting...")
                break
    else:
        scanning_start_time = None

    # Check termination conditions
    if last_known_name is not None and (time.time() - last_known_name_time) > 5:
        print(" Thank you " + name)
        break

    # Display "Scanning in progress" if no match is found
    if len(face_names) == 0:
        cv2.putText(frame, "Scanning in progress...", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3, 2)

    cv2.imshow("Attendance", frame)
    cv2.waitKey(1)

# Display attendance message
if len(students) == 0:
    print("Attendance successful.")
else:
    print("Attendance incomplete. Missing students:", students)

video_capture.release()
cv2.destroyAllWindows()
f.close()
