from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('discussions/', views.discussion_list, name='discussion_list'),
    path('discussions/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/new/', views.new_discussion, name='new_discussion'),
]
