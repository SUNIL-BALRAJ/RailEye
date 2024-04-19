import os
import shutil
import torch
import cv2
import time

cap = cv2.VideoCapture('C:/Users/sumit/OneDrive/Desktop/RailEye/static/assets/crowd.mp4')

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
bbox_count = 0
red_bbox_count = 0  # Variable to count red color bounding boxes within the ROI
person_count = 0  # Variable to count persons within the restricted area

raimg_folder = 'raimg'
# Delete existing images in the 'raimg' folder
if os.path.exists(raimg_folder):
    shutil.rmtree(raimg_folder)
os.makedirs(raimg_folder)

frame_number = 0
frames_saved = 0
start_time = time.time()
first_frame_saved = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))
    results = model(frame)

    roi = frame[0:130, 1:182]

    bbox_count = 0
    red_bbox_count = 0
    person_count = 0

    for index, row in results.pandas().xyxy[0].iterrows():
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        class_name = row['name']
        bbox_count += 1

        if class_name == 'person':
            person_count += 1
            
            if x1 >= 784 and x2 <= 1014 and y1 >= 314 and y2 <= 498:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                red_bbox_count += 1
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.putText(frame, f'Crowd Count: {bbox_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Restricted area count: {red_bbox_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Uncomment the next two lines if you want to display the frame (not recommended if you're not viewing it)
    # cv2.imshow("ROI", frame)
    # if cv2.waitKey(1) & 0xFF == 27:
    #     break
    
    if red_bbox_count > 0 and frames_saved < 10:
        if not first_frame_saved:
            first_frame_saved = True
            frame_number += 1
            image_path = os.path.join(raimg_folder, f'{frame_number}.jpg')
            cv2.imwrite(image_path, frame)
            frames_saved += 1
            start_time = time.time()
        elif time.time() - start_time >= 1:
            frame_number += 1
            image_path = os.path.join(raimg_folder, f'{frame_number}.jpg')
            cv2.imwrite(image_path, frame)
            frames_saved += 1
            start_time = time.time()

cap.release()
# cv2.destroyAllWindows()  # No need to destroy windows if not created