from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('tweeet_like/<int:pk>', views.tweeet_like, name='tweeet_like'),
    path('show_tweeet/<int:pk>', views.show_tweeet, name='show_tweeet'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/following/<int:pk>', views.following, name='following'),
    path('delete_tweeet/<int:pk>', views.delete_tweeet, name='delete_tweeet'),
    path('search/', views.search, name='search'),
    path('search_users/', views.search_users, name='search_users'),

]
