from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Comment, Post,Category

# choices = [('coding','coding'),('lifestyle','lifestyle'),('sport','sport'),('health','health'),]
choices = Category.objects.all().values_list('name','name')
# print(choices)
choices_list=[]

for item in choices:
    choices_list.append(item)
# print(choices_list)


class PostForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(PostForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['author'].required = False
    
    class Meta:
        model = Post
        fields = ['title','author','category','body']

        widgets={
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            # 'author' : forms.Select(attrs={'class':'form-control'}),
            'author' : forms.HiddenInput(attrs={'class':'form-control','required': False}),
            # 'category':forms.Select(choices=choices,attrs={'class':'form-control'}),
            'category':forms.Select(choices=choices_list,attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title','body']

        widgets={
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            # 'author' : forms.Select(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['body']

        widgets={
            # 'user' : forms.TextInput(attrs={'class':'form-control'}),
            # 'author' : forms.Select(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control'})
        }
