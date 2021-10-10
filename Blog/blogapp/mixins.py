from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.conf import settings

from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin


# class CheckReaderGroupMixin():
    
#     def dispatch(self,request,*args,**kwargs):        
#         if request.user.groups.filter(name="reader")or request.user.groups.filter(name="commentor") or request.user.groups.filter(name="editor") or request.user.is_superuser:
#             return super().dispatch(request, *args, **kwargs)
#             # return True
#         else:
#             raise PermissionDenied

class CheckReaderGroupMixin(UserPassesTestMixin,LoginRequiredMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["reader","commentor","editor"]) 


# class CheckCommentorGroupMixin():
    
#     def dispatch(self,request,*args,**kwargs):        
#         if request.user.groups.filter(name="commentor")or request.user.groups.filter(name="editor") or request.user.is_superuser:
#             return super().dispatch(request, *args, **kwargs)
#             # return True
#         else:
#             raise PermissionDenied



class CheckCommentorGroupMixin(UserPassesTestMixin,LoginRequiredMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["commentor","editor"]) or self.request.user.is_superuser


# class CheckEditorGroupMixin():
    
#     def dispatch(self,request,*args,**kwargs):        
#         if request.user.groups.filter(name="editor")or request.user.is_superuser:
#             return super().dispatch(request, *args, **kwargs)
#             # return True
#         else:
#             raise PermissionDenied


class CheckEditorGroupMixin(UserPassesTestMixin,LoginRequiredMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="editor") or self.request.user.is_superuser