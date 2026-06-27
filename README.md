# pushFCM

Django + Arduino IoT 기반 센서 데이터 모니터링 및 Firebase Cloud Messaging(FCM) 푸시 알림 시스템.

## 구성

- **sensorFCM/datasender/datasender.ino**: Arduino 센서 → 서버로 데이터 전송 펌웨어
- **sensorFCM/**: Django 서버 - 센서 데이터 수신·저장, 임계값 초과 시 FCM 푸시 발송

## 기능

- 유량(flow) 센서 데이터 수신 및 SQLite 저장
- 설정 임계값(`limit`) 초과 시 FCM 푸시 알림 자동 발송
- 실시간 그래프 대시보드

## 실행

```bash
cd sensorFCM
python manage.py runserver
```

`.env` 또는 `views.py`의 `key`(FCM Server Key), `pkey`(모바일 기기 키) 설정 필요.