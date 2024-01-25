import face_recognition
import cv2
import numpy as np
import os
import xlwt
from xlwt import Workbook
from datetime import date
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

face_locations = []
face_encodings = []
face_names = []

CurrentFolder = os.getcwd() #Read current folder path
image = CurrentFolder+'\\ARU.jpg'
image2 = CurrentFolder+'\\BKD.jpg'

video_capture = cv2.VideoCapture(0)

#images that needs to be recogonized 01
p1_name = "Aarushi"
p1_image = face_recognition.load_image_file(image)
p1_face_encoding = face_recognition.face_encodings(p1_image)[0]
#02
p2_name = "PAPA"
p2_image = face_recognition.load_image_file(image2)
p2_face_encoding = face_recognition.face_encodings(p2_image)[0]

known_face_encodings = [
    p1_face_encoding,
    p2_face_encoding
]
known_face_names = [
    p1_name,
    p2_name
]
process_this_frame = True

rb = xlrd.open_workbook('attendence_excel.xls', formatting_info=True) 
wb = xl_copy(rb)
inp = input('Please give current subject lecture name')
sheet1 = wb.add_sheet(inp)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))
row=1
col=0
already_attendence_taken = ""
while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    if((already_attendence_taken != name) and (name != "Unknown")):
                     sheet1.write(row, col, name )
                     col =col+1
                     sheet1.write(row, col, "Present" )
                     row = row+1
                     col = 0
                     print("attendence taken")
                     wb.save('attendence_excel.xls')
                     already_attendence_taken = name
                    else:
                     print("next student")
                        
            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xff==ord('q'):   
                print("data save")
                break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
