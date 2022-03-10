from django.contrib.auth.models import AnonymousUser
from django.shortcuts import HttpResponse, get_list_or_404,  get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth import get_user_model
from .models import Movie, Genre, Rating
from .serializers import MovieSerializer, RatingSerializer, RatingListSerializer
import requests
import random
import json
import os


BASE_URL = 'https://api.themoviedb.org/3'
paths = [
        'popular',
        'now_playing',
        'top_rated',
        'upcoming'
]

def get_movies_genres(request):
    '''
    데이터 seeding
    '''
    movies_and_genres = []

    for path in paths:
        response = requests.get(f'{BASE_URL}/movie/{path}', params = {
            'api_key': os.environ.get('API_KEY'),
            'language': 'ko-KR',
            'region': 'KR',
        })

        movies = response.json()['results']
        for movie in movies:
            dict_movie = {}
            dict_movie['model'] = 'movies.movie'
            dict_fields = {
                'movie_code': movie['id'],
                'title': movie['title'],
                'release_date': movie['release_date'],
                'popularity': movie['popularity'],
                'vote_average': movie['vote_average'],
                'overview': movie['overview'],
                'genres': movie['genre_ids'],
                'poster_path': movie['poster_path'],
                'backdrop_path': movie['backdrop_path'],
                'category': path,
            }

            dict_movie['fields'] = dict_fields
            movies_and_genres.append(dict_movie)

    response_genres = requests.get(f'{BASE_URL}/genre/movie/list?', params = {
        'api_key': os.environ.get('API_KEY'),
        'language': 'ko-KR',
    }).json()

    genres = response_genres['genres']
    for genre in genres:
        dict_genre = {
            'model': 'movies.genre',
            'pk': genre['id'],
            'fields': {
                'name': genre['name']
            }
        }
        movies_and_genres.append(dict_genre)

    with open('./movies/fixtures/movies.json', 'w', encoding="utf-8") as json_file:
        json.dump(movies_and_genres, json_file, ensure_ascii=False, indent=4)

    return HttpResponse('message')


@api_view(['GET'])
@permission_classes([AllowAny])
def recommended(request):
    '''
    추천 영화 데이터(popular, now_playing, top_rated, upcoming, 랜덤 장르 영화, 랜덤 배우 영화, 랜덤 감독 영화) 리턴
    '''
    all_movies = Movie.objects.all()
    recommended_movies = {}

    for path in paths:
        serializer = MovieSerializer(all_movies.filter(category__exact=path), many=True)
        recommended_movies[path] = serializer.data
    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        data = {'token': token}
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        user_id = valid_data['user_id']
        user = get_object_or_404(get_user_model(), pk=user_id)
    except:
        user = ''

    if user and user.rating_set.filter(rank__gte=7):
        random_like_genres = []
        random_like_movies = []
        recommended_movies['user'] = user.username
        for rating in request.user.rating_set.filter(rank__gte=7):
            random_like_movies.append(rating.movie)
            for like_genre in rating.movie.genres.all():
                random_like_genres.append(like_genre)
        random_genre = random.choice(random_like_genres)
        random_movie = random.choice(random_like_movies)
    else:
        genres = []
        for genre in Genre.objects.all():
            genres.append(genre)
        random_genre = random.choice(genres)

        random_movie = random.choice(all_movies)

    
    response = requests.get(f'{BASE_URL}/movie/{random_movie.movie_code}/credits', params = {
            'api_key': os.environ.get('API_KEY'),
            'language': 'ko-KR',
    }).json()
    
    if response['cast']:
        random_actor = response['cast'][0]
    else:
        random_actor = {'id': 1713025, 'name': '장동윤'}

    crews = response['crew']
    random_director = {'id': 126809, 'name': '이준익'}
    for crew in crews:
        if crew['job'] == 'Director':
            random_director = crew
            break

    query_string_info = {
        'with_genres': (random_genre.pk, random_genre.name),
        'with_cast': (random_actor['id'], random_actor['name']),
        'with_crew': (random_director['id'], random_director['name'])
    }

    for key, val in query_string_info.items():
        response = requests.get(f'{BASE_URL}/discover/movie', params = {
            'api_key': os.environ.get('API_KEY'),
            'language': 'ko-KR',
            'region': 'KR',
            key: f'{val[0]}',
        })

        movies = response.json()['results']
        movie_obj = []
        for movie in movies:
            dict_movie = {
                'id': movie['id'],
                'movie_code': movie['id'],
                'title': movie['title'],
                'release_date': movie['release_date'],
                'popularity': movie['popularity'],
                'vote_average': movie['vote_average'],
                'overview': movie['overview'],
                'poster_path': movie['poster_path'],
                'category': key,
                'genres': movie['genre_ids'],
            }
            movie_obj.append(dict_movie)
        recommended_movies[key] = { 'name': val[1], 'movies': movie_obj }
    return Response(recommended_movies, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # allowAny를 안하면 로그인 안한 사용자가 MovieModal을 띄웠을 때 Rating을 GET하면서 버그
def get_create_rating(request, movie_id):
    '''
    1. 프론트 쪽에 있는 모든 영화가 저장되어 있지 않으므로, db pk 값이 없다.
    DB에 저장했던 4개의 카테고리에서만 정상 동작한다.
    '''
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        ratings = Rating.objects.filter(movie=movie)
        serializer = RatingListSerializer(instance=ratings, many=True)
        return Response(serializer.data)

    user = get_object_or_404(get_user_model(), pk=request.data['userId'])
    if request.method == 'POST':
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def update_delete_rating(request, movie_id, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.method == 'PUT':
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        rating.delete()
        return Response(status=HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_my_rating(request):
    ratings = get_list_or_404(Rating, user=request.user.id)
    serializer =RatingListSerializer(instance=ratings, many=True)
    return Response(serializer.data)
