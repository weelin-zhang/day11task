#_*_coding:utf-8_*_
'''
Created on 2016年11月26日

@author: ZWJ
'''
from django import template
from django.utils.safestring import mark_safe
from django.template.base import  Node, TemplateSyntaxError
register = template.Library()

@register.simple_tag
def get_groupnameofhost(hostobj):
    '''根据主机拿到主机所在的属组（用户组A用户组B）
    '''
    return hostobj.usergroup.groupname

@register.simple_tag
def get_groupnameofuser(userobj):
    '''根据用户拿到用户所在的属于组（用户组A、用户组B）
    '''
    tmp_l=[]
    for group in userobj.usergroup_set.all():
        tmp_l.append(group.groupname)
    return '/'.join(tmp_l)

@register.simple_tag
def get_usertype(userobj):
    '''根据用户拿到用户类型
    '''
    return userobj.usertype.name