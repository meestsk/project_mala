from ultralytics import YOLO
import os
import cv2
import numpy as np 

model = YOLO('best.pt')

image_dir = r"C:\Users\windows 10\ProjectMala\datasets\test\images"

output_dir = r"C:\Users\windows 10\ProjectMala\results"
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(image_dir):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_dir, file)
        print(f"🔍 Detecting: {image_path}")

        results = model(image_path)[0]
        
        #conf_thres: ค่าความมั่นใจขั้นต่ำสำหรับการตรวจจับวัตถุ
        # iou_thres: ค่าการทับซ้อนของกรอบ (Intersection over Union) สำหรับการยกเลิกการตรวจจับที่ซ้ำกัน

        wanted_ids = [0, 1, 2, 3, 4]
        boxes = results.boxes
        confidence_threshold = 0.96
        boxes = results[0].boxes
        keep = [i for i in range(len(boxes.cls)) if int(boxes.cls[i]) in wanted_ids ]
        #in wanted_ids
        #and boxes.conf[i] > confidence_threshold
      
        results[0].boxes = boxes[keep]

        result_image = results[0].plot()
        
        output_path = os.path.join(output_dir, file)
        cv2.imwrite(output_path, result_image)

print(" เสร็จสิ้น: ตรวจจับเฉพาะ class ที่ต้องการและบันทึกเรียบร้อยแล้ว")
