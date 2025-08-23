from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_discussions, name='category_discussions'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/new/', views.new_discussion, name='new_discussion'),
    path('discussion/<int:discussion_id>/add_comment/', views.add_comment, name='add_comment'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
]
