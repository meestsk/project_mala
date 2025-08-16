
function uploadImage() {
    const input = document.getElementById('cameraInput');
    if (input.files.length === 0) {
        alert('กรุณาเลือกไฟล์');
        return;
    }

    const file = input.files[0]; 
    const formData = new FormData();
    formData.append('image', file);

    const apiUrl = 'http://127.0.0.1:3000/detect';  

    fetch(apiUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.image) {
            document.getElementById('resultText').textContent = `ตรวจจับ ${data.count} ไม้`;
            document.getElementById('resultImage').src = `data:image/jpeg;base64,${data.image}`;
        } else {
            alert('ไม่สามารถตรวจจับไม้ได้');
        }
    })
    .catch(error => {
        alert('เกิดข้อผิดพลาดในการส่งคำขอ');
        console.error(error);
    });
}
