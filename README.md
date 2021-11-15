# Assignment5

원티드x위코드 백엔드 프리온보딩 과제4
- 과제 출제 기업 정보
  - 기업명 : 휴먼스케이프
    - [휴먼스케이프 사이트](https://humanscape.io/kr/index.html)
    - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/41413)

## Members
|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|고유영 |[lunayyko](https://github.com/lunayyko)     | |
|박지원 |[jiwon5304](https://github.com/jiwon5304)   | |
|최신혁 |[shchoi94](https://github.com/shchoi94)     | |
|박세원 |[sw-develop](https://github.com/sw-develop) | |

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
    - 참고: [https://www.data.go.kr/data/3074271/fileData.do#/API 목록/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887](https:/www.data.go.kr/data/3074271/fileData.do#/API%20%EB%AA%A9%EB%A1%9D/GETuddi%3Acfc19dda-6f75-4c57-86a8-bb9c8b103887)
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


## API
[링크-Swagger](http://18.188.189.173:8041/swagger/)

## 구현 기능


## 배포정보
---
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 | http://18.188.189.173:8041/            |    |


## API TEST 방법
1. 우측 링크를 클릭해서 swagger로 들어갑니다. [링크](http://18.188.189.173:8041/swagger/)


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

3. Django SECRET_KEY 용및 공공데이터 API_KEY를 환경 변수를 등록한다.
   ```bash
      export DJANGO_SECRET_KEY='django시크릿키'
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

2. docker환경 설정 파일을 만든다.

  
3. 백엔드 서버용 .dockerenv.deploy.backend 파일을 만들어서 안에 다음과 같은 내용을 입력한다. manage.py와 같은 폴더에 생성한다.
    ### .dockerenv.deploy.backend
    ```text
      DJANGO_SECRET_KEY='django시크릿키'
    ```
       
4. docker-compose를 통해서 db와 서버를 실행시킨다.
    
    ```bash
    docker-compose -f docker-compose-deploy.yml up
    ```
    
5. 만약 백그라운드에서 실행하고 싶을 시 `-d` 옵션을 추가한다.
  
    ```bash
    docker-compose -f docker-compose-deploy.yml up -d
    ```

## 폴더 구조
```bash

```


## TIL정리 (Blog)
- 김태우 : 
- 고유영 :
- 박지원 : 
- 최신혁 :
- 박세원 :

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 휴먼스케이프에서 출제한 과제를 기반으로 만들었습니다.
