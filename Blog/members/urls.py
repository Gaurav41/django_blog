from django.urls import path,include
from . import views
urlpatterns = [
   path('register/',views.UserRegistrationView.as_view(),name='register'),
   path('edit_profile/',views.UserEditView.as_view(),name='edit_profile'),
]
