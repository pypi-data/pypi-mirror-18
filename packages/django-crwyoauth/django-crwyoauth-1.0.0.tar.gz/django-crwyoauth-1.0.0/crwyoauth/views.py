# encoding=utf-8
import urllib
import urllib2
import json
import re
from django.conf import settings
from django.apps import apps
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login
from .models import CrwyoauthConfig

# Create your views here.

User = apps.get_model(settings.AUTH_USER_MODEL)


def get_oath_config(oauth_to):
    res = {}
    config = CrwyoauthConfig.objects.get(oauth_to=oauth_to)
    res['CLIENT_ID'] = config.client_id
    res['CLIENT_SECRET'] = config.client_secret
    res['CALL_BACK'] = config.call_back
    return res


class GithubOauthView(RedirectView):
    permanent = False
    url = None

    def get_access_token(self):
        code = self.request.GET.get('code')
        res = get_oath_config('GITHUB')
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': res.get('CLIENT_ID'),
            'client_secret': res.get('CLIENT_SECRET'),
            'code': code,
            'redirect_uri': res.get('CALL_BACK'),
        }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers={'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        result = response.read()
        result = json.loads(result)
        return result

    def get_user_info(self, access_token):
        url = 'https://api.github.com/user?access_token=%s' % access_token
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html)
        username = str(data['id']) + '-github_oauth'
        nickname = data['login']
        head_oauth_avatar = data['avatar_url']
        email = str(data['id']) + '@github-oauth.com'
        password = '********'
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, email, password)
            user.nickname = nickname
            user.head_oauth_avatar = head_oauth_avatar
            user.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.GET.get('state')
        try:
            access_token_info = self.get_access_token()
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except ImportError:
            pass
        return super(GithubOauthView, self).get_redirect_url(*args, **kwargs)


class SinaOauthView(RedirectView):
    permanent = False
    url = None

    def get_access_token(self):
        code = self.request.GET.get('code')
        res = get_oath_config('SINA')
        url = 'https://api.weibo.com/oauth2/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': res.get('CLIENT_ID'),
            'client_secret': res.get('CLIENT_SECRET'),
            'code': code,
            'redirect_uri': res.get('CALL_BACK'),
        }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers={'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        result = response.read()
        result = json.loads(result)
        return result

    def get_user_info(self, access_token, uid):
        # 获取对应uid用户信息
        url = 'https://api.weibo.com/2/users/show.json?access_token=%s&uid=%s' % (access_token, uid)
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html)
        username = str(uid) + '-sina_oauth'
        nickname = data['name']
        head_oauth_avatar = data['avatar_hd']
        email = str(uid) + '@sina-oauth.com'
        password = '********'
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, email, password)
            user.nickname = nickname
            user.head_oauth_avatar = head_oauth_avatar
            user.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.GET.get('state')
        try:
            access_token_info = self.get_access_token()
            access_token = access_token_info['access_token']
            uid = access_token_info['uid']
            self.get_user_info(access_token, uid)
        except ImportError:
            pass
        return super(SinaOauthView, self).get_redirect_url(*args, **kwargs)


# QQ api 在获取access_token时，返回的为urlencode类型数据
# access_token=FE04************************CCE2&expires_in=7776000&refresh_token=88E4************************BE14
# QQ api 在获取openid时，返回的为带callback字样的数据
# callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
# QQ api 在获取access_token时，返回的为json类型数据


class TencentOauthView(RedirectView):
    permanent = False
    url = None

    def get_access_token(self):
        # 获取access_token
        code = self.request.GET.get('code')
        res = get_oath_config('QQ')
        url = 'https://graph.qq.com/oauth2.0/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': res.get('CLIENT_ID'),
            'client_secret': res.get('CLIENT_SECRET'),
            'code': code,
            'redirect_uri': res.get('CALL_BACK'),
        }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers={'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        tmp = response.read()
        result = {}
        tmp = tmp.split("&")[0]
        result['access_token'] = tmp.split("=")[1]
        # 正则匹配json数据部分
        # result = re.search("\{.*\}", result).group()
        # result = json.loads(result)
        return result

    def get_openid(self, access_token):
        # 获取openid
        url = 'https://graph.qq.com/oauth2.0/me?access_token=%s' % access_token
        response = urllib2.urlopen(url)
        html = response.read()
        # 正则匹配json数据部分
        html = re.search("\{.*\}", html).group()
        result = json.loads(html)
        return result

    def get_user_info(self, access_token, oauth_consumer_key, openid):
        # 获取用户信息
        url = 'https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s' % (access_token, oauth_consumer_key, openid)
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html)
        username = str(openid) + '-qq_oauth'
        nickname = data['nickname']
        head_oauth_avatar = data['figureurl']
        email = str(openid) + '@qq-oauth.com'
        password = '********'
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, email, password)
            user.nickname = nickname
            user.head_oauth_avatar = head_oauth_avatar
            user.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.GET.get('state')
        try:
            access_token_info = self.get_access_token()
            access_token = access_token_info['access_token']
            openid_info = self.get_openid(access_token)
            openid = openid_info['openid']
            oauth_consumer_key = get_oath_config('QQ').get('CLIENT_ID')
            self.get_user_info(access_token, oauth_consumer_key, openid)
        except ImportError:
            pass
        return super(TencentOauthView, self).get_redirect_url(*args, **kwargs)
