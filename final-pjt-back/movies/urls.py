from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.get_movies_genres),
    path('recommended/', views.recommended),
    path('<int:movie_id>/rating/', views.get_create_rating),
    path('<int:movie_id>/rating/<int:rating_id>/', views.update_delete_rating),
    path('my-rating/', views.get_my_rating)
]
