from django.urls import path
from . import views
from django.urls import path
from .groq_chat import chat_api
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('report/', views.report_issue, name='report_issue'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('tasks/', views.tasks, name='tasks'),
    path('store/', views.store, name='store'),
    path('news/', views.news, name='news'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('contact/', views.contact, name='contact'),
    path('report/<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('report/<int:report_id>/delete/', views.delete_report, name='delete_report'),
    path('redemptions/', views.redeem_history, name='redeem_history'),
    path('area-issues/', views.area_issues, name='area_issues'),
    path('api/chat/', chat_api, name='chat_api'),
    

]


from .views import user_register, user_login, user_logout

urlpatterns += [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
