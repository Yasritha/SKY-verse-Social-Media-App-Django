from django.urls import path
from . import views
from .views import chat_view,friends_list
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('switch_mode/<str:mode>/', views.switch_mode, name='switch_mode'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('explore/', views.explore_view, name='explore'),
    path('category/<str:category_name>/', views.category_view, name='category'),
    path('category/entertainment/', views.entertainment_category, name='entertainment_category'),
    path('category/education/', views.education_category, name='education_category'),
    path('category/job/', views.job_category, name='job_category'),
    path('category/news/', views.news_category, name='news_category'),
    path('category/shopping/', views.shopping_category, name='shopping_category'),
    path('category/friends/', views.friends_category, name='friends_category'),
    path('category/kids/',views.kids_category, name='kids_category'),
    path('category/mixed/', views.mixed_category, name='mixed_category'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('kids_home/', views.kids_home_view, name='kids_home'),
    path('', views.home, name='home'),
    path('friends/', views.view_friends, name='view_friends'),
    path('chat/<int:friend_id>/', views.chat_with, name='chat_with'),
    path('friend_requests/', views.view_friend_requests, name='view_friend_requests'),
    path('friend_suggestions/', views.view_friend_suggestions, name='view_friend_suggestions'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('ignore_friend_request/<int:request_id>/', views.ignore_friend_request, name='ignore_friend_request'),
    # Add other URLs as per your application's needs
]


