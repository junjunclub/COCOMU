from rest_framework import serializers
from .models import Movie, Genre


# 전체 게시글 serializer
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # 영화 리스트에서 표시될 내용
        # 제목, 출시일, 포스터, 평점, 볼 수있는 OTT
        # 내부적으로 장르, tmdbid 필요해서 추가로 적습니다
        fields = (
            "title",
            "release_date",
            "poster_path",
            "vote_average",
            "provide_info",
            "genres",
            "movie_id",
            "backdrop_path",
        )


# 상세 영화정보
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # 전체 직렬화
        fields = "__all__"
