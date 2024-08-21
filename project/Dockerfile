# 베이스 이미지 설정
FROM python:3.9-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    openssh-client \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev

# 작업 디렉토리 설정
WORKDIR /app

RUN pip install --upgrade pip 
# 종속성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# 애플리케이션 소스 코드 복사
COPY . /app/

# 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=backend.myproject.settings

# PYTHONPATH에 backend 디렉토리를 추가합니다.
ENV PYTHONPATH=/app

# 포트 설정
EXPOSE 8000

# 서버 실행 명령
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
