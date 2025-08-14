from django.urls import path, include
from . import views
from .groq_chat import chat_api

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('news/', views.news_view, name='news'),
    # New URL for news modal
    path('news/<int:news_id>/modal/', views.news_detail_modal, name='news_detail_modal'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('contact/', views.contact, name='contact'),
    path('api/chat/', chat_api, name='chat_api'),
    path('post/create/', views.create_issue_post, name='create_issue_post'),  # Renamed for clarity
    path('feed/', views.feed, name='feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/update-status/', views.update_post_status, name='update_post_status'),
    path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),
    path('post/<int:post_id>/comments/form/', views.comment_form, name='comment_form'),
    path('saved/', views.saved_posts_view, name='saved_posts'),
    path('post/<int:post_id>/save/', views.toggle_save_post, name='toggle_save_post'),
    path('verify-task/<int:task_id>/', views.verify_task, name='verify_task'),  # Admin/internal use
]

# User authentication URLs
urlpatterns += [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
