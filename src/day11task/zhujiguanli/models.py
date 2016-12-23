#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        label = u'这个对象包含(%s)'%(self.name)
        #return label
        return self.name


class User(models.Model):
    username = models.CharField(max_length=50,null=False)
    password = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=50,null=False)
    phone = models.CharField(max_length=11,null=False)
    create_date = models.DateTimeField(auto_now_add=True,null=False)
    update_date = models.DateTimeField(auto_now=True,null=False)
    usertype = models.ForeignKey(UserType)
    def __unicode__(self):
        label = u'这个对象包含(%s,%s,%s)'%(self.username,self.email,self.phone)
        return label
    
class UserGroup(models.Model):
    groupname = models.CharField(max_length=20,null=False)
    users = models.ManyToManyField(User)
    def __unicode__(self):
        label = u'这个对象包含(%s)'%(self.groupname)
        #return label
        return self.groupname
   
class Asset(models.Model):
    hostname = models.CharField(max_length=256)
    ip = models.GenericIPAddressField()
    usergroup = models.ForeignKey(UserGroup)
    
    #默认状态打印asset对象返回Asset Object
    #此处可以定制
    def __unicode__(self):
        label = u'这个对象包含(%s,%s)'%(self.hostname,self.ip)
        #return label
        return self.hostname
    