from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.urls import reverse_lazy,reverse
from .forms import SignupForm,EditProfileForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


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

@login_required()
def user_change_password(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            # to keep user logged in
            # update_session_auth_hash(request,fm.user)
            return HttpResponseRedirect(reverse('home'))    
    else:
        fm = PasswordChangeForm(request.user)
        # fm = SetPasswordForm(request.user)
    return render(request,"registration/change_password.html",{'form':fm})