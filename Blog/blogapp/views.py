from django.db import models
from django.db.models import fields
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post,Category,Comment
from .forms import PostForm,EditForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .mixins import CheckReaderGroupMixin, CheckCommentorGroupMixin, CheckEditorGroupMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request,"blogapp/home.html")
    # return HttpResponse("Hi")

class PostFilter(django_filters.FilterSet):
    # start_date = django_filters.DateFilter(field_name='publish_date',lookup_expr='gte')
    # end_date = django_filters.DateFilter(field_name='publish_date',lookup_expr='lte')
    # range = django_filters.DateFromToRangeFilter (field_name='publish_date',lookup_expr='lte')
    body = django_filters.CharFilter(field_name='body',lookup_expr='icontains')
    # category = django_filters.CharFilter(field_name='category',lookup_expr='icontains')
    class Meta:
        model = Post
        fields="__all__"
        exclude=['body','publish_date']


class HomeView(ListView):
    # LOGIN_URL = reverse_lazy('login')

    model = Post
    template_name = 'blogapp/home.html'
    ordering = ['-publish_date']
    # filter_backends = [DjangoFilterBackend]
    # filterset_fileds=['category']
    
    filterset_class = PostFilter
    def get_template_names(self):
        # if self.request.user.is_superuser:
        #     template_name = 'blog_admin/index.html'
        # else:
        #     template_name = 'blogapp/home.html'
        template_name = 'blogapp/home.html'
        return template_name



    def get_queryset(self):
        keyword = self.request.GET.get('search','')
        if keyword:
            posts = Post.objects.filter(body__contains=keyword)
            return posts
        # myFilter = PostFilter(self.request.GET,self.get_queryset())
        return super().get_queryset()
    
    def get_context_data(self,*args, **kwargs):
        myFilter = PostFilter(self.request.GET,self.get_queryset())
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()
        context['myFilter']= myFilter  
        context['object_list']= myFilter.qs  
        return context




# def post_filter(request):
# 	posts= Post.object.all()
# 	filter = PostFilter(request.GET, queryset = posts)
# 	return render(request, 'blogapp/home.html', {'object_list' : filter})



class ArticleView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'blogapp/article.html'

class AddPostView(LoginRequiredMixin,CheckEditorGroupMixin,CreateView):
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

    
class EditPostView(LoginRequiredMixin,CheckEditorGroupMixin,UpdateView):
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
        

    

class DeletePostView(LoginRequiredMixin,CheckEditorGroupMixin,DeleteView):
    model = Post
    template_name = 'blogapp/delete_post.html'
    success_url=reverse_lazy('home')

class AddCategoryView(LoginRequiredMixin,CheckEditorGroupMixin,CreateView):
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
    filterset_class = PostFilter
    def get_queryset(self,*args, **kwargs):
        cats = self.kwargs['cats']
        category_posts = Post.objects.filter(category=cats).order_by("-publish_date")
        return category_posts

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()

        myFilter = PostFilter(self.request.GET,self.get_queryset())
        context['myFilter']= myFilter  
        context['object_list']= myFilter.qs 
        return context

# Add comment
class AddCommentView(LoginRequiredMixin,CheckCommentorGroupMixin,CreateView):
    model = Comment
    form_class = CommentForm
    # fields = '__all__'
    template_name = 'blogapp/add_comment.html'
    ordering = ['-date_added']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)


# Search Post
def search_post(request):
    if request.method == 'POST':
        keyword = request.POST['search']
        posts = Post.objects.filter(body__contains=keyword)
        return render(request,'blogapp/home.html',{'object_list':posts})
    return render(request,'blogapp/home.html')


class MyPostView(LoginRequiredMixin, CheckEditorGroupMixin ,ListView):
    model = Post
    template_name = 'blogapp/myposts.html'
    ordering = ['-publish_date']
    
    filterset_class = PostFilter

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.user)
        return posts
    
    def get_context_data(self,*args, **kwargs):
        myFilter = PostFilter(self.request.GET,self.get_queryset())
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()
        context['myFilter']= myFilter  
        context['object_list']= myFilter.qs  
        return context
        

class SocialLoginTemplateView(TemplateView):
    template_name="blogapp/social_login.html"