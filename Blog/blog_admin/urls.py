from django.urls import path,include
from . import views

urlpatterns=[
    path('admin_home/',views.HomeView.as_view(),name='admin_home'),
    path('add_user',views.AddUserView.as_view(),name='add_user'),
    path('edit_user/<int:pk>',views.EditUserView.as_view(),name='edit_user'),
    # path('delete_user/<int:pk>',views.DeleteUserView.as_view(),name='delete_user'),
    path('delete_user/<int:pk>',views.delete_user,name='delete_user'),
    path('users',views.UserList.as_view(),name='users'),
    path('posts',views.PostListView.as_view(),name='posts'),
    path('comments',views.CommentsListView.as_view(),name='comments'),
    path('comments/delete/<int:pk>',views.delete_comment,name='delete_comment'),
]