#_*_coding:utf-8_*_
from django.contrib import admin

# Register your models here.
#注册和配置django admin 后台管理页面


from zhujiguanli import models

class AssetAdmin(admin.ModelAdmin):
    list_display=('hostname','ip')#在admin中现实的内容，不仅仅显示一个对象
    
    search_fields = ('hostname', 'ip')#添加搜索功能
    
    list_filter = ('hostname', 'ip')#添加快速过滤
class UserAdmin(admin.ModelAdmin):
    list_display=('username','email','phone')
    search_fields = ('username', 'phone')
    list_filter=('username','phone')
    
admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.User,UserAdmin)