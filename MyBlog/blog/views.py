from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View, FormView

from blog.forms import PostCreationForm
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
        already_read_queryset = list(AlreadyRead.objects.filter(user=request.user).values_list('post_id', flat=True))
        followers_queryset = list(UserFollowing.objects.filter(user=request.user).values_list('following', flat=True))
        post_list = Post.objects.filter(author__in=followers_queryset).exclude(id__in=already_read_queryset).order_by(
            '-date')
        template_name = 'blog/subs_list.html'
        context = {'post_list': post_list}
        return render(request, template_name, context)


class AddAlreadyReadView(View, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        AlreadyRead.objects.get_or_create(user=request.user, post=post)
        already_read_queryset = list(AlreadyRead.objects.filter(user=request.user).values_list('post_id', flat=True))
        followers_queryset = list(UserFollowing.objects.filter(user=request.user).values_list('following', flat=True))
        post_list = Post.objects.filter(author__in=followers_queryset).exclude(id__in=already_read_queryset).order_by(
            '-date')
        template_name = 'blog/subs_list.html'
        context = {'post_list': post_list}
        return render(request, template_name, context)


class PostCreateView(FormView, LoginRequiredMixin):
    def post(self, request, ordering='AZ', *args, **kwargs):
        template_name = 'add_post.html'
        form = PostCreationForm(request.POST, author=request.user)
        if form.is_valid():
            # Данные формы валидны.
            # img = form.cleaned_data.get("image")
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.author = request.user
            # Добавляем пользователя к созданному объекту.
            new_item.save()
            '''
            mail_host = "localhost"
            user_list = User.objects.filter(id__in=lst_of_ids)
            recipients = []
            for user in user_list:
                recipients.append(user.email)
            message = 'У пользователя {0} в блоге появилась новая запись!'.format(user)
            subject = 'Новый пост'
            send_mail(subject, message, mail_host, recipients, fail_silently=False)
            '''
            return redirect("/home/")

    def get(self, request, ordering='AZ', *args, **kwargs):
        template_name = 'blog/create.html'
        form = PostCreationForm(author=request.user)
        context = {'form': form}
        return render(request, template_name, context)


class PostEditView(FormView, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['id'])
        author = post.author
        form = PostCreationForm(request.POST, instance=post, author=request.user)
        if form.is_valid() and author == request.user:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home/")

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['id'])
        form = PostCreationForm(request.POST, instance=post, author=request.user)
        return render(request, 'blog/post_edit.html', {'form': form})


class PostDeleteView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['id'])
        author = post.author
        if author == request.user:
            Post.objects.get(id=self.kwargs['id']).delete()
        return redirect("/home/")
