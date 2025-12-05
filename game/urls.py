from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_game, name='new_game'),
    path('hit/', views.hit, name='hit'),
    path('stand/', views.stand, name='stand'),
    path('split/', views.split, name='split'),
    path('state/', views.game_state, name='game_state'),
]