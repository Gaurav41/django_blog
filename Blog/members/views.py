from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.urls import reverse_lazy
from .forms import SignupForm,EditProfileForm
from django.contrib.auth import logout

# Create your views here.

class UserRegistrationView(generic.CreateView):
    # form_class = UserCreationForm
    form_class = SignupForm # our custom form  instead UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login') 

class UserEditView(generic.UpdateView):
    # form_class = UserChangeForm  
    form_class = EditProfileForm  
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy('home') 

    def get_object(self):
        return self.request.user

def logout_user(request):
    logout(request)
