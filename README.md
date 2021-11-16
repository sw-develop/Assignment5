# Assignment5

원티드x위코드 백엔드 프리온보딩 과제4
- 과제 출제 기업 정보
  - 기업명 : 휴먼스케이프
    - [휴먼스케이프 사이트](https://humanscape.io/kr/index.html)
    - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/41413)

## Members
| 이름 | github                                     | 담당 기능                 |
|-----|--------------------------------------------|-------------------------|
|김태우 |[jotasic](https://github.com/jotasic)       | batch 자동화 기능 구현      |
|고유영 |[lunayyko](https://github.com/lunayyko)     | 상세 임상정보 조회 API, 스웨거|
|박지원 |[jiwon5304](https://github.com/jiwon5304)   | 최근 임상정보 조회 API, 배포 |
|최신혁 |[shchoi94](https://github.com/shchoi94)     | batch task 로직 구현      |
|박세원 |[sw-develop](https://github.com/sw-develop) | 검색 임상정보 조회 API      |

## 과제 내용
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
### 1. batch task   
  - 과제 번호를 identifier로 가정히여   
  open api의 리스폰스 기반으로 데이터베이스에 데이터 추가, 수정, 삭제 기능을 구현하였습니다.
     
  - 'eq', 'hash' 매직메소드를 직접 구현하지 않고 set이 사용가능한   
    dataclass, 값 객체를 정의하였습니다.
    ```
    @dataclass(frozen=True)
    class DataResearch:
        name: str
        number: str
        period: str
        ...
    ```
  - db 데이터와 open api 데이터를 각각 dataclass, 값 객체로 매핑 후, 데이터를 비교하여   
    데이터를 데이터베이스에 추가, 수정, 삭제되도록 하였습니다.

### 2. batch 자동화 기능 (django-crontab)
#### 기능 구현 방식
 - django-crontab을 이용해서 하루 단위로 batch task를 실행 할 수 있도록 하였습니다.
 ```python
 CRONJOBS = [
        ('* 0 * * *', 'research.crontab.start_batch', ),
]
 ```
  
  
 #### batch 기능에 대한 이력 작업
   - 백그라운드에서 구동되는 작업이기 때문에, 관리자가 batch task가 정상 동작했는지, 실패했는지 알 수 있는 방법이 없다고 생각하였고, 알 수 있기 위해서 Log를 남겨야겠다고 생각했습니다.
    
   ```text
    [17/Nov/2021 01:22:01] INFO [utils.py:12] [start_batch] trying [1/5]
    [17/Nov/2021 01:22:01] INFO [batch.py:98] [batch_task] Start get_data_from_open_api
    [17/Nov/2021 01:22:01] INFO [batch.py:101] [batch_task] Start get_data_from_db
    [17/Nov/2021 01:22:01] INFO [batch.py:104] [batch_task] Check items for Create, Udate, Delete]
    [17/Nov/2021 01:22:01] INFO [batch.py:108] [batch_task] Create new itmes to db [total: 145]
    [17/Nov/2021 01:22:01] INFO [batch.py:111] [batch_task] Update new itmes to db [total: 0]
    [17/Nov/2021 01:22:01] INFO [batch.py:116] [batch_task] Delete new itmes to db [total: 0]
    [17/Nov/2021 01:22:01] INFO [crontab.py:21] [start_batch] Success batch job [took:0.24s]
    
    [17/Nov/2021 01:23:01] INFO [utils.py:12] [start_batch] trying [1/5]
    [17/Nov/2021 01:23:01] INFO [batch.py:98] [batch_task] Start get_data_from_open_api
    [17/Nov/2021 01:23:01] INFO [batch.py:101] [batch_task] Start get_data_from_db
    [17/Nov/2021 01:23:01] INFO [batch.py:104] [batch_task] Check items for Create, Udate, Delete]
    [17/Nov/2021 01:23:01] INFO [batch.py:108] [batch_task] Create new itmes to db [total: 1]
    [17/Nov/2021 01:23:01] INFO [batch.py:111] [batch_task] Update new itmes to db [total: 0]
    [17/Nov/2021 01:23:01] INFO [batch.py:116] [batch_task] Delete new itmes to db [total: 0]
    [17/Nov/2021 01:23:01] INFO [crontab.py:21] [start_batch] Success batch job [took:0.13s]
   ```
   
   - 만약 LOG LEVEL이 ERROR일 경우 관리자에게 이메일을 보내도록 설정하였습니다.(deploy 환경일 경우만 동작합니다)
   - 설정 방법은 `설치 및 실행 방법 - 배포용`을 참고해 주시기 바랍니다. 
   ![image](https://user-images.githubusercontent.com/8219812/142047477-984d31aa-be61-4fd7-a51e-0e08b4b1a1d1.png)



### 3. 특정 임상정보 조회 API
- 연구 데이터를 상세 조회합니다.
- 연구번호 값을 기준으로 해당 데이터를 조회합니다.


### 4. 최근 업데이트 임상정보 조회 API
- 최근 일주일의 연구데이터를 조회합니다. 조회일을 기준으로 7일 전의 데이터까지 총 8일(조회일 포함)의 데이터를 보여줍니다.
- 최근 리스트를 조회하기 위해 "updated_at" 필드에 range[-7:0] 필터링을 적용하여 RecentListView 클래스를 구현하였습니다.

   ```bash
    ResearchInformation.objects.filter(updated_at__range = [date.today() - timedelta(days = 7), date.today()])
    ```
- Pagination
  - Cursor Pagination을 적용하였고, 기본 100개의 정보를 조회하도록 구현하였습니다.
- Ordering
  - 최근 업데이트 된 날짜를 우선으로 정렬하여 데이터가 반환되도록 구현하였습니다.
- Pagination & Ordering 은 검색 API 와 동일하게 적용합니다.
- ex) 2021.11.17일 데이터 조회 -> 2021.11.17 ~ 10일까지의 데이터 중 최근 날짜를 우선으로 반환하게 됩니다.



### 5. 임상정보 검색 API
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
---
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 | http://ec2-3-35-166-14.ap-northeast-2.compute.amazonaws.com:8000/            |    |


## API TEST 방법
1. 우측 링크를 클릭해서 swagger로 들어갑니다. [링크](http://ec2-3-35-166-14.ap-northeast-2.compute.amazonaws.com:8000/swagger/)


## 설치 및 실행 방법
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

### 참고 임상정보 open API Key
1. [임상정보 open API](https://www.data.go.kr/data/3074271/fileData.do#/API%20%EB%AA%A9%EB%A1%9D/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887) 에서 활용 신청을 클릭해서 신청을 진행합니다.
![스크린샷 2021-11-17 오전 4 01 09](https://user-images.githubusercontent.com/8219812/142048791-3f609654-51aa-4606-8eaa-ac1e51476bd4.png)


2. 신청을 진행하시면 자동으로 신청이 완료되며, 마이페이지로 가시면 신청하신 API List가 있는데, `질병관리청_임상연구 과제정보`를 클릭합니다.
![image](https://user-images.githubusercontent.com/8219812/142049022-769ae22c-9816-425b-8bb8-ded717984014.png)

3. 아래와 같은 정보들이 나오는데, 필요한 값은 `일반 인증키 (decoding)` 입니다. 이 값을 설정 파일에 OPEN_API_KEY에 적용하시면 됩니다.
![스크린샷 2021-11-17 오전 3 59 36](https://user-images.githubusercontent.com/8219812/142049135-1073fb23-b254-48a4-a3ab-74a1e075a9dc.png)
 

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
