from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.conf import settings


class CheckReaderGroupMixin():
    
    def dispatch(self,request,*args,**kwargs):        
        if request.user.groups.filter(name="reader")or request.user.groups.filter(name="commentor") or request.user.groups.filter(name="editor") or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            # return True
        else:
            raise PermissionDenied


class CheckCommentorGroupMixin():
    
    def dispatch(self,request,*args,**kwargs):        
        if request.user.groups.filter(name="commentor")or request.user.groups.filter(name="editor") or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            # return True
        else:
            raise PermissionDenied


class CheckEditorGroupMixin():
    
    def dispatch(self,request,*args,**kwargs):        
        if request.user.groups.filter(name="editor")or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            # return True
        else:
            raise PermissionDenied
