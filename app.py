from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import base64
import os
from flask_cors import CORS
from ultralytics import YOLO

model = YOLO('best.pt')

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)


@app.route('/')
def index_page():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def send_css():
    return send_from_directory('.', 'style.css')

@app.route('/detect', methods=['POST'])
def detect_circles():
    if 'image' not in request.files:
        print("No image part")  
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        print("No selected file") 
        return jsonify({'error': 'No selected file'}), 400

    try:
        
        img_np = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        if img is None:
            print("Invalid image format")  
            return jsonify({'error': 'Invalid image format'}), 400

        print("Image loaded successfully")  

        # ใช้ภาพเดิมโดยไม่ต้องกรองสี
        results = model(img)[0]
        count = 0

        # ตรวจจับไม้และนับจำนวนที่พบ
        for box in results.boxes:
            count += 1
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  

        # แปลงภาพที่ตรวจจับแล้วเป็น base64 เพื่อนำไปแสดงผล
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        print(f"Detection count: {count}")  

        return jsonify({
            'count': count,  # จำนวนไม้ที่ตรวจจับได้
            'image': img_base64  # ภาพที่แสดงกรอบผลการตรวจจับ
        })

    except Exception as e:
        print(f"Error: {str(e)}")  
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
