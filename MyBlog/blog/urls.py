from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', lambda req: redirect('/home/')),
    path('all/', views.PostListView.as_view(), name='post_list'),
    path('myblog/', views.MyPostListView.as_view(), name='my_post_list'),
    path('home/', views.SubsListView.as_view(), name='subs_post_list'),
    path('add_user/<str:username>/', views.AddUserView.as_view(), name='add_user'),
    path('delete_user/<str:username>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('<str:username>/', views.UserPostListView.as_view(), name='user_post_list'),
]
