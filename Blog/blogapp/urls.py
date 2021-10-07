from django.urls import path,include
from . import views 
urlpatterns = [
    path('',views.HomeView.as_view(),name="home" ),
    path('article/<int:pk>',views.ArticleView.as_view(),name="article" ),
    path('article/<int:pk>/comment',views.AddCommentView.as_view(),name="add_comment" ),
    path('add_post/',views.AddPostView.as_view(),name="add_post" ),
    path('add_category/',views.AddCategoryView.as_view(),name="add_category" ),
    path('article/edit/<int:pk>',views.EditPostView.as_view(),name="edit_post" ),
    path('article/delete/<int:pk>',views.DeletePostView.as_view(),name="delete_post" ),
    # path('category/<str:cats>',views.CategoryView,name="category" ),
    path('category/<str:cats>',views.CategoryView.as_view(),name="category" ),
    path('search',views.search_post,name="search" ),
    path('my_posts',views.MyPostView.as_view(),name="my_posts"),
    

]
