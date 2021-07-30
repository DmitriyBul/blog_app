from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', lambda req: redirect('/home/')),
    path('all/', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('edit/<int:id>/', views.PostEditView.as_view(), name='post_edit'),
    path('delete/<int:id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('myblog/', views.MyPostListView.as_view(), name='my_post_list'),
    path('home/', views.SubsListView.as_view(), name='subs_post_list'),
    path('add_user/<str:username>/', views.AddUserView.as_view(), name='add_user'),
    path('delete_user/<str:username>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('<str:username>/', views.UserPostListView.as_view(), name='user_post_list'),
    path('alreadyread/<int:id>/', views.AddAlreadyReadView.as_view(), name='already_read'),
]
