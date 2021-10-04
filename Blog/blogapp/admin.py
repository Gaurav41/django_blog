from django.contrib import admin
from .models import Post,Category
# Register your models here.

# admin.site.register(Post)
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display=['id','title','author','publish_date','category']

admin.site.register(Category)
