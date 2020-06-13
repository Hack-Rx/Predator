from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexview, name='Index'),
    path('login', views.loginview, name='Login'),
    path('create-profile', views.create_profile_view, name='create_profile'),
    path('profile', views.show_profile_view, name='show_profile'),
    path('update-profile', views.update_profile_view, name='update_profile'),
    path('add-food', views.add_food_view, name='add_food'),
    path('food-list', views.food_list_view, name='food_list'),
    path('create-walk', views.create_walk_view, name='create_walk'),
    path('walk-list', views.walk_list_view, name='walk_list')
]