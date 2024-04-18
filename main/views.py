from django.shortcuts import render
from ft.models import FairyTale 
import base64
import cv2

def main(request):
    return render(request, 'main/main.html')

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # 사용자의 FairyTale 객체 정보를 조회
        user_fairytales = FairyTale.objects.filter(user=request.user)

         # 바이너리 이미지 데이터를 Base64로 인코딩하여 템플릿에 전달
        for fairy_tale in user_fairytales:
            if fairy_tale.image:
                fairy_tale.base64_image = base64.b64encode(fairy_tale.image).decode('utf-8')


        # 템플릿에 전달할 컨텍스트 데이터
        context = {
            'user_fairytales': user_fairytales,
            'next_page': 'main2'
        }

        return render(request, 'main/index.html', context)
    else:
        return render(request, 'main/index.html')

def main2(request):
    return render(request, 'main/index2.html')

def main3(request):
    context = {'next_page': 'main4/'}
    return render(request, 'main/index3.html', context)

def main4(request):
    return render(request, 'main/index4.html')