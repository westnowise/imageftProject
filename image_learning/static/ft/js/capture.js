// static/capture.js
document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('webcam');
    const captureBtn = document.getElementById('captureBtn');
    const capturedImage = document.getElementById('capturedImage');

    let stream;

    // 웹캠 스트림 시작
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (mediaStream) {
            video.srcObject = mediaStream;
            stream = mediaStream;
        })
        .catch(function (err) {
            console.error('Could not access the webcam: ', err);
        });

    // 버튼 클릭 시 이미지 캡처
    captureBtn.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        capturedImage.src = canvas.toDataURL('image/jpeg');
        capturedImage.style.display = 'block';
        
        // 이미지 서버로 전송 (AJAX 등을 사용하여 Django 뷰로 전송)
        fetch('http://localhost:8080/',  {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData }),
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error sending image to Unity:', error));
    });
});
