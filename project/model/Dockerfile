FROM python:3.9-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    vim \
    locales \
    wget \
    curl \
    python3-openssl \
    git && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen ko_KR.utf8 && dpkg-reconfigure locales

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 패키지 설치
COPY model/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Hugging Face CLI 설치 (필요한 경우)
# RUN pip install --upgrade huggingface-hub

# 애플리케이션 코드 복사
COPY model/ /app

# 서비스 계정 키 파일 복사 (필요한 경우)
COPY credentials.json /app/credentials.json

# 환경 변수 설정
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# 애플리케이션 실행
CMD ["python", "llm_server.py"]
