from ultralytics import YOLO

model = YOLO("yolov8n.pt")


model.train(data=r"C:\Users\windows 10\ProjectMala\datasets\data.yaml", 
            epochs=100, 
            imgsz=640, 
            batch=16)
