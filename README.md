# Django Record Plate

장고 프로젝트 재사용을 위한 보일러 플레이트

로그인 기록 작성 및 일별기록 확인가능한 RESTAPI 제공

## 실행방법

```Bash
# dev
docker-compose up -d

# db test
docker-compose -f docker-compose.db.yaml up --build

# product
docker-compose -f docker-compose.prod.yaml up --build

# logs
docker-compose logs

# down
docker-compose down

# docker bash 접속
docker exec -it 'name' bash
```

## 시스템 구성

- Backend : Django (Django Rest Framework)  + Nginx + Gunicorn + Docker
- DB : PostgreSQL
- Infra : Docker

## 사용 기술

- Django Rest Framework
- Django + Nginx + Gunicorn + Docker
- dj-rest-auth : REST API를 통한 로그인/로그아웃 제공

## 데이터베이스 설계

[record ERD](https://www.erdcloud.com/d/RACtxBeL3C63ePSM8)

## API 설계

| INDEX | METHOD | URL                   | DESCRIPTION             |
| ----- | ------ | --------------------- | ----------------------- |
| 1     | GET    | /login                | 로그인 기록 리스트 조회 |
| 2     | POST   | /login                | 로그인 기록 작성        |
| 3     | GET    | /login/{id}           | ID별 로그인 기록 조회   |
| 4     | PUT    | /login/{id}           | ID별 로그인 기록 수정   |
| 5     | DELETE | /login/{id}           | ID별 로그인 기록 삭제   |
| 6     | GET    | /login/user/{user_id} | 유저별 로그인 기록 조회 |
| 7     | GET    | /daily                | 일별기록 리스트 조회    |
| 8     | POST   | /daily                | 일별기록 작성           |
| 9     | GET    | /daily/{id}           | ID별 일별기록 조회      |
| 10    | PUT    | /daily/{id}           | ID별 일별기록 수정      |
| 11    | DELETE | /daily/{id}           | ID별 일별기록 삭제      |
| 12    | GET    | /daily/user/{user_id} | 유저별 일별기록 조회    |

## 주요 업데이트

### 1. Nginx + Gunicorn + Django + Docker

- Nginx + Gunicorn + Django + Docker 환경 구성

- 참고 사이트
  1. [[실전] Docker + Nginx + gunicorn + django](https://velog.io/@masterkorea01/Docker-Nginx-gunicorn-django)
  2. [웹서비스의 구성 - Web Server , CGI, WAS , WSGI의 특징 및 차이점](https://my-repo.tistory.com/20?category=918048)

### 2. Swagger 적용

- Django REST Swagger(drf_yasg module)을 적용하여 API 문서 생성
- Swagger 에서 POST 실행 시 csrf token 에러가 발생하는데 Responses Curl 부분과 쿠키를 맞춰주면 해결된다.

### 3. Test Code 적용

### - 테스트 종류

1. unit test(유닛테스트)
   - 독립적인 class와 function 단위의 테스트
2. Regression test(버그 수정 테스트)
   - 발생하였던 버그에 대한 수정 테스트
3. Integration test(통합테스트)
   - 유닛 테스크를 완료한 각각의 독립적인 컴포넌트들이 함께 결합하여 수행하는 동작을 검증.
   - 각 컴포넌트들의 내부적인 동작까지는 검증할 필요가 없다. 해석해보면 비즈니스 로직에 대한 검증인거 같다

### - 테스트 함수

```python
self.assertEquals # 생각한 값과 같은지 체크해주는 함수
self.assertTrue(True) # () 안의 값이 True인지 체크
self.assertFalse(False) # () 안의 값이 False인지 체크
```

### - Test Setting

Test용 DB가 따로 생성되기 때문에 superuser 등 기본 세팅을 해줘야한다.

- 참고 사이트 : https://docs.djangoproject.com/en/4.1/topics/testing/overview/

### - Django Rest Framework의 Testing

APIRequestFactory를 통해 CRUD 테스트를 짧은 코드로도 만들 수 있다.

- 참고 사이트 : https://www.django-rest-framework.org/api-guide/testing/

### 4. 유효성 검사 (validators)

- LoginAccess 모델의 tag는 IN, OUT만 가능하도록 제한이 필요하다고 느꼈음
- 모델에 validators 인수를 추가하면 가능하다. 처음엔 안되서 찾아보니 Django Rest Framework에서는 serializers.py에 추가해야한다는 설명이 있는데 모델에 추가해야 동작했다.
- 참고 사이트 : https://docs.djangoproject.com/en/4.1/ref/validators/

### 5. MultipleValueDictKeyError 수정

```python
data["check_time"] # 데이터가 존재하지 않을 경우 MultipleValueDictKeyError
data.get("check_time", False) # 데이터가 없으면 False로 처리
```

### 6. validator 대신 Enum으로 변경

출입 Tag 값을 IN, OUT로 선택할 수 있도록 바꿨다. 이를 통해 잘못된 값이 들어오는 것을 방지하고 사용자가 어떤 값을 입력해야 할지 명확해졌다.

```python
# 변경 전
tag = models.CharField(max_length=10, default="IN", validators=[validate_tag])

# 변경 후
class TagChoices(Enum):
    IN = 'IN'
    OUT = 'OUT'

tag = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in TagChoices], default=TagChoices.IN.value)
```

### 7. LoginAccess 기록 알고리즘 수정

기존 알고리즘의 경우 불필요한 if가 남발되어 수정하였다.

```python
class LoginAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in TagChoices], default=TagChoices.IN.value)
    check_time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # 태그가 OUT일 경우 처리
        if self.tag == TagChoices.OUT.value:
            last_login_in = LoginAccess.objects.filter(user=self.user, tag=TagChoices.IN.value).order_by('-check_time').first()
            # 오늘 출근한 적이 있으면 출석기록을 가져와서 leave_time, working_time 계산 후 저장한다.
            if last_login_in:
                last_daily_record = DailyRecord.objects.filter(user=self.user, date=last_login_in.check_time.date()).first()
                if last_daily_record:
                    last_daily_record.leave_time = self.check_time
                    last_daily_record.save()
                    last_daily_record.working_time = (last_daily_record.leave_time - last_daily_record.go_time).seconds // 3600
                    last_daily_record.save()
                else:
                    # Handle case if no previous DailyRecord is found
                    pass
            else:
                # Handle case if no previous LoginAccess with tag IN is found
                pass
        super(LoginAccess, self).save(*args, **kwargs)
```

### 8. wait-for-it.sh 사용 유의사항

- OS가 windows인지 unix 인지에 따라 오류가 발생함.
- docker container는 unix 기반이기 때문에 windows에서 코드를 복붙 후 실행하면 CRLF(\r\n), CR(\r), LF(\n) 문제가 발생할 수 있으니 주의

### 9. static file 인식 문제 해결

product 버전으로 실행 시 static file을 인식하지 못하는 문제가 있었다.
다음과 같이 url에 static 파일 경로를 설정해줘야 인식했다.

```python
urlpatterns = [
    ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 10. DB healthcheck

wait-for-it.sh 사용에 불편함이 있어 docker에서 healthcheck 방법이 있나 해서 찾아보았다. DB 셋업 중에 django 실행 시 db연결 에러가 나서 디버깅에 어려움이 있었는데 실패 시 재시도 하는 방법으로 해결하였다.

```docker
  backend:
    # ... 생략
    depends_on:
      db:
        condition: service_healthy # DB의 healthcheck 참고하여 에러 여부확인
    restart: on-failure # 실패 시 재시도 (db 연결 속도 문제)
  db:
    # ... 생략
    healthcheck: # 상태 확인, 에러시 5초 후 다시 확인, 5번 실패 시 종료
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
      timeout: 5s
```