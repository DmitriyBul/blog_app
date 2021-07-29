from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View

from blog.models import Post, UserFollowing, AlreadyRead
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        post_list = Post.objects.all().order_by('-date')
        context_object_name = 'posts'
        template_name = 'blog/post_list.html'
        context = {'post_list': post_list}
        return render(request, template_name, context)


class UserPostListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        post_list = Post.objects.filter(author__username=self.kwargs['username'])
        blog_author = get_object_or_404(User, username=self.kwargs['username'])
        blog_author_name = blog_author.username
        template_name = 'blog/user_post_list.html'
        user_id = request.user.id
        user_in_followers = list(UserFollowing.objects.filter(user=request.user).values_list('following', flat=True))
        if blog_author.id in user_in_followers:
            user_in_list = True
        else:
            user_in_list = False
        context = {'blog_author_name': blog_author_name, 'post_list': post_list, 'user_in_list': user_in_list}
        return render(request, template_name, context)


class MyPostListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        post_list = Post.objects.filter(author=request.user)
        template_name = 'blog/my_post_list.html'
        context = {'post_list': post_list}
        return render(request, template_name, context)


class AddUserView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(User, username=self.kwargs['username'])
        UserFollowing.objects.get_or_create(user=request.user, following=user_to_follow)
        return redirect("/home/")


class DeleteUserView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(User, username=self.kwargs['username'])
        UserFollowing.objects.filter(user=request.user, following=user_to_follow).delete()
        return redirect("/home/")


class SubsListView(ListView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        qs = UserFollowing.objects.filter(user=request.user).values_list('following', flat=True)
        lst_of_ids = list(qs)
        ar_qs = AlreadyRead.objects.filter(user=request.user).values_list('post_id', flat=True)
        lst_of_ar = list(ar_qs)
        post_list = Post.objects.filter(author__in=lst_of_ids).exclude(id__in=lst_of_ar).order_by('-date')
        # post_list = Post.objects.filter(author=request.user)
        template_name = 'blog/subs_list.html'
        context = {'post_list': post_list}
        return render(request, template_name, context)
