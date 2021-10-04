from django.db import models
from django.shortcuts import render,HttpResponse
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm,EditForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
def home(request):
    return render(request,"blogapp/home.html")
    # return HttpResponse("Hi")


class HomeView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    # ordering = ['-id']
    ordering = ['-publish_date']

class ArticleView(DetailView):
    model = Post
    template_name = 'blogapp/article.html'

class AddPostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogapp/add_post.html'
    # fields = '__all__'
    
class EditPostView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'blogapp/edit_post.html'
    # fields=['title','body']
    form_class = EditForm


class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blogapp/delete_post.html'
    success_url=reverse_lazy('home')