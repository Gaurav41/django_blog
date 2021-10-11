from django.urls import path,include
from . import views
urlpatterns = [
   path('register/',views.UserRegistrationView.as_view(),name='register'),
   path('logout/',views.logout_user,name='logout'),
   path('edit_profile/',views.UserEditView.as_view(),name='edit_profile'),
   path('password/', views.user_change_password, name="changepassword"),
]
