# 너의 기름은?

<img src="https://user-images.githubusercontent.com/47537803/229174640-f3067963-1008-4c8d-9ba4-bf65bb0792dc.png" width="700" height="400">

> 개발 기간: 2023.03.27 ~ 2023.03.30</p>🎥 시연영상 https://www.youtube.com/watch?v=9THfgrYiP5I


## 🖐프로젝트 소개
당신의 기름, 이대로 괜찮은가요?

주유소 검색 서비스, '너의 기름은?'은 사용자가 검색한 위치 기반, 휘발유 저가순으로 주유소 목록 확인이 가능합니다.

주유소에 대한 리뷰도 확인하고, 직접 작성도 해보자구요!

## 👨‍👩‍👧팀원
|이름|역할|
|------|---|
|전정훈</br>[@jeonghunjeon](https://github.com/jeonghunjeon)|- 메인 화면 UI</br>- 오피넷API, 카카오맵API</br>- 검색 기능|
|오승연</br>[@O-Wensu](https://github.com/O-Wensu)|- 회원가입, 주유소 목록 화면 UI</br>- 회원가입, 로그인, 로그아웃</br>- 검색 기능|
|이현규</br>[@OliveLover](https://github.com/OliveLover)|- 로그인, 리뷰 화면 UI</br>- 리뷰 조회/작성/수정/삭제|
|이재호</br>[@spainclub](https://github.com/spainclub)|- 오피넷API, 카카오맵API </br>- 서버 배포|

## 🔨 기술 스택
<img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=white"> <img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=Css3&logoColor=white"> <img src="https://img.shields.io/badge/Javascript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=black"> <img src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jQuery&logoColor=white">

<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white"> <img src="https://img.shields.io/badge/Mongo DB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white"> <img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white"> <img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=black">

<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white"> <img src="https://img.shields.io/badge/Notion-FFFFFF?style=for-the-badge&logo=Notion&logoColor=black">

## 💻 기능
+ 검색 및 주유소 목록 표시
    + 검색한 위치 기반 주유소 목록 표시
        + 카카오 맵 API를 통해 지도상 중앙 좌표(위도, 경도)를 얻어,<p>
            오피넷 API를 통해 2km내의 주유소 목록을 가져오기
    </p>
+ 회원가입, 로그인, 로그아웃
    </p>
+ 주유소 상세 정보
    + 선택한 주유소의 지도상 위치를 표시
        + 카카오 맵 API 사용
    + 선택한 주유소의 정보 출력
    </p>
+ 리뷰
    + 주유소별로 작성된 리뷰 목록 표시
    + 로그인한 경우, 리뷰 작성, 수정, 삭제 가능
        + 사용자가 작성한 리뷰에 대해서만 수정/삭제 가능
