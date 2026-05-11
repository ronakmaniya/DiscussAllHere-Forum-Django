from django.urls import path
from . import views

# urlpatterns is done by both {{Ronak CE037}} and {{Utsav CE027}} Accordingly
urlpatterns = [
    path('', views.home, name='home'),
    path('discussions/', views.discussion_list, name='discussion_list'),
    path('category/new/', views.new_category, name='new_category'),
    path('category/<slug:category_slug>/', views.category_discussions, name='category_discussions'),
    path('discussion/<slug:discussion_slug>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/new/<slug:category_slug>/', views.new_discussion, name='new_discussion'),
    path('discussion/<slug:discussion_slug>/edit/', views.edit_discussion, name='edit_discussion'),
    path('discussion/<slug:discussion_slug>/delete/', views.delete_discussion, name='delete_discussion'),
    path('discussion/<slug:discussion_slug>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
]
