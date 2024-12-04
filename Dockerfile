# 1. Python 이미지를 기반으로 설정
FROM python:3.10

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. 의존성 파일 복사
COPY requirements.txt /app/

# 4. 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 장고 프로젝트 파일 복사
COPY . /app/

# 6. 환경변수 설정 (예: 개발 환경)
ENV PYTHONUNBUFFERED 1

# 7. 장고 설정을 위한 포트 노출
EXPOSE 8000

# 8. collectstatic 실행 후 gunicorn 실행
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"
