from django.http import JsonResponse  
from django.shortcuts import render
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

# Create your views here.
def index(request):
    return render(request,'ft/image.html')

# def capture_image(request):
#     if request.method == 'POST' and 'image' in request.POST:
#        image_data = request.POST['image']
#        with open('./image_learning/static/captured_image.jpg', 'wb') as f:
#            f.write(image_data.split(',')[1].decode('base64'))
#        return JsonResponse({'message': 'Image captured successfully.'})
#    else:
#        return JsonResponse({'error': 'Invalid request method or image data missing.'}, status=400)
    

# def capture_image(request):
#     if request.method == 'POST' and 'image' in request.POST:
#         # 캡처한 이미지 받아오기
#         image_data = request.POST['image']
#         # 이미지를 파일로 저장
#         image_data = base64.b64decode(image_data.split(',')[1])

#         # 배경 제거
#         input_image = Image.open(BytesIO(image_data))
#         output_image = remove(input_image)

#         # 임시로 배경이 제거된 이미지 저장
#         output_image_path = 'image_learning/static/img'
#         output_image.save(output_image_path)

#         # HTML 페이지에 이미지 경로 전달
#         return JsonResponse({'message': 'Image captured and background removed successfully.', 'image_url': '/static/removed_bg_image.png'})
#     else:
#         return JsonResponse({'error': 'Invalid request method or image data missing.'}, status=400)

import tempfile
import os

def capture_image(request):
    if request.method == 'POST' and 'image' in request.POST:
        # 캡처한 이미지 받아오기
        image_data = request.POST['image']
        # 이미지를 파일로 저장
        image_data = base64.b64decode(image_data.split(',')[1])

        # 배경 제거
        input_image = Image.open(BytesIO(image_data))
        output_image = remove(input_image)

       # 배경이 제거된 이미지를 저장할 폴더 경로
        output_image_dir = r'C:\Users\user\Downloads\fakeosmo\fakeosmo\image_learning\static\img'
        # 저장할 이미지 파일의 이름
        output_image_filename = 'removed_bg_image.png'
        # 저장할 이미지 파일의 전체 경로
        output_image_path = os.path.join(output_image_dir, output_image_filename)

        # 폴더가 없으면 생성
        os.makedirs(output_image_dir, exist_ok=True)

        # 배경이 제거된 이미지를 저장
        output_image.save(output_image_path)

        # 클라이언트에게 전달할 이미지 경로
        image_url = '/static/img/' + output_image_filename

        # 임시 파일로 배경이 제거된 이미지 저장
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            output_image.save(temp_file)

            # HTML 페이지에 이미지 경로 전달
            return JsonResponse({'message': 'Image captured and background removed successfully.', 'image_url': image_url})
    else:
        return JsonResponse({'error': 'Invalid request method or image data missing.'}, status=400)
