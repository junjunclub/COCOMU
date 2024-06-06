from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer, SearchSerializer


# 게시글 전체 조회 (캐싱하면 좋을듯)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index(request):
    articles = Article.objects.all()
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 게시글 작성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def article_create(request):
    print("Request Data:", request.data)
    print("User:", request.user)
    serializer = ArticleSerializer(data=request.data)
    # movie는 영화의 pk값으로 들어옴
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 상세 조회
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    serializer = ArticleSerializer(article)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 게시글 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user == article.user:
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)


# 게시글 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user == article.user:
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


# 댓글 작성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_create(request, article_id):
    # user의 pk가 들어가야함
    article = get_object_or_404(Article, pk=article_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        comment = serializer.save(user=request.user, article=article)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def comment_update(request, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    print(comment)
    if request.user == comment.user:
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


# 댓글 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def comment_delete(request, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search(request, keyword):
    # 제목에 keyword가 포함된 게시글을 검색
    articles = Article.objects.filter(title__icontains=keyword)
    # 검색된 결과를 시리얼라이즈
    serializer = SearchSerializer(articles, many=True)
    # JSON 응답 반환
    return Response(serializer.data)