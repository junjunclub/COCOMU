from django.core.cache import cache
import requests
from rest_framework.response import Response
from django.conf import settings
from .models import Movie, Ott

API_KEY = settings.TMDB_API_KEY

def insert_movie_info(movie_data,movie_id,details_params):
    credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    credits_response = requests.get(credits_url, params=details_params).json()
    
    director = next(
        (
            {'name': crew['name'], 'profile_path': crew['profile_path']}
            for crew in credits_response.get('crew', [])
            if crew['job'] == 'Director'
        ),
        None
    )
    
    actors = [
        {
            'name': cast['name'],
            'character': cast['character'],
            'profile_path': cast['profile_path']
        }
        for cast in credits_response.get('cast', [])[:5]
    ]  # Get top 5 actors
    
    movie_data['director'] = director
    movie_data['actor'] = actors
    
    # Get provider information
    providers_url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers'
    providers_params = {
        'api_key': API_KEY,
        'language': 'ko-KR'
    }
    providers_response = requests.get(providers_url, params=providers_params).json()
    providers_kr = providers_response.get('results', {}).get('KR', {})
    
    for provider_type in ['flatrate', 'rent', 'buy']:
        if provider_type in providers_kr:
            movie_data['provide_info'][provider_type] = [
                provider['provider_id'] for provider in providers_kr[provider_type]
            ]
    return movie_data


def fetch_movie_from_api(movie_id):
    details_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    details_params = {
        'api_key': API_KEY,
        'language': 'ko-KR'
    }
    print('탐색 시작')
    details_response = requests.get(details_url, params=details_params)
    
    if details_response.status_code != 200:
        return None  # 외부 API 요청이 실패하면 None 반환

    details_data = details_response.json()
    print(details_data)
    if 'title' not in details_data:
        return None
    
    movie_data = {
        'title': details_data.get('title'),
        'release_date': details_data.get('release_date'),
        'poster_path': details_data.get('poster_path'),
        'backdrop_path': details_data.get('backdrop_path'),
        'is_adult': details_data.get('adult'),
        'movie_id': movie_id,
        'overview': details_data.get('overview'),
        'origin_country': details_data.get('production_countries')[0]['iso_3166_1'] if details_data.get('production_countries') else None,
        'runtime': details_data.get('runtime'),
        'vote_average': details_data.get('vote_average'),
        'genres': details_data.get('genres'),
        'director': None,  # Placeholder for director information
        'actor': None,     # Placeholder for actor information
        'provide_info': {
            'flatrate': [],
            'rent': [],
            'buy': []
        }
    }
    insert_movie_info(movie_data,movie_id,details_params)

    return movie_data

def fetch_similar_movie_from_api(movie_title):
    API_KEY = settings.TMDB_API_KEY
    details_url = 'https://api.themoviedb.org/3/search/movie'
    details_params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
        'query': movie_title,
        'include_adult': False,
    }
    
    details_response = requests.get(details_url, params=details_params)
    
    if details_response.status_code != 200:
        return None  # 외부 API 요청이 실패하면 None 반환

    details_data = details_response.json()
    
    if not details_data.get('results'):
        return None  # 결과가 없으면 None 반환
    
    movie_details = details_data['results'][0]  # 첫 번째 검색 결과 사용
    print("첫번째 검색 결과는?")
    print(movie_details)
    movie_data = {
        'title': movie_details.get('title'),
        'release_date': movie_details.get('release_date'),
        'poster_path': movie_details.get('poster_path'),
        'backdrop_path': movie_details.get('backdrop_path'),
        'is_adult': movie_details.get('adult'),
        'movie_id': movie_details.get('id'),
        'overview': movie_details.get('overview'),
        'origin_country': movie_details.get('origin_country'),
        'runtime': movie_details.get('runtime'),
        'vote_average': movie_details.get('vote_average'),
        'genres': movie_details.get('genre_ids'),  # 장르 ID를 가져옴
        'director': None,  # Placeholder for director information
        'actor': None,     # Placeholder for actor information
        'provide_info': {
            'flatrate': [],
            'rent': [],
            'buy': []
        }
    }
    movie_id = movie_data['movie_id']
    insert_movie_info(movie_data,movie_id,details_params)

    return movie_data