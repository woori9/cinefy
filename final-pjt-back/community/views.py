from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Review, Comment
from .serializers import CommentSerializer, ReviewListSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


@api_view(['GET'])
@permission_classes([AllowAny])
def review_list(request):
    '''
    GET: 리뷰 목록 가져오기
    '''

    if request.method == 'GET':
        reviews = Review.objects.order_by('-pk')
        serializers = ReviewListSerializer(reviews, many=True)
        return Response(serializers.data)


@api_view(['POST'])
def review_create(request):
    '''
    POST: 리뷰 작성
    '''
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delete(request, review_pk):
    '''
    GET: 해당 리뷰 정보 가져오기
    PUT: 해당 리뷰 수정
    DELETE: 해당 리뷰 삭제
    '''
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': '글이 삭제되었습니다.'}, status=HTTP_204_NO_CONTENT)


@api_view(['POST'])
def review_like(request, review_pk):
    '''
    POST: 리뷰 좋아요 추가/삭제
    '''
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        liked = False
    else:
        review.like_users.add(request.user)
        liked = True
    context = {
        'isLiked': liked,
        'likeCnt': review.like_users.count(),
    }
    return Response(context)


@api_view(['POST'])
def comment_create(request, review_pk):
    '''
    POST: 해당 리뷰에 댓글 작성
    '''
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(review=review, user=request.user)
                return Response(serializer.data, status=HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
def comment_update_delete(request, review_pk, comment_pk):
    '''
    PUT: 해당 리뷰에 있는 해당 댓글 수정
    DELETE: 해당 리뷰에 있는 해당 댓글 삭제
    '''
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    if request.method == 'DELETE':
        comment.delete()
        return Response({'message': '댓글이 삭제되었습니다.'}, status=HTTP_204_NO_CONTENT)
