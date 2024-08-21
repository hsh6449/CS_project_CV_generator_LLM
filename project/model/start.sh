#!/bin/bash

# 인터넷 연결 테스트
echo "Set GCP ENV.."
export GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json


echo "Starting the LLM server..."
python3 /app/llm_server.py

# 무한 대기 루프를 추가하여 컨테이너가 종료되지 않도록 합니다.
tail -f /dev/null
