from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Movie
from .serializers import MovieSerializer, MovieListSerializer
from .utils import fetch_movie_from_api,fetch_similar_movie_from_api
from openai import OpenAI
import requests

API_KEY = settings.TMDB_API_KEY

# Create your views here.
# 영화 전체 조회 (캐싱하면 좋을듯)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def movie_index(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_movie_data(movie_id):
    print('검색을 시작합니다.')
    cache_key = f"movie_data_{movie_id}"
    movie_data = cache.get(cache_key)
    print('캐시에 있는지 확인합니다.')
    if movie_data is None:
        try:
            movie = Movie.objects.get(movie_id=movie_id)
        except Movie.DoesNotExist:
            movie_data = fetch_movie_from_api(movie_id)
            if not movie_data:
                return None
            movie = Movie.objects.create(**movie_data)
        serializer = MovieSerializer(movie)
        movie_data = serializer.data
        cache.set(cache_key, movie_data, timeout=60*60)  # Cache for 1 hour
        print('캐시에 넣었습니다.')
        print(movie_data)
    return movie_data

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    movie_data = get_movie_data(movie_id)
    # print(movie_data)
    if not movie_data:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(movie_data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def movie_detail_recommend(request, movie_id):
    movie_data = get_movie_data(movie_id)
    if not movie_data:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    
    title = movie_data['title']
    genres = [genre['name'] for genre in movie_data['genres']]
    genre_str = ', '.join(genres)
    
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = (
        f"release_date가 2010년 이후이고, 장르가 {genre_str}이고, 영화 {title} 유사한 영화 3개의 영어제목을 python list형식으로 만들어줘 만약 영어제목에 single quote가 포함돼있다면 그 앞에 python escape 문자를 넣어서 만들어줘"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    similar_movies_titles = eval(response.choices[0].message.content)
    print('================')
    print(similar_movies_titles)
    related_movies = []
    for movie_title in similar_movies_titles:
        similar_movie_data = fetch_similar_movie_from_api(movie_title)
        if similar_movie_data:
            related_movies.append({
                'movie_id': similar_movie_data['movie_id'],
                'title': similar_movie_data['title'],
                'poster_path': similar_movie_data.get('poster_path')
            })
    
    movie_data['related_movies'] = related_movies
    print('==============')
    print(movie_data)
    return Response(movie_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    user = request.user
    if user in movie.like_user.all():
        movie.like_user.remove(user)
        return Response({"detail": "영화 좋아요 취소됨."})
    else:
        movie.like_user.add(user)
        return Response({"detail": "영화 좋아요 추가됨."})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def movie_search(request, keyword):
    # DB에서 영화 검색
    movies = Movie.objects.filter(title__icontains=keyword)
    if movies.exists():
        # 검색된 영화가 있을 경우
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # 검색된 영화가 없을 경우 외부 API 호출
    API_URL = f'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
        'query': keyword,
        'include_adult': False,
    }
    response = requests.get(API_URL, params=params)
    search_result = response.json().get('results',[])
    for result in search_result:
        result['movie_id'] = result['id']
    print(response.json().get('results'))
    print('=========')
    if response.status_code == 200:
        return Response(search_result)
    else:
        return Response({"error": "Failed to fetch data from external API"}, status=response.status_code)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_by_pk(request, pk):
    print('============')
    movie = Movie.objects.get(pk=pk)
    serializer = MovieSerializer(movie)
    print(serializer.data)
    print('============')
    return Response(serializer.data, status=status.HTTP_200_OK)