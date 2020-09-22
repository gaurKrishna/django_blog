from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.contrib.auth.models import User

def home(request):
    return render(request, 'blog/home.html', context={'posts': Post.objects.all(), 'title': "My Django blog"})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    #By default search for blog/post_List.html
    #Naming convention <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(post_author = user).order_by('date_posted')

class PostDetailView(DetailView):
    model = Post  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    #It will share template with update view
    #The defaullt template it searchf for is post_form.html

    def form_valid(self, form):
        form.instance.post_author = self.request.user

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    #It will share template with update view
    #The defaullt template it searchf for is post_form.html

    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_author:
            return True
        return False 


def about(request):
    return render(request, 'blog/about.html')

