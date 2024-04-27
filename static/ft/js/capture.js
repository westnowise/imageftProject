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
        // 10초 뒤에 이미지 캡처 실행
        setTimeout(function () {
            // 기존에 추가된 배경 제거된 이미지 삭제
            const previousRemovedBgImage = document.querySelector('.removed-bg-image');
            if (previousRemovedBgImage) {
                previousRemovedBgImage.remove();
            }
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
            capturedImage.src = canvas.toDataURL('image/jpeg');
            capturedImage.style.display = 'block';
            
            // CSRF 토큰 가져오기
            const csrftoken = getCookie('csrftoken');
            
            // 이미지 서버로 전송 (폼 데이터로 전송)
            const formData = new FormData();
            formData.append('image', canvas.toDataURL('image/jpeg'));
            
            fetch('/capture/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken  // CSRF 토큰 추가
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                // 서버로부터의 응답에서 배경이 제거된 이미지의 URL을 추출
                const removedBgImageUrl = data.image_url;
                
                // 이미지를 표시할 <img> 요소 생성
                const removedBgImage = document.createElement('img');
                removedBgImage.src = removedBgImageUrl;
                removedBgImage.classList.add('removed-bg-image'); // 클래스 추가
                
                // 이미지를 표시할 HTML 요소에 추가
                document.body.appendChild(removedBgImage);
            })
            .catch(error => console.error('Error capturing image:', error));
        }, 10000); // 10초 후에 캡처 실행
    });

    // CSRF 토큰을 쿠키에서 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
