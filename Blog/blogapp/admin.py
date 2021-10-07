from django.contrib import admin
from .models import Post,Category,Comment
# Register your models here.

# admin.site.register(Post)
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display=['id','title','author','publish_date','category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']

    
admin.site.register(Comment)
    