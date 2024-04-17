// 필터링을 통해 동화 검색 -> 검색 버튼이 필요 없을 듯
const searchInput = document.querySelector('.search-bar input[type="text"]');
        const items = document.querySelectorAll('.item');

        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase();

            items.forEach(item => {
                const titleText = item.querySelector('.ft_title').textContent.toLowerCase();

                if (titleText.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });

document.addEventListener('DOMContentLoaded', function() {
    // start.html로 이동하는 함수
    function redirectToStartPage() {
        window.location.href = '/'; // start.html로 이동
    }

    // "fas fa-chevron-right" 아이콘을 클릭하면 redirectToStartPage 함수 실행
    document.querySelector('.fas.fa-chevron-right').addEventListener('click', redirectToStartPage);
});

document.addEventListener('DOMContentLoaded', function() {
    // start.html로 이동하는 함수
    function redirectToStartPage() {
        window.location.href = '/';
    }

    // "fas fa-shopping-bag" 아이콘을 클릭하면 redirectToStartPage 함수 실행
    document.querySelector('.fas.fa-shopping-bag').addEventListener('click', redirectToStartPage);
});