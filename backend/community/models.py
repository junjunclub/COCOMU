from django.db import models
from accounts.models import User
from movies.models import Movie

# Create your models here.
class Article(models.Model):
    # 외래키
    # 게시글을 작성한 유저, 영화후기 작성 시 영화 선택가능
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    # ---
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    category = models.TextField()
    # 평점은 영화 리뷰가 아니면 의미가 없어서 null값을 True로
    rate = models.FloatField(blank=True, null=True)
    
class Comment(models.Model):
    # 외래키
    # 댓글의 주인인 게시글, 댓글을 단 유저
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ---
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    