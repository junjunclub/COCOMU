from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from movies.models import Movie
from .serializers import UserSerializer, SurveySerializer
from movies.serializers import MovieSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def book_mark(request):
    user = request.user
    try:
        favorite_movies = Movie.objects.filter(like_user=user)
        if not favorite_movies:
            raise Movie.DoesNotExist
        serializer = MovieSerializer(favorite_movies, many=True)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({"detail": "찜한 영화 리스트가 없습니다."}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def survey(request):
    # request data 받아와서 user DB에 저장 (수정)
    try:
        user_profile = User.objects.get(username=request.user)
        user_profile.genre1 = None
        user_profile.genre2 = None
        user_profile.genre3 = None
        user_profile.save()
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SurveySerializer(user_profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Survey data saved successfully."}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def profile_update(request):
    user = request.user  # 현재 로그인된 사용자 가져오기
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print("수정완료!!!")
        return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def profile_delete(request):
    user = request.user  # 현재 로그인된 사용자 가져오기
    user.delete()
    print("삭제완료!!!")
    return Response({"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)