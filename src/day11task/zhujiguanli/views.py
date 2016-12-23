#_*_coding:utf-8_*_
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from models import User,UserGroup,UserType,Asset
from forms import RegisterUserForm,LoginForm

from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
# Create your views here.


#搞一个装饰器

def checkLogin(func):
    
    def wrapper(request,*args,**kwargs):
        if not request.session.get('is_login',None):
            print 'no logined'
            return redirect('/zhujiguanli/login')
        return func(request,*args,**kwargs)
    return wrapper

'''
    @csrf_protect，为当前函数强制设置防跨站请求伪造功能，即便settings中没有设置全局中间件。
    @csrf_exempt，取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
'''
#@csrf_exempt
#@csrf_protect
def login(request,*args,**kwargs):
    print 'views middleware process test'
    loginform = LoginForm()
    ret = {'status':'','form':loginform}
    if request.method == 'POST':
        resultform = LoginForm(request.POST)
        if resultform.is_valid():
            result_dict=resultform.clean()
            count = User.objects.filter(username=result_dict['username'],password=result_dict['password']).count()
            if count == 1:
                #设置session
                request.session['is_login'] = {'user':result_dict['username'],'login':True}
                return redirect('/zhujiguanli/index/')
            else:
                ret['form']=resultform
                ret['status']='用户名或密码错误'
        else:
            ret['form']=resultform
            ret['status'] = resultform.errors.as_data().values()[0][0].messages[0]
            print ret['status']
    return render(request,'login.html',ret)    

@checkLogin
def user(request,*args,**kwargs):
    groupobj = UserGroup.objects.get(id=1)
    print groupobj.users.all().get(id=12)
    print groupobj.users.get(id=12)#同上
    print groupobj.users.all().filter(id=12)
    print groupobj.users.filter(id=12)#同上
    return redirect('/zhujiguanli/deleteuser/')

@checkLogin
def usertype(request,*args,**kwargs):
    
    data = UserType.objects.all()
    if request.method == 'POST':
        formdata = request.POST
        if 'delete' not in formdata:
            usertypename = request.POST.get('usertype',None)
            not_empty=all([usertypename])
            if not_empty:
                #1.检查是否已经有了这个usertype
                reCount = UserType.objects.filter(name=usertypename).count()
                print reCount
                if reCount == 1:
                    print '已经有了'
                    return render_to_response('usertype.html',{'usertypes':data,'status':'group已经存在'})
                else:
                    #2.存到数据库中
                    try:
                        UserType.objects.create(name = usertypename)
                        data = UserType.objects.all()
                        return render_to_response('usertype.html',{'usertypes':data,'status':'添加成功'})
                    except Exception as e:
                        print e
                        return render_to_response('usertype.html',{'usertypes':data,'status':'添加失败请重试..'})
            else:
                    return render_to_response('usertype.html',{'usertypes':data,'status':'usertype不能为空..'})
        
        #删除逻辑
        usertype_id = formdata['delete']
        #判断usertype是否有用户
        usertypeobj = UserType.objects.filter(id=usertype_id)[0]
        usercount = usertypeobj.user_set.all().count()
        if usercount:
            print usercount
            return render_to_response('usertype.html',{'usertypes':data,'deletestatus':'存在属于该组的用户'})
        UserType.objects.filter(id=usertype_id)[0].delete()
        data = UserType.objects.all()
        return render_to_response('usertype.html',{'usertypes':data,'deletestatus':'update success'})
        
        
    else:
        return render_to_response('usertype.html',{'usertypes':data})

@checkLogin  
def group(request,*args,**kwargs):
    data = UserGroup.objects.all()
    if request.method == 'POST':
        formdata = request.POST
        if 'delete' not in formdata:
            groupname = request.POST.get('groupname',None)
            not_empty=all([groupname])
            if not_empty:
                #1.检查是否已经有了这个username
                reCount = UserGroup.objects.filter(groupname=groupname).count()
                print reCount
                if reCount == 1:
                    print '已经有了'
                    return render(request,'groupmanger.html',{'groups':data,'status':'group已经存在'})
                else:
                    #2.存到数据库中
                    try:
                        UserGroup.objects.create(groupname = groupname)
                        data = UserGroup.objects.all()
                        return render(request,'groupmanger.html',{'groups':data,'status':'添加成功'})
                    except Exception as e:
                        print e
                        return render(request,'groupmanger.html',{'groups':data,'status':'添加失败请重试..'})
            else:
                    return render(request,'groupmanger.html',{'groups':data,'status':'groupname不能为空..'})
        
        #删除逻辑
        groupobj_id = formdata['delete']
        #判断组内是否有用户and 主机
        groupobj = UserGroup.objects.filter(id=groupobj_id)[0]
        usercount = groupobj.users.all().count()
        hostscount = groupobj.asset_set.all().count()
        if usercount or hostscount:
            print 'usersnum:',usercount,'hostsnum:',hostscount
            return render(request,'groupmanger.html',{'groups':data,'deletestatus':'存在属于该组的用户或主机..不可删除'})
        UserGroup.objects.filter(id=groupobj_id)[0].delete()
        data = UserGroup.objects.all()
        return render(request,'groupmanger.html',{'groups':data,'deletestatus':'update success'})
        
        
    else:
        return render(request,'groupmanger.html',{'groups':data})

@checkLogin
def host(request,*args,**kwargs):
    usergroups = UserGroup.objects.all()
    data = Asset.objects.all()
#    1.根据外键的值获取asset中所有外键等于此外键的asset对象(一对多),
#     assets = Asset.objects.filter(usergroup=1)#等价下面
#     #assets = Asset.objects.filter(usergroup__groupname='用户组A') #跨表双下划线   
#     for asset in assets:
#         print asset
#         print asset.hostname,asset.ip,asset.usergroup.groupname

#    2.根据给定的用户，获取该用户所有的属于(user与group多对多)
#     testuserobj = User.objects.filter(id=12)[0]
#     for i in testuserobj.usergroup_set.all():
#         print u'用户组:',i
#         print u'用户:%s属于:%s'%(testuserobj.username,i.groupname)
        
#    3.根据给定的group，获取该用户组所有的用户(user与group多对多)第一个 用户组(id=1)
#     testgroupobj = UserGroup.objects.filter(id=1)[0]
#     for i in testgroupobj.users.all():
#         print u'用户:',i
#         print u'%s所属用户组:%s'%(i.username,testgroupobj.groupname)
    if request.method == 'POST':
        formdata = request.POST
        if 'del' not in formdata:#ajax
            hostname = request.POST.get('hostname',None)
            ip = request.POST.get('ip',None)
            not_empty=all([hostname,ip])
            if not_empty:
                #1.检查是否已经有了这个hostname
                reCount = Asset.objects.filter(hostname=hostname).count()
                if reCount == 1:
                    print '已经有了'
                    return render(request,'hostmanger.html',{'usergroups':usergroups,'hosts':data,'status':'主机已经存在'})
                groupid = request.POST.get('usergroup',None)
                groupobj = UserGroup.objects.filter(id=groupid)[0]
                print hostname,ip,groupobj.groupname
                #2.存到数据库中
                try:
                    Asset.objects.create(hostname = hostname,ip = ip,usergroup=groupobj)
                    data = Asset.objects.all()
                    return render(request,'hostmanger.html',{'usergroups':usergroups,'hosts':data,'status':'添加成功'})
                except Exception as e:
                    print e
                    return render(request,'hostmanger.html',{'usergroups':usergroups,'hosts':data,'status':'添加失败请重试..'})
            else:
                    return render(request,'hostmanger.html',{'usergroups':usergroups,'hosts':data,'status':'hostname或ip不能为空..'})
    
        #删除业务ajax
        else:#ajax
            hostobj_id_str = formdata['del']#'4-6'
            if hostobj_id_str:
                hostobj_id_l=hostobj_id_str.split('-')
                print 'str',hostobj_id_l
            else:#空
                ajaxresponse={'failajax':'没有选择任何dongdong...'}
                return HttpResponse(json.dumps(ajaxresponse))
            for id in hostobj_id_l:
                id=int(id)
                Asset.objects.filter(id=id)[0].delete()
            data = Asset.objects.all()
            ajaxresponse={'successajax':'nice...waiting to be refresh'}
            return HttpResponse(json.dumps(ajaxresponse))
    else:
        return render(request,'hostmanger.html',{'usergroups':usergroups,'hosts':data})

def index(request,*args,**kwargs):
    
    user_dict = request.session.get('is_login',None)
    
    if user_dict:
        
        return render_to_response('index.html',{'user':user_dict['user']})

    return redirect('/zhujiguanli/login/')

@checkLogin
def showuser(request,groupid):
    if groupid != 'all':
        try:
            groupobj = UserGroup.objects.get(id=int(groupid))
        except:
            return HttpResponse('no the groupid')
        #拿到groupid对应的users
        userobjs = groupobj.users.all()
    else:
        userobjs = User.objects.all()
    for user in userobjs:
        print user.username,user.phone,user.email,groupid
#         for i in user.user_group.all():
#             print i.id,i.groupname
    #print groupobj.groupname,userobjs[0].username
    if userobjs:
        return render_to_response('userlist.html', {'data':userobjs,'groupid':groupid})
    return render_to_response('userlist.html',{'data':None,'groupid':groupid })

@checkLogin
def adduser(request,*args,**kwargs):
    status=''
    adduserform = RegisterUserForm()
    try:
        if request.method == 'POST':
            print 'ok'
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            group_l = []
            if request.POST.get('admin1'):group_l.append(1)
            if request.POST.get('admin2'):group_l.append(2)
            if request.POST.get('admin3'):group_l.append(3)
            
            User.objects.create(username=username,password=password,email=email,phone=phone)
            userobj = User.objects.get(username=username)
            for i in group_l:
                groupobj = UserGroup.objects.get(id=i)
                userobj.user_group.add(groupobj)
            status = 'add user success!'
            return render_to_response('adduser.html', {'form':adduserform,'status':status})
    except:
        status='add user fail!'
        return render_to_response('adduser.html', {'form':adduserform,'status':status})
    else:
        return render_to_response('adduser.html',{'form':adduserform})

@checkLogin
def deleteuser(request,groupid):
    if groupid != '':#分组显示
        try:
            groupobj = UserGroup.objects.get(id=int(groupid))
        except:
            return HttpResponse('不存在这个groupid')
        userobjs = groupobj.users.all()
        print userobjs
    else:userobjs = User.objects.all()
    #处理提交结果    
    if request.method == 'POST':
        data = request.POST#拿到对象的字典
        for user in userobjs:
            if user.username in data:
                #delete user of username
                User.objects.filter(id=data[user.username]).delete()
        if groupid != '':#分组显示
            groupobj = UserGroup.objects.get(id=groupid)
            print groupobj.groupname,groupobj.id
            userobjs = groupobj.user_set.all()
        else:userobjs = User.objects.all()  
        return render(request,'userlist_delete.html',{'data':userobjs,'groupid':groupid})
    return render(request,'userlist_delete.html',{'data':userobjs,'groupid':groupid})


def register(request,*args,**kwargs):
    usergroups = UserGroup.objects.all()
    usertypes = UserType.objects.all()
    registerform = RegisterUserForm()
    ret={'form':registerform,'status':'','usergroups':usergroups,'usertypes':usertypes,'checkuserstatus':''}
    if request.method == 'POST':
        #检查是否已经注册过(ajax)
        ajax_username = request.POST.get('in_name',None)
        #有输入才处理
        if ajax_username and len(ajax_username.strip()) >= 6:
            print 'ajax check username:',json.dumps(ajax_username)
            if User.objects.filter(username=ajax_username).count():
                ajax_response={'checkuserstatus':'用户已存在,重新输入'}
                return HttpResponse(json.dumps(ajax_response))
            else:ajax_response={'checkuserstatus':'用户名有效'};return HttpResponse(json.dumps(ajax_response))
        ajax_response={'checkuserstatus':'长度不够至少6位'}
        
        return HttpResponse(json.dumps(ajax_response))
        username_input = request.POST.get('username',None)
        if not username_input:
            ret['status'] = '请重新输入用户名...'
            return render_to_response('register.html',ret)
        checkform = RegisterUserForm(request.POST)
        if checkform.is_valid():
            result_dict=checkform.clean()
            print 'result:',result_dict#result: {'username': u'testtest', 'phone': u'11111111111', 'password': u'testtest', 'email': u'test1@qq.com'}
            #检查是否存在此用户名
            usernameinput = result_dict['username']
            if User.objects.filter(username=usernameinput).count():
                print '已经存在'
                ret['status'] = '用户名存在'
                return render(request,'register.html',ret)
            #--不存在这个username
            #拿到用户类型对象
            usertypeobj = UserType.objects.get(id=request.POST['usertype'])
            try:
                userobj = User.objects.create(username = username_input,password=result_dict['password'],email = result_dict['email'],phone = result_dict['phone'],usertype=usertypeobj)
                print userobj
                #添加多对多关系
                flag = False                
                for groupobj in usergroups:
                    if groupobj.groupname in request.POST:#用户组的id在POST数据中（key）
                        groupobj.users.add(userobj)
                        flag=True
                if not flag:UserGroup.objects.get(id=1).users.add(userobj)
                ret['form'] = registerform
                ret['status'] = '添加成功'
                return render(request,'register.html',ret)
            except Exception as e:
                print e
                ret['status'] = '添加失败'
                ret['form'] = checkform
                return render(request,'register.html',ret)
        else:#form格式不对
            ret['form'] = checkform
            ret['status']=checkform.errors.as_data().values()[0][0].messages[0]
            return render(request,'register.html',ret)
    else:
        return render(request,'register.html',ret)

@checkLogin
def hostupdate(request,*args,**kwargs):
    hostid=kwargs['hostid']
    hostobj=Asset.objects.filter(id=int(hostid))[0]
    groups=UserGroup.objects.all()
   
    if request.method=="GET":
        return render(request,'hostupdate.html',{'hostobj':hostobj,'usergroups':groups})
    else:
        update_dict=request.POST
        
        if hostobj.hostname==update_dict['hostname'] and hostobj.ip==update_dict['ip'] and hostobj.usergroup==UserGroup.objects.filter(id=update_dict['usergroup'])[0]:
            print 'p'
            return render(request,'hostupdate.html',{'hostobj':hostobj,'usergroups':groups,'status':'逗我'})
        hostobj.hostname=update_dict['hostname']
        hostobj.ip=update_dict['ip']
        usergroupobj=UserGroup.objects.filter(id=update_dict['usergroup'])[0]
        hostobj.usergroup=usergroupobj
        hostobj.save()
        return redirect('/zhujiguanli/host/')

@checkLogin
def groupupdate(request,*args,**kwargs):
    groupid=kwargs['groupid']
    groupobj=UserGroup.objects.filter(id=int(groupid))[0]
    if request.method=="GET":
        return render(request,'groupupdate.html',{'groupobj':groupobj})
    else:
        #判断是否有用户和主机
        contain_users_num=groupobj.users.all().count()
        contain_host_num=groupobj.asset_set.all().count()
        print 'num;',contain_users_num,'host',contain_host_num
        if contain_users_num or contain_host_num:return render(request,'groupupdate.html',{'groupobj':groupobj,'status':'存在跟这个组关联的用户或主机，不可更改'})
        
        
        update_dict=request.POST
        
        if groupobj.groupname==update_dict['groupname']:return render(request,'groupupdate.html',{'groupobj':groupobj,'status':'逗我?'})
        
        groupobj.groupname=update_dict['groupname']
        groupobj.save()
        return redirect('/zhujiguanli/group/')
@checkLogin         
def logout(request,*args,**kwargs):
    
    del request.session['is_login']
    
    return redirect('/zhujiguanli/login/')