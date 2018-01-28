from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from app.models import AccessToken, User
from rest_framework import viewsets
from app.serializers import CoreTokenSerializer
import requests
import json
import time
# from app.models import

# 使用之前需要修改下面的app_id 和 app_secret
appid = 'wx05429a8ee93be82d'
appsecret = '5012ec05c9c049bcfed217767e635efa'
# grant_type = 'client_credential'
# Create your views here.


# @get_access_token
def index(request):
    # code = request.GET.get('code')
    # state = request.GET('state')
    return HttpResponse('hello world')


def auth(request):
    # 微信网页授权跳转页，获取code，同时发出auth_access_token请求并更新
    # 注意：正式环境不管是否关注公众号都可以返回code，//没考虑没关注公众号情况，默认都是关注了公众号
    next_host = request.get_host()
    next_url = request.path  # 重定向的路径
    state = request.GET.get('state')  # 根据state判断取哪一页
    code = request.GET.get('code')
    get_auth_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'
    params = {
        'appid': appid,
        'secret': appsecret,
        'code': code,
        'grant_type': 'authorization_code',
    }
    r = requests.get(get_auth_access_token_url, params=params)
    """
        正确时的格式
        { "access_token":"ACCESS_TOKEN",
        "expires_in":7200,
        "refresh_token":"REFRESH_TOKEN",
        "openid":"OPENID",
        "scope":"SCOPE" }
    """
    res = r.json()
    if 'errcode' in res:  # 判断是否有问题
        request_error = 'True'
    elif 'errcode' not in res:
        request_error = 'False'
        user_list = fetch_user_list()  # 获取公众号用户清单
        if res.get('openid') in fetch_user_list():  # 从公众号后台获取用户列表判断是否在列表里，并获取详细信息
            get_userinfo_url = 'https://api.weixin.qq.com/cgi-bin/user/info'
            openid = res.get('openid')
            get_userinfo_params = {
                'access_token': get_access_token(),
                'openid': res.get('openid'),
                'lang': 'zh_CN',
            }
            userinfo = requests.get(
                get_userinfo_url, params=get_userinfo_params).json()
            print(json.dumps(userinfo))
            print('this is our client')
        else:
            print('user %s is not our client' %
                  openid)  # 默认只有关注了才能继续往下，后期加上提示页
        if User.objects.filter(openid=userinfo.get('openid')).exists():
            #查看数据库是否有值
            # 判断access_token是否过期
            if int(time.time()) < int(User.objects.filter(openid=userinfo.get('openid')).get().user_access_time):
                #没有过期，下一步操作
                pass
            else:# 过期了，更新user_access_token
                refresh_token_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
                refresh_token_params = {
                        'appid': appid,
                        'refresh_token': res.get('refresh_token'),
                        'grant_type': 'refresh_token',
                    }
                refresh_token_results = requests.get(refresh_token_url, params=refresh_token_params).json()
                user_db = User.objects.filter(openid=userinfo.get('openid'))
                user_db.user_access_token = refresh_token_results.get('access_token')
                user_db.user_access_time = int(time.time()) + 7000 # 刷新过期时间
            #数据库没有值，插入数据
        else:
            add_user = User(
                # subcribe=str(userinfo.get('subscribe')),
                openid=userinfo.get('openid'),
                nickname=userinfo.get('nickname'),
                user_sex=str(userinfo.get('sex')),
                user_city=userinfo.get('city'),
                user_country=userinfo.get('country'),
                user_province=userinfo.get('province'),
                user_subscribe_time=userinfo.get('subscribe_time'),
                user_access_token=res.get('access_token'),
                user_access_time= int(time.time()) + 7000,
                user_refresh_token=res.get('refresh_token'),
                user_refresh_time= int(time.time()) + 2592000,
            )
            add_user.save()
            print('inserting to db...')
            # # else:  # 查询数据库User表，是否已存
            #     try:
            #         User.objects.get(openid=res.get('openid'))  # 可以查出来就跳过
            #         # if                              # 查看access_token是否过期
            #         # print('in db')

            #         # refresh_token
            #         # https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN
            #         refresh_token_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
            #         refresh_token_params = {
            #             'appid': appid,
            #             'refresh_token': res.get('refresh_token'),
            #             'grant_type': 'refresh_token',
            #         }
            #         refresh_access_token_info = requests.get(
            #             refresh_token_url, params=refresh_token_params).json()
            #     except:
            #         print('not in db, now inserting ...')  # 查不出来则新增插入数据
            #         save_user = User(
            #             openid=userinfo.get('openid'),
            #             subscribe=str(userinfo.get('subscribe')),
            #             nickname=userinfo.get('nickname'),
            #             # user_sex=str(userinfo.get('sex')),
            #             user_city=userinfo.get('city'),
            #             user_country=userinfo.get('country'),
            #             user_province=userinfo.get('province'),
            #             # user_subscribe_time=userinfo.get('subscribe_time'),
            #             user_access_token=res.get('access_token'),
            #             # user_access_time=int(time.time()) + 7000,  # 2小时过期
            #             user_refresh_token=res.get('access_token'),
            #             # user_refresh_time=int(time.time()) + 2590000,  # 30天过期
            #         )

            # return HttpResponse('there is %s,the next_host is %s,the access code is %s and the state is %s, and the next_url is %s, and the json is %s'
            #         % (request_error,next_host,code, state, next_url, json.dumps(res)))
    return HttpResponse('user_info is %s and the access token is %s ' % (json.dumps(userinfo),json.dumps(res)))


def get_access_token():
    access_url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': appsecret,
    }
    if AccessToken.objects.all().values().exists():  # 判断数据库是否有值
        token_info = AccessToken.objects.all().values().get()
        print('there is access_token in db')
        # 计算access_token是否过期
        if (int(time.time()) < token_info['expire_in']):
            # 已存在，没过期，直接返回，如果出错可能因为没有做校验，用了别的appid等
            print('old_access_token %s ' % token_info['access_token'])
            return token_info['access_token']
        else:  # 已存在，过期，重新获取，更新
            r = requests.get(access_url, params=params)
            res = r.json()
            access_token_modify = AccessToken.objects.get(id=1)
            access_token_modify.access_token = res.get('access_token')
            access_token_modify.expire_in = int(time.time()) + 7000
            access_token_modify.save()
            print('new access token %s ' % access_token_modify.access_token)
            return access_token_modify.access_token
    else:  # 数据库没有值，插入一条记录
        r = requests.get(access_url, params=params)
        res = r.json()
        access_token_create = AccessToken(access_token=res.get(
            'access_token'), expire_in=int(time.time()) + 7000)
        access_token_create.save()
        return access_token_create.access_token


def fetch_user_list():
    access_url = 'https://api.weixin.qq.com/cgi-bin/user/get?'
    access_token = get_access_token()
    next_openid = ''
    params = {
        'access_token': access_token,
        'next_openid': next_openid,
    }
    r = requests.get(access_url, params=params)
    res = r.json()
    return res.get('data').get('openid')


# def user_refresh():
#     # 关注和取消关注事件触发本方法
#     pass


class TokenViewSet(viewsets.ModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = CoreTokenSerializer
