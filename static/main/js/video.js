document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('popupButton');
    const video = document.getElementById('videoPlayer');
    
    // 버튼 클릭 이벤트 리스너
    button.addEventListener('click', function () {
        displayPopup();
    });
    
    // 팝업 창 표시 함수
    function displayPopup() {
        // 팝업 창을 여기에 구현
        alert('Popup is displayed!');
    }
});