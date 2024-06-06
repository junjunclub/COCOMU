"""

"""

from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_index, name='movie_index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/recommend/', views.movie_detail_recommend, name='movie_detail_recommend'),
    path('<int:movie_id>/likes/', views.movie_likes, name='movie_likes'),
    path('search/<str:keyword>/', views.movie_search, name='movie_search'),
    path('searchpk/<int:pk>/', views.search_by_pk, name='search_by_pk'),
]