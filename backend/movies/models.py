from django.db import models
from django.conf import settings
from accounts.models import User

# Create your models here.

    
    
# # OTT 모델
# class Ott(models.Model):
#     # 외래키
#     # 유저가 이용하는 ott
#     user = models.ManyToManyField(User, related_name='ott')
#     # OTT_id, 가격, 타입(구독, 대여, 구매), OTT이름, 로고img
#     provider_id = models.IntegerField()
#     price = models.IntegerField()
#     provider_info = models.JSONField()
#     provider_name = models.CharField(max_length=100)
#     logo_path = models.TextField()

class Ott(models.Model):
    provider_name = models.CharField(max_length=30)
    provider_id = models.IntegerField()
    logo_path = models.URLField()

    
class Movie(models.Model):
    # 외래키
    # user, Ott의 id
    # OTT 주석처리
    # service_ott = models.ManyToManyField(Ott, related_name='service_movie')
    like_user = models.ManyToManyField(User, related_name='like_movie')
    # ---
    title = models.TextField()
    release_date = models.DateField()
    poster_path = models.URLField(null=True)
    is_adult = models.BooleanField()
    # 수정한 목록
    movie_id = models.IntegerField(unique=True)
    overview = models.TextField()
    origin_country = models.JSONField(null=True)
    runtime = models.IntegerField()
    director = models.JSONField(null=True)
    vote_average = models.FloatField()
    provide_info = models.JSONField()
    # 추가해야할 필드
    genres = models.JSONField()
    # 백드랍필드 : 글자가 없는 포스터(없는 경우도 있음) > 다양한 사진을 제공하기 위해 추가함
    backdrop_path = models.URLField(null=True)
    # 오류가 생기면 이거때문일수도.... 문제 없음!
    actor = models.JSONField()
    related_movies = models.JSONField(null=True,blank=True)
    

class Genre(models.Model):
    genre_ids = models.JSONField()
    name = models.TextField()