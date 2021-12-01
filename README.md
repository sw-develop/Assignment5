# 원티드x위코드 백엔드 프리온보딩 프로젝트 #5

해당 프로젝트는 원티드X위코드 프리온보딩 백엔드 코스에서 수행한 **휴먼스케이프**의 기업 과제 입니다.

## Members
| 이름 | github                                     | 담당 기능                 |
|-----|--------------------------------------------|-------------------------|
|박세원 |[sw-develop](https://github.com/sw-develop) | 임상정보 검색 API 및 필터링 기능 구현, Unit Test 코드 작성|

## 구현 조건 내용

<details>
<summary><b>구현 조건 자세히 보기</b></summary>
<div markdown="1">
  
  
### **[필수 포함 사항]**

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### 확인 사항

- **ORM 사용 필수**
- **데이터베이스는 SQLite로 구현**
- **secret key, api key 등을 레포지토리에 올리지 않도록 유의**
    - README.md 에 관련 설명 명시 필요

### 도전 과제: 스스로에게도 도움이 되는 내용 + 추가 가산점

- 배포하여 웹에서 사용 할 수 있도록 제공
- 임상정보 검색 API 제공

### 과제 안내

다음 사항들을 충족하는 서비스를 구현해주세요.

- 임상정보를 수집하는 batch task
    - [참고](https://www.data.go.kr/data/3074271/fileData.do#/API%20%EB%AA%A9%EB%A1%9D/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887)
- 수집한 임상정보에 대한 API
    - 특정 임상정보 읽기(키 값은 자유)
- 수집한 임상정보 리스트 API
    - 최근 일주일내에 업데이트(변경사항이 있는) 된 임상정보 리스트
        - pagination 기능

- **Test 구현시 가산점이 있습니다.**

### 실행 예제

- Read
    
    ```bash
    curl localhost:3000/trials/{trial_id}
    => {
          "count": 30,
          "data" : [
             {
                "post" : "test...",
                "author" : "somebody",
                "created_at" : 212312312312312,
                ...
             }, 
             ...
          ]
       }
    
    ```
    
- List
    
    ```bash
    curl localhost:3000/list
    => {
          "count": 300,
          "data" : [
             {
                "post" : "test...",
                "author" : "somebody",
                "created_at" : 212312312312312,
                ...
             }, 
             ...
          ]
       }
    
    ```

  
</div>
</details>


## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/sqlite-0064a5?style=for-the-badge&logo=sqlite&logoColor=white"/>&nbsp;
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/SWAGGER-5B8C04?style=for-the-badge&logo=Swagger&logoColor=white"/>&nbsp;

## 모델링

![image](https://user-images.githubusercontent.com/80395324/142038266-71eca5cd-e933-49e1-bddc-59fdd642a778.png)

|이름(필드명)   |필드 타입                   |필터링 가능/필요 여부 |lookup_expression|
|-------|-------------------------|--------------------|--------------------|
|과제명(name) |Char    |O |icontains (입력된 값을 포함하는 경우)  |
|과제번호(number) |Char (unique)    |X (수집한 임상정보에 대한 API에서 처리) |X  |
|연구기간(period) |Char    |X (데이터가 통일성이 없음) |X  |
|연구범위(range) |Char    |O |icontains (입력된 값을 포함하는 경우)  |
|연구종류(code) |Char    |O |icontains (입력된 값을 포함하는 경우)  |
|연구책임기관(institute) |Char    |O |icontains (입력된 값을 포함하는 경우)  |
|임상시험단계(stage) |Char    |O |icontains (입력된 값을 포함하는 경우)  |
|전체목표연구대상자수(target_number) |Integer    |O |lte, gte (최소/최대 대상자 수)  |
|진료과(office) |Char    |O |icontains (입력된 값을 포함하는 경우)  |
|생성일(created_at) |Date    |X (우리 데이터베이스에 객체 생성된 시점 값이므로 필터링 필요없음) |X |
|업데이트일(updated_at) |Date    |X (수집한 임상정보 리스트 API에서 처리) |X |


## API
[링크-Swagger](http://ec2-3-35-166-14.ap-northeast-2.compute.amazonaws.com:8000/swagger/)

## 구현 기능
### 임상정보 검색 & 필터링 API
- 구현 방식
  - 각 필드별 구체적인 필터링 기능을 구현하기 위해 django-filter 라이브러리기반 FilterSet을 상속한 새로운 ResearchFilter 클래스를 구현하였습니다. 
- Search
  - rest_framework 라이브러리에서 제공하는 SearchFilter를 사용해 검색 기능을 구현하였습니다. 해당 기능에서 검색 대상이 되는 필드들은 CharField나 TextField 같은 text type이어야 하므로 name, number, range, code, institute, stage, office를 검색 대상 필드로 설정하였습니다. 
    
- Pagination & Ordering
  - 일정한 주기로 Open API를 호출하여 임상정보 데이터가 새롭게 생성되고, 업데이트 되어지는 점을 고려하여 실시간 데이터 처리로 데이터의 누락 및 중복을 방지할 수 있는 Cursor Pagination을 적용하였습니다.
  - 또한 데이터 조회 시 새롭게 업데이트된 순으로 정렬된 데이터들이 반환되도록 구현하였습니다.

- 테스트 코드 작성
  - 수집한 임상정보에 대한 API (특정 임상정보 읽기)**,** 수집한 임상정보 리스트 API (최근 일주일내에 업데이트된 임상정보 리스트), 임상정보 검색 API 각각에 대한 실패/성공 테스트 코드를 작성하였습니다.
  - 전체 Test Coverage 확인
  - [coverage](https://coverage.readthedocs.io/en/6.1.2/install.html) 라이브러리를 사용해 작성한 테스트 코드를 기반으로 Code Coverage를 측정 하였고, 97% 를 달성하였습니다. 
  ![image](https://user-images.githubusercontent.com/80395324/142041639-d01cbc59-214c-417b-bddd-0d51b36ea498.png)

## 배포정보
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 | http://ec2-3-35-166-14.ap-northeast-2.compute.amazonaws.com:8000/            |    |


## API TEST 방법
1. 우측 링크를 클릭해서 swagger로 들어갑니다. [링크](http://ec2-3-35-166-14.ap-northeast-2.compute.amazonaws.com:8000/swagger/)


## 설치 및 실행 방법

<details>
<summary><b>Local 개발 및 테스트용</b></summary>
<div markdown="1">
  
  
###  Local 개발 및 테스트용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment5
    cd Assignment5
    ```

2. 가상 환경을 만들고 프로젝트에 사용한 python package를 받는다.
    ```bash
    conda create --name Assignment5 python=3.8
    conda actvate Assignment5
    pip install -r requirements.txt
    ```

3. 환경 설정 파일 복사하고 해당 디렉토리로 이동해서 내용을 수정한다.
  ```bash
  cp -r env_template env
  cd env
  ```
  - .env.dev_local.json
  ```json
  {
    "DJANGO_SECRET_KEY" : "SECRET_KEY",
    "OPEN_API_KEY" : "임상정보 open API Key (후술)"
  }
  ```

4. db를 table 구조를 최신 model에 맞게 설정한다.
    ```bash
    python manage.py migrate
    ```

5. 서버를 실행한다.
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```


</div>
</details>

  
<details>
<summary><b>배포용</b></summary>
<div markdown="1">
  
  
###  배포용 
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
  ```bash
  git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment5
  cd Assignment5
  ```

2. 환경 설정 파일 복사하고 해당 디렉토리로 이동해서 내용을 수정한다.
  ```bash
  cp -r env_template env
  cd env
  ```
  - .env.deploy.json
  ```json
  {
    "DJANGO_SECRET_KEY" : "SECRET_KEY",
    "OPEN_API_KEY" : "임상정보 open API Key (후술)"
  }
  ```

  - .env.admin_info.json (서버 에러발생시 email를 받을 관리자 정보)
  ```json
  [
    {
      "name" : "관리자 이름1",
      "email" : "관리자 이메일1"
    },
    {
      "name" : "관리자 이름2",
      "email" : "관리자 이메일2"
    }
    (추가 가능)
  ]
  ```
       
3. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-deploy.yml up
    ```
    
4. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
 
    ```bash
    docker-compose -f docker-compose-deploy.yml up -d
    ```

</div>
</details>


<details>
<summary><b>참고 임상정보 open API Key</b></summary>
<div markdown="1">
  
  
### 참고 임상정보 open API Key
1. [임상정보 open API](https://www.data.go.kr/data/3074271/fileData.do#/API%20%EB%AA%A9%EB%A1%9D/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887) 에서 활용 신청을 클릭해서 신청을 진행합니다.
![스크린샷 2021-11-17 오전 4 01 09](https://user-images.githubusercontent.com/8219812/142048791-3f609654-51aa-4606-8eaa-ac1e51476bd4.png)


2. 신청을 진행하시면 자동으로 신청이 완료되며, 마이페이지로 가시면 신청하신 API List가 있는데, `질병관리청_임상연구 과제정보`를 클릭합니다.
![image](https://user-images.githubusercontent.com/8219812/142049022-769ae22c-9816-425b-8bb8-ded717984014.png)

3. 아래와 같은 정보들이 나오는데, 필요한 값은 `일반 인증키 (decoding)` 입니다. 이 값을 설정 파일에 OPEN_API_KEY에 적용하시면 됩니다.
![스크린샷 2021-11-17 오전 3 59 36](https://user-images.githubusercontent.com/8219812/142049135-1073fb23-b254-48a4-a3ab-74a1e075a9dc.png)

  
</div>
</details>


## 폴더 구조
```bash
📦 Assignment5
 ┣ 📂 commands
 ┃ ┣ 📂 management
 ┃ ┃ ┣ 📂 commands
 ┃ ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┃ ┗ 📜 import_csv_to_db.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📂 migrations
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📜 __init__.py
 ┃ ┗ 📜 apps.py
 ┣ 📂 config
 ┃ ┗ 📂 nginx
 ┃ ┃ ┗ 📜 nginx.conf
 ┣ 📂 env_template
 ┃ ┣ 📜 .env.admin_info.json
 ┃ ┣ 📜 .env.deploy.json
 ┃ ┗ 📜 .env.dev_local.json
 ┣ 📂 humanscape
 ┃ ┣ 📂 settings
 ┃ ┃ ┣ 📜 base.py
 ┃ ┃ ┣ 📜 deploy.py
 ┃ ┃ ┗ 📜 dev_local.py
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 asgi.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 wsgi.py
 ┣ 📂 research
 ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 0001_initial.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📂 tests
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┣ 📜 tests_detail.py
 ┃ ┃ ┣ 📜 tests_recent.py
 ┃ ┃ ┗ 📜 tests_search_.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜 admin.py
 ┃ ┣ 📜 apps.py
 ┃ ┣ 📜 batch.py
 ┃ ┣ 📜 crontab.py
 ┃ ┣ 📜 filters.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 serializers.py
 ┃ ┣ 📜 urls.py
 ┃ ┣ 📜 utils.py
 ┃ ┗ 📜 views.py
 ┣ 📜 .gitignore
 ┣ 📜 Dockerfile-deploy
 ┣ 📜 README.md
 ┣ 📜 db_data.csv
 ┣ 📜 docker-compose-deploy.yml
 ┣ 📜 execptions.py
 ┣ 📜 graph.png
 ┣ 📜 manage.py
 ┣ 📜 pull_request_template.md
 ┣ 📜 requirements.txt
 ┗ 📜 utils.py

```


## TIL정리 (Blog)
- 김태우 : https://velog.io/@burnkim61/프리온보딩-과제-5
- 고유영 :
- 박지원 : 
- 최신혁 :
- 박세원 :

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 휴먼스케이프에서 출제한 과제를 기반으로 만들었습니다.
