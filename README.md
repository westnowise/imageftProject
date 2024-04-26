# 👸매일 듣는 동화 이야기
![image](https://github.com/westnowise/imageftProject/assets/98007431/914762bc-28a6-4b60-ac2b-9c74535d4cf4)

### 👶체감형-교육 프로그램

 해당 프로젝트는 학습자인 만4~5세 유아들이 학습할 수 있는 체감형 교육 컨텐츠를 제작하고, 웹으로 배포하는 것을 목표로 한다.

 유아의 학습 활동은 인지 및 신체 발달, 지식을 향상시킬 수 있는 효율적인 방법으로,  학습자가 그린 그림을 웹캠으로 인식하여 배경과 피사체를 분리하고 피사체만 DB에 저장 후 동화 비디오에 합성하는 이미지 인식 동화 컨텐츠와. 학습자의 웹캠을 통해 학습자의 손 동작을 인식하여 화면 속 알맞은 금액의 동전을 바구니에 올바르게 넣는 모션 인식 게임을 제작하였다.



## 🔖 Guide
### Needed
    python 3.11.7 # 7 이상 버전
    pip install -r requirement.txt
    pip install pydub simpleaudio # 오류 발생 가능

pip install pydub 오류 발생 시
1) Microsoft Visual C++ Build Tools 설치

https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/

설치 시 "C++ 데스크톱 개발" 워크로드를 포함


2) ffmpeg 환경변수 설정
   - ffmpeg 설치 https%3A%2F%2Fkminito.tistory.com%2F108
  
    echo %SDL_AUDIODRIVER%     # CMD
    set SDL_AUDIODRIVER= (편집됨)

3) 재부팅 후 pip install pydub 재실행



### Running
    python -m venv myvenv
    # 가상환경 접속
    source /myvenv/bin/activate
    # Needed pip 설치 
    cd /Dproject
    python manage.py runserver





## 👨‍👩‍👧‍👦Member
### PM   
|              | 역할                            | git |
| ------------- | ---------------------------------- | ------------------- | 
| 정하민 | 프로젝트 팀장 | |
| 조나희 | UI, UX 디자인 | |
| 임희승 | 컨텐츠 제작 | |

### Develop
|               | 역할                             | git|
| ------------- | ---------------------------------- | ------- | 
| 송희도 | 개발 PL, DB 구축, 웹 제작 및 배포 ||
| 윤소현 | 모션인식,  웹 배포 ||
| 이수현 | 모션인식, 프론트 ||
| 박수아 | 영상처리, 프론트 ||
| 조서현 | 이미지 전처리,  웹 제작 및 배포 ||


