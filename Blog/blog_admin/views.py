from django.shortcuts import redirect, render
from django.views.generic import TemplateView,CreateView,UpdateView,ListView
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import DeleteView
from blogapp.models import Post,Category,Comment
from blogapp.views import PostFilter,HomeView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import django_filters
from .forms import EditProfileForm,UserFilterForm,SignupForm
from django.http import HttpResponseForbidden
from .permissions import IsStaffOrSuperUserMixin

# Create your views here.


class HomeView(IsStaffOrSuperUserMixin,TemplateView):
    
    template_name = 'blog_admin/index.html'


class UserFilter(django_filters.FilterSet):
    
    class Meta:
        form = UserFilterForm
        model = User
        fields=['email','is_staff','groups','is_active','is_superuser']
    

class AddUserView(IsStaffOrSuperUserMixin,CreateView):
    # permission_classes=[IsSelfOrReadOnly]
    # authentication_classes=[SessionAuthentication]
    # form_class = UserCreationForm
    form_class = SignupForm
    template_name = "blog_admin/add_user.html"
    # success_url = "/edit_user/" 
    
    def get_absolute_url(self,**kwargs):
        print("*"*50)
        username = kwargs['username']
        user = User.objects.get(username=username)
        print(user)
        return reverse('edit_user',args=(user.id,))
        
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset

    def form_valid(self, form):
        # instance = form.save(commit=False)
        # username = self.request.user
        # self.object = form.save()
        user = form.save()
        print("User: ",user)
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        return  HttpResponseRedirect(self.get_absolute_url(username=user))




class EditUserView(IsStaffOrSuperUserMixin,UpdateView):
    model = User
    # form_class = UserChangeForm  
    form_class = EditProfileForm  
    template_name = "blog_admin/edit_user.html"
    success_url = reverse_lazy('users') 

    # def get_object(self,**kwargs):
    #     if kwargs:
    #         username = self.kwargs['user']
    #         user = User.objects.get(username=username)
    #         print(user)
    #     return user
    
    # def get_absolute_url(self):
    #     return reverse('article',args=(str(self.id),))

    # def form_valid(self, form):
    #     # instance = form.save(commit=False)
    #     # username = self.request.user
    #     # self.object = form.save()
    #     user = form.save()
    #     print("User: ",user)
    #     # do something with self.object
    #     # remember the import: from django.http import HttpResponseRedirect
    #     return  HttpResponseRedirect(self.get_absolute_url(user=user))

class DeleteUserView(IsStaffOrSuperUserMixin,DeleteView):
    model = User
    template_name = 'blog_admin/delete_User.html'
    success_url=reverse_lazy('users')


# def delete_user(request,pk):
#     try:
#         user = User.objects.get(pk=pk)
#         user.delete()
#         return redirect(reverse('users'))
#     except :
#         return redirect(reverse('users'))

class DeleteUserView(IsStaffOrSuperUserMixin,DeleteView):
    model = User
    template_name = 'blog_admin/delete_confirm.html'
    success_url = reverse_lazy('users')


class UserList(IsStaffOrSuperUserMixin,ListView):
    template_name = 'blog_admin/users.html'
    model = User
    # ordering = ['-publish_date']
    context_object_name = 'users'
    # filter_backends = [DjangoFilterBackend]
    # filterset_fileds=['category']
    
    filterset_class = UserFilter

    def get_context_data(self,*args, **kwargs):
        myFilter = UserFilter(self.request.GET,self.get_queryset())
        context = super().get_context_data(*args,**kwargs)
        # context['categories']= Category.objects.all()
        context['myFilter']= myFilter  
        context['users']= myFilter.qs  
        return context


class PostListView(IsStaffOrSuperUserMixin,ListView):
    model = Post
    template_name = 'blog_admin/posts.html'
    ordering = ['-publish_date']
    context_object_name = 'posts'    
    filterset_class = PostFilter
    
    def get_context_data(self,*args, **kwargs):
        myFilter = PostFilter(self.request.GET,self.get_queryset())
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()
        context['myFilter']= myFilter  
        context['posts']= myFilter.qs  
        return context

class CommentFilter(django_filters.FilterSet):
    # start_date = django_filters.DateFilter(field_name='publish_date',lookup_expr='gte')
    # end_date = django_filters.DateFilter(field_name='publish_date',lookup_expr='lte')
    # range = django_filters.DateFromToRangeFilter (field_name='publish_date',lookup_expr='lte')
    body = django_filters.CharFilter(field_name='body',lookup_expr='icontains')
    # category = django_filters.CharFilter(field_name='category',lookup_expr='icontains')
    class Meta:
        model = Comment
        fields="__all__"
        exclude=['body','user','post','date_added']



class CommentsListView(IsStaffOrSuperUserMixin,ListView):
    model = Comment
    template_name = 'blog_admin/comments.html'
    ordering = ['-date_added']
    context_object_name = 'comments'    
    filterset_class = CommentFilter
    
    def get_context_data(self,*args, **kwargs):
        myFilter = CommentFilter(self.request.GET,self.get_queryset())
        context = super().get_context_data(*args,**kwargs)
        context['categories']= Category.objects.all()
        context['myFilter']= myFilter  
        context['comments']= myFilter.qs  
        return context



# class CommentDeleteView(DeleteView):
#     model = Comment
#     success_url  = 'blog_admin/comments.html'
#     def get_object(self, queryset=None):
#         """ Hook to ensure object is owned by request.user. """
#         obj = super(CommentDeleteView, self).get_object()
#         if not (obj.user == self.request.user or self.request.user.is_superuser()) :
#             raise Http404
#         return obj


def delete_comment(request,pk):

    # try:
    comment = Comment.objects.get(pk=pk)
    if (comment.user == request.user or request.user.is_superuser) :
        comment.delete()
        return redirect(reverse('comments'))
    
    return HttpResponseForbidden()
        
    # except :
    #     return redirect(reverse('comments'))

class AddCategoryView(IsStaffOrSuperUserMixin,CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'blog_admin/add_category.html'
    fields = '__all__'
    success_url = '/blog_admin/admin_home/'


class CategoryView(IsStaffOrSuperUserMixin,ListView):
    model = Category
    template_name = 'blog_admin/categories.html'
    context_object_name = 'categories'
                              
# DeleteCategoryView

class DeleteCategoryView(IsStaffOrSuperUserMixin,DeleteView):
    model = Category
    template_name = 'blog_admin/delete_confirm.html'
    success_url = reverse_lazy('categories')
    

class EditCategoryView(IsStaffOrSuperUserMixin,UpdateView):
    model = Category
    template_name = 'blog_admin/edit_category.html'
    success_url = reverse_lazy('categories') 
    fields = '__all__'
