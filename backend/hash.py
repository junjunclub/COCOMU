import os
import django
from django.contrib.auth.hashers import make_password

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'COCOMU_API.settings')
django.setup()

# 비밀번호 해시 생성
password = 'ssafy135!'
hashed_password = make_password(password)
print(hashed_password)