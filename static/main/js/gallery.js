document.addEventListener('DOMContentLoaded', function() {
    // 이전 페이지로 이동하는 함수
    function goBack() {
        window.history.back();
    }

    // 버튼 클릭 시 이전 페이지로 이동하는 이벤트 핸들러 연결
    document.querySelector('.g_arr_left').addEventListener('click', goBack);
});
