$(document).ready(function() {
    // 이미지 및 목표 이미지의 경로 설정
    var hatPath = '{% static "Filters/red_hood(2).png" %}';
    var basketPath = '{% static "Images/target.png" %}';

    // 이미지 컨테이너 선택 및 크기 설정
    var imageContainer = $('#image-container');
    var containerWidth = imageContainer.width();
    var containerHeight = imageContainer.height();

    // 목표 이미지 추가
    var targetImage = $('<img id="target-image" src="' + basketPath + '">');
    imageContainer.append(targetImage);

    // 드래그 가능한 이미지 추가 및 이벤트 설정
    var dragImages = [
        { path: '{% static "Images/ImagesPNG/image1.png" %}', position: { top: 50, left: 50 } },
        { path: '{% static "Images/ImagesPNG/image2.png" %}', position: { top: 50, left: 200 } },
        { path: '{% static "Images/ImagesPNG/image3.png" %}', position: { top: 50, left: 350 } }
    ];

    $.each(dragImages, function(index, dragImage) {
        var draggableImage = $('<img class="draggable-image" src="' + dragImage.path + '">');
        draggableImage.css(dragImage.position);
        imageContainer.append(draggableImage);

        // 드래그 기능 추가
        draggableImage.draggable({
            containment: 'parent' // 부모 요소 내에서만 드래그 가능하도록 설정
        });
    });
});
