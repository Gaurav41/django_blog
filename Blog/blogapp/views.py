from django.db import models
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import Post,Category,Comment
from .forms import PostForm,EditForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
# Create your views here.
def home(request):
    return render(request,"blogapp/home.html")
    # return HttpResponse("Hi")


class HomeView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    # ordering = ['-id']
    ordering = ['-publish_date']
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()
        return context


class ArticleView(DetailView):
    model = Post
    template_name = 'blogapp/article.html'

class AddPostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogapp/add_post.html'

    # fields = '__all__'
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        # self.object = form.save()
        instance.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect(instance.get_absolute_url())

    
class EditPostView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'blogapp/edit_post.html'
    # fields=['title','body']
    form_class = EditForm
    
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.has_perm('blog_permission.blog_edit'):
    #         raise PermissionDenied()
    #     return super(EditPostView, self).dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(EditPostView, self).get_object(*args, **kwargs)
        if obj.author.id == self.request.user.id:
            return obj   
        raise PermissionDenied #Http404
        

    

class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blogapp/delete_post.html'
    success_url=reverse_lazy('home')

class AddCategoryView(LoginRequiredMixin,CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'blogapp/add_category.html'
    fields = '__all__'


# def CategoryView(request,cats):
#     cats = cats.replace('-',' ')
#     category_posts = Post.objects.filter(category=cats).order_by("-publish_date")
#     return render(request,'blogapp/categories.html',{'category':cats.title(),'category_posts':category_posts})


class CategoryView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    # ordering = ['-id']
    ordering = ['-publish_date']

    def get_queryset(self,*args, **kwargs):
        cats = self.kwargs['cats'].replace('-',' ')
        category_posts = Post.objects.filter(category=cats).order_by("-publish_date")
        return category_posts

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()
        return context

# Add comment
class AddCommentView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    # fields = '__all__'
    template_name = 'blogapp/add_comment.html'
    ordering = ['-date_added']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)