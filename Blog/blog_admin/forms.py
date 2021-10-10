from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.forms.models import ModelForm

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

choices_list=[]
for user in User.objects.all():
        choices_list.append(user.groups.values_list('name','name'))



class UserFilterForm(forms.ModelForm):
    username = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control','required': False}))
    email = forms.EmailField(max_length=250,widget=forms.EmailInput(attrs={'class':'form-control','required': False}))
    is_staff = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check','required': False}))

    class Meta:
        model = User
        fields = ['username','email','groups','is_staff']

        # widgets={
        #     # 'username' : forms.TextInput(attrs={'class':'form-control'}),
        #     'groups':forms.Select(choices=choices_list,attrs={'class':'form-control'}),
        #     # 'is_staff' : forms.BooleanField(attrs={'class':'form-control'}),
        # }


class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    # first_name = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}))
    # password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['email','username','password1','password2']
        labels={'email':'Email'}

    def __init__(self,*args,**kwargs):
        super(SignupForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'