from django.shortcuts import render, HttpResponse
import json
from oauthServer import models as oauthM
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from oauthServer.Tools import Tools
import time,datetime

# Create your views here.
def server(request):
    # response = HttpResponse(json.dumps(request))
    # response["Access-Control-Allow-Origin"] = "*"
    datas = ""
    response_type = ''
    client_id = ''
    redirect_uri = ''
    scope = ''
    state = ''
    authCode = ''
    url = ''
    try:
        if request.method == 'GET':
            #确定'response_type'和'client_id'必须有值
            if (request.GET.get('response_type') != None) & (request.GET.get('client_id') != None):
                #根据'response_type'筛选授权类型(4种)
                if request.GET.get('response_type') == 'code':
                    response_type = request.GET['response_type']
                    client_id = request.GET['client_id']
                    redirect_uri = request.GET['redirect_uri']
                    scope = request.GET['scope']
                    state = request.GET['state']
                    # authCode = Tools.auto_auth_code()
                    # extime = datetime.datetime.now
                    # url = redirect_uri + "?code=" + authCode + "&state=" + state
                    # host = oauthM.Host.objects.create()
                    # oauthM.Authcode_log.objects.create(
                    #     host=client_id, response_type=response_type, client_id=client_id, redirect_uri=redirect_uri, scope=scope, state=state, auth_code=authCode, extime=extime)
                    # return HttpResponse('add(ok).')
                elif request.GET.get('response_type') == 'token':
                    pass
                elif request.GET.get('response_type') == 'password':
                    pass
                elif request.GET.get('response_type') == 'clientcredentials':
                    pass
                else:
                    pass
            #'response_type'和'client_id'无值情况
            else:
                pass
    except Exception as e:
        print(e)
    return render(request, 'server.html', locals())

#登录
def do_login(request):
    #try:
    username = ''
    password = ''
    response_type = ''
    client_id = ''
    redirect_uri = ''
    scope = ''
    state = ''
    authCode = ''
    url = ''
    if request.method == 'GET':
        if (request.GET.get('username') != None) & (request.GET.get('password') != None):
            username = request.GET['username']
            password = request.GET['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                return HttpResponse(request.user.first_name)
            else:
                return HttpResponse('no user auth(get).')
        else:
            return HttpResponse('have no user')
    elif request.method == 'POST':
        postData = json.loads(request.body)
        if (postData.get('username') != None) & (postData.get('password') != None):
            username = postData.get('username')
            password = postData.get('password')
            response_type = postData.get('response_type')
            client_id = postData.get('client_id')
            redirect_uri = postData.get('redirect_uri')
            scope = postData.get('scope')
            state = postData.get('state')
            authCode = Tools.auto_auth_code()
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                host = oauthM.Host.objects.create(
                    client_id=client_id, host_ip='192.168.10.18', active_time=int(time.time()), user_id=request.user.id)
                host.save()
                oauthM.Authcode_log.objects.create(host=host, response_type=response_type,
                                                   redirect_uri=redirect_uri, scope=scope, state=state, auth_code=authCode, exptime=int(time.time()+600000))
                jsonData = {
                    'redirect_uri': redirect_uri,
                    'auth_code': authCode,
                    'state':state,
                }
                return HttpResponse(json.dumps(jsonData))
            else:
                return HttpResponse('no user auth(post).')
        else:
            return HttpResponse('have no user')
    else:
        return HttpResponse('http error')
    #except Exception as e:
        #pass



def authorize(request):
    try:
        if request.method == 'GET':
            token = ''
            jsonData = {}
            code = request.GET.get('code')
            client_id = request.GET.get('client_id')
            if (code != None) & (client_id != None):
                isClientIdEx = oauthM.Host.objects.filter(client_id=client_id).exists()
                isCodeEx = oauthM.Authcode_log.objects.filter(auth_code=code).exists()
                if isCodeEx & isClientIdEx:
                    isCodeOk = oauthM.Authcode_log.objects.filter(auth_code=code).all().values('exptime')[0]
                    isCodeOk = isCodeOk['exptime'] >= time.time()
                    if isCodeOk:
                        token = Tools.auto_hash_code()
                        print("+++")
                        print(token['refresh_token'])
                        # oauthM.Accesstoken.objects.update_or_create(
                        #     host_id=17,
                        #     is_alive='1',
                        #     access_token=token['access_token'],
                        #     exptime=int(time.time()+86400000),
                        # )
                        # oauthM.Refreshtoken.objects.update_or_create(
                        #     host_id=16,
                        #     is_alive='1',
                        #     refresh_token=token['refresh_token'],
                        #     exptime=int(time.time()+86400000),
                        # )
                        jsonData={
                            'token':token,
                            'user':'dong'
                        }
                response = HttpResponse(json.dumps(jsonData))
                response["Access-Control-Allow-Origin"] = "*"
                return response
    except Exception as e:
        print(e)
    # return HttpResponse('ok')



