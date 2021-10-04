from django.urls import path,include
from . import views 
urlpatterns = [
    path('',views.HomeView.as_view(),name="home" ),
    path('article/<int:pk>',views.ArticleView.as_view(),name="article" ),
    path('add_post/',views.AddPostView.as_view(),name="add_post" ),
    path('article/edit/<int:pk>',views.EditPostView.as_view(),name="edit_post" ),
    path('article/delete/<int:pk>',views.DeletePostView.as_view(),name="delete_post" ),
]
