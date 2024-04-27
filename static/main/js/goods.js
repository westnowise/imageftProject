document.addEventListener('DOMContentLoaded', function() {
    // 첫 번째 코드 블록
    const back = document.querySelector('.icon-container');
    const calendarIcon = document.querySelector(".icon-container i.far.fa-calendar-alt");
    const calendarModal = document.getElementById("calendar-modal");

    function centerModal() {
        const modalWidth = calendarModal.offsetWidth;
        const modalHeight = calendarModal.offsetHeight;
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const leftPosition = (windowWidth - modalWidth) / 2;
        const topPosition = (windowHeight - modalHeight) / 2;
        calendarModal.style.left = leftPosition + "px";
        calendarModal.style.top = topPosition + "px";
    }

    window.addEventListener('resize', centerModal);
    back.addEventListener('click', function(event) {
        event.stopPropagation();
        window.location.href = "/start";
    });

    calendarModal.style.display = 'none';
    calendarIcon.addEventListener('click', function(event) {
        event.stopPropagation();
        calendarModal.style.display = 'block';
        centerModal();
    });

    window.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            calendarModal.style.display = 'none';
        }
    });

    document.querySelector('.scriptCalendar tbody').addEventListener('click', function(event) {
        const target = event.target;
        if (target.tagName === 'TD' && !target.classList.contains('calendarBtn')) {
            const selectedYear = document.getElementById('calYear').innerText;
            const selectedMonth = document.getElementById('calMonth').innerText;
            const selectedDay = target.innerText;
            const selectedDate = `${selectedYear}-${selectedMonth.padStart(2, '0')}-${selectedDay.padStart(2, '0')}`;
            console.log('Selected date:', selectedDate);
            calendarModal.style.display = 'none';
        }
    });

    // 두 번째 코드 블록
    const images = document.querySelectorAll(".db-image img");
    const leftArrow = document.querySelector(".arrow_left");
    const rightArrow = document.querySelector(".arrow_right");
    let currentImageIndex = 0;
    let imagesData = [];

    function fetchImages() {
        fetch('/get-images/')
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                imagesData = data.images;
                updateImages();
            } else {
                console.error('No images data available');
            }
        })
        .catch(error => console.error('Error loading images:', error));
    }

    function updateImages() {
        if (!imagesData.length) {
            console.error('No images data available');
            return;
        }
        images.forEach((img, index) => {
            const imageData = imagesData[currentImageIndex];
            if (imageData && imageData.image) {
                img.src = `data:image/png;base64,${imageData.image}`;
            } else {
                console.error('Invalid or missing image data at index:', currentImageIndex);
                img.src = '';
            }
        });
    }

    leftArrow.addEventListener('click', function() {
        currentImageIndex = (currentImageIndex - 1 + imagesData.length) % imagesData.length;
        updateImages();
    });

    rightArrow.addEventListener('click', function() {
        currentImageIndex = (currentImageIndex + 1) % imagesData.length;
        updateImages();
    });

    fetchImages();
});