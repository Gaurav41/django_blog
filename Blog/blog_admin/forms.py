from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}))
    is_superuser= forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check','required': False}))
    is_staff = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check','required': False}))
    is_active = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check','required': False}))
    date_joined = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','is_active','is_staff','is_superuser']
        labels={'email':'Email'}