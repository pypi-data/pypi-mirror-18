# -*- coding: utf-8 -*-

import urllib

from crypt.WXBizMsgCrypt import WXBizMsgCrypt

from utils import HttpUtil, Util, ObjectDict
from utils import WxError


class WxBasic(object):
    """
    基本消息解析及被动回复,包含签名校验和加解密
    """
    def __init__(self, appid, appsecret, token, aes_key=None):
        """
        初始化方法
        :param appid:微信公众号appid
        :param appsecret:微信公众号appsecret
        :param token:微信公众号token
        :param aes_key:aes加解密key, 如明文传消息则不要传入此参数
        """
        self._appid = appid
        self._appsecret = appsecret
        self._token = token
        self._aes_key = aes_key

        self._is_parsed = False
        self._message = None

    def check_signature(self, query):
        """
        验证消息真实性
        :param query: url请求键值对
        :return: bool
        """
        assert self._token
        signature = query.get('signature','')
        timestamp = query.get('timestamp','')
        nonce = query.get('nonce','')
        tmp_list = [self._token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        return signature == Util.sha1(tmp_str)

    def parse_data(self, body, query=None):
        """
        解析微信发送的原始数据(http://mp.weixin.qq.com/wiki/1/6239b44c206cab9145b1d52c67e6c551.html)
        :param body: 原始响应数据,从request的body中获取
        :param query: url请求键值对,解密需要.如不需解密则忽略此参数
        注意排重:对普通消息使用msgId排重,对event消息看具体类型排重
        """
        if self._aes_key:
            assert query
            msg_sig = query.get('msg_signature', '')
            timestamp = query.get('timestamp', '')
            nonce = query.get('nonce', '')
            assert msg_sig and timestamp and nonce, 'must provide msg_signature,timestamp,nonce in query when decrypt'
            xml_data = self._decrypt_msg(body, msg_sig, timestamp, nonce)
        else:
            xml_data = body

        message_dict = {}
        for k, v in Util.xml_to_dict(xml_data).items():
            message_dict[Util.cap_lower(k)] = v
        self._message = ObjectDict(message_dict)
        self._is_parsed = True

    @property
    def message(self):
        """
        返回消息字典(对象),类型有:text,image,voice,video,shortvideo,location,news,event
        字典对象是由xml转换成的键值对,key为驼峰式,也可作为对象属性访问,如message.msgType
        微信文档(http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html)
        """
        assert self._is_parsed, 'message has not been parsed'
        return self._message

    def pack_text(self, content):
        """
        响应文本
        :param content: 响应的文本字符串
        :return: xml格式字符串
        """
        template = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''
        result = template % (self.message.fromUserName, self.message.toUserName, Util.timestamp(), content)
        return self._ensure_encrypt(result)

    def pack_image(self, media_id):
        """
        响应图片
        :param media_id: 媒体文件id
        :return: xml格式字符串
        """
        template = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[%s]]></MediaId>
                </Image>
                </xml>
            '''
        result = template % (self.message.fromUserName, self.message.toUserName, Util.timestamp(), media_id)
        return self._ensure_encrypt(result)

    def pack_voice(self, media_id):
        """
        响应声音
        :param media_id: 多媒体文件id
        :return: xml字符串
        """
        template = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                <MediaId><![CDATA[%s]]></MediaId>
                </Voice>
                </xml>
            '''
        result = template % (self.message.fromUserName, self.message.toUserName, Util.timestamp(), media_id)
        return self._ensure_encrypt(result)

    def pack_video(self, media_id, title='', description=''):
        """
        响应视频
        :param media_id: 媒体文件id
        :param title: 标题(可选)
        :param description: 描述(可选)
        :return:
        """
        template = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                <MediaId><![CDATA[%s]]></MediaId>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                </Video>
                </xml>
            '''
        result = template % (self.message.fromUserName, self.message.toUserName, Util.timestamp(), media_id, title, description)
        return self._ensure_encrypt(result)

    def pack_music(self, musicurl='', hqmusicurl='', thumb_media_id='', title='', description=''):
        """
        响应音乐
        :param musicurl: 音乐链接
        :param hqmusicurl: 高质量音乐链接，WIFI环境优先使用该链接播放音乐
        :param thumb_media_id: 缩略图的媒体id
        :param title: 标题
        :param description: 描述
        :return:xml字符串
        """
        template = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                <MusicUrl><![CDATA[%s]]></MusicUrl>
                <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
                </Music>
                </xml>
            '''
        result = template % (self.message.fromUserName, self.message.toUserName, Util.timestamp(), title, description, musicurl, hqmusicurl, thumb_media_id)
        return self._ensure_encrypt(result)

    def pack_news(self, item_list):
        """
        回复图文消息
        :param item_list: 图文消息列表,每项是一个字典:{'title':'', 'description':'', 'picurl':'', 'url':''}
        :return: xml字符串
        """
        article_count = len(item_list)
        assert article_count in range(1, 11), 'news count should be in [1,10]'
        xml_data = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>%s</ArticleCount>
                <Articles>
            ''' % (self.message.fromUserName, self.message.toUserName, Util.timestamp(), article_count)
        for item in item_list:
            item_xml = '''
                    <item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>
                ''' % (item.get('title'), item.get('description'), item.get('picurl'), item.get('url'))
            xml_data += item_xml
        xml_data += "</Articles></xml>"
        return self._ensure_encrypt(xml_data)

    def pack_transfer_kf(self):
        """回复转发到客服系统的消息"""
        template = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[transfer_customer_service]]></MsgType>
                </xml>'''
        xml_data = template % (self.message.fromUserName, self.message.toUserName, Util.timestamp())
        return self._ensure_encrypt(xml_data)

    def _ensure_encrypt(self, xml_data):
        """判断是否需要加密消息"""
        if self._aes_key:
            return self._encrypt_msg(xml_data)
        return xml_data

    def _decrypt_msg(self, xml_data, msg_sig, timestamp, nonce):
        crypt = WXBizMsgCrypt(self._token, self._aes_key, self._appid)
        ret ,decryp_xml = crypt.DecryptMsg(xml_data, msg_sig, timestamp, nonce)
        if ret:
            assert WxError, 'decrypt error, errcode_code:%s' % ret
        return decryp_xml

    def _encrypt_msg(self, xml_data):
        crypt = WXBizMsgCrypt(self._token, self._aes_key, self._appid)
        ret,encrypt_xml = crypt.EncryptMsg(xml_data, Util.generate_nonce(10))
        if ret:
            assert WxError, 'encrypt error, errcode_code:%s' % ret
        return encrypt_xml


class WxApi(object):
    """
    微信基本接口,基类,返回值为dict
    """
    BASE_URL = 'https://api.weixin.qq.com'

    def __init__(self, access_token):
        """
        传入access_token初始化对象.
        """
        self._access_token = access_token

    @staticmethod
    def request_access_token(appid, appsecret):
        """
        网络请求获取access_token
        :param appid:
        :param appsecret:
        :return: {'access_token':'', 'expires_in':3600}
        """
        url = WxApi.BASE_URL + "/cgi-bin/token?grant_type=client_credential"
        params = {'appid': appid, 'secret': appsecret}
        return HttpUtil.get(url, params)

    @property
    def access_token(self):
        """
        属性化access_token,并作检查
        """
        assert self._access_token, 'self._access_token must not be none'
        return self._access_token

    def request_jsapi_ticket(self):
        """
        网络请求jsapi_ticket
        :return: {'jsapi_ticket':'', 'expires_in':7200}
        """
        jdata = self._get('/cgi-bin/ticket/getticket?type=jsapi')
        return {'jsapi_ticket':jdata['ticket'], 'expires_in':jdata['expires_in']}

    def request_card_api_ticket(self):
        """
        网络请求card_api_ticket
        :return: {'card_api_ticket':'', 'expires_in':7200}
        """
        jdata = self._get('/cgi-bin/ticket/getticket?type=wx_card')
        return {'card_api_ticket':jdata['ticket'], 'expires_in':jdata['expires_in']}

    ##############消息API############

    def send_text(self, openid, content):
        """
        主动发送文本
        :param openid: 发送对象openid
        :param content: 发送内容
        :return:
        """
        data = {
            "touser": openid,
            "msgtype": "text",
            "text": {"content": content}
        }
        return self._send_service_msg(data)

    def send_image(self, openid, media_id):
        """
        主动发送图片
        :param openid: 发送对象openid
        :param media_id: 媒体文件id
        :return:
        """
        data = {
            "touser": openid,
            "msgtype": "image",
            "image":{"media_id": media_id}
        }
        return self._send_service_msg(data)

    def send_voice(self, openid, media_id):
        """
        主动发送声音
        :param openid: 发送对象openid
        :param media_id: 媒体文件id
        :return:
        """
        data = {
            "touser": openid,
            "msgtype": "voice",
            "voice":{"media_id": media_id}
        }
        return self._send_service_msg(data)

    def send_video(self, openid, media_id, thumb_media_id, title='', description=''):
        """
        主动发送视频
        :param openid:发送对象openid
        :param media_id:媒体ID
        :param thumb_media_id:缩略图的媒体ID
        :param title:标题(可选)
        :param description:描述(可选)
        :return:
        """
        data = {
            "touser": openid,
            "msgtype": "video",
            "video":{
                    "media_id": media_id,
                    "thumb_media_id": thumb_media_id,
                    "title": title,
                    "description": description
            }
        }
        return self._send_service_msg(data)

    def send_music(self, openid, musicurl, hqmusicurl, thumb_media_id, title='', description=''):
        """
        主动发送音乐
        :param openid: 发送对象openid
        :param musicurl: 音乐链接
        :param hqmusicurl: 高品质音乐链接
        :param thumb_media_id: 缩略图的媒体ID
        :param title: 标题(可选)
        :param description: 描述(可选)
        :return:
        """
        data = {
            "touser": openid,
            "msgtype": "music",
            "music":{
                    "title": title,
                    "description": description,
                    "musicurl": musicurl,
                    "hqmusicurl": hqmusicurl,
                    "thumb_media_id": thumb_media_id
            }
        }
        return self._send_service_msg(data)

    def send_news(self, openid, news_list):
        """
        主动发送图文消息, 最多8条，点击跳转到外链
        :param openid: 发送对象openid
        :param news_list: 图文消息列表,每一项为dict:{'url':'','picurl':'','title':'','description':''}
        :return:
        """
        assert len(news_list) in range(1, 9), 'news count should be in [1,8]'
        data = {
            "touser": openid,
            "msgtype": "news",
            "news": {
                "articles": []
            }
        }
        data['news']['article'] = news_list
        return self._send_service_msg(data)

    def send_mp_news(self, openid, media_id):
        """
        主动发送图文消息，点击跳转到图文消息页面
        :param openid: 发送对象openid
        :param media_id: 图文消息ID
        :return:
        """
        data = {
            "touser": openid,
            "msgtype": "mpnews",
            "mpnews":
                {
                    "media_id": media_id
                }
        }
        return self._send_service_msg(data)

    def send_template_msg(self, openid, template_id, data, url='', topcolor=None):
        """
        发送模板消息,
        :param openid: 发送对象openid
        :param template_id: 模板id
        :param url: 点击消息跳转url
        :param data: http://mp.weixin.qq.com/wiki/5/6dde9eaa909f83354e0094dc3ad99e05.html
        """
        data = {
            'touser': openid,
            'template_id': template_id,
            'url':url,
            'data':data
        }
        if topcolor:
            data["topcolor"] = topcolor
        return self._post('/cgi-bin/message/template/send', data)

    def add_kfaccount(self, kfaccount, nickname, password):
        """
        添加客服账号
        :param kfaccount:完整客服账号，格式为:账号前缀@公众号微信号
        :param nickname: 客服昵称
        :param password: 客服密码
        """
        data = {
             "kf_account" : kfaccount,
             "nickname" : nickname,
             "password" : Util.md5(password),
        }
        return self._post('/customservice/kfaccount/add', data)

    def update_kfaccount(self, kfaccount, nickname, password):
        """
        修改客服账号
        :param kfaccount:
        :param nickname:
        :param password:
        """
        data = {
             "kf_account" : kfaccount,
             "nickname" : nickname,
             "password" : Util.md5(password),
        }
        return self._post('/customservice/kfaccount/update', data)

    def del_kfaccount(self, kfaccount, nickname, password):
        """
        删除客服账号
        :param kfaccount:
        :param nickname:
        :param password:
        """
        data = {
             "kf_account" : kfaccount,
             "nickname" : nickname,
             "password" : Util.md5(password),
        }
        return self._post('/customservice/kfaccount/del', data)

    # def set_kfavatar(self, kfaccount, file_stream):
    #     """设置客服帐号的头像,还没实现"""
    #     raise ValueError, 'have not implement'
    #     print kfaccount

    def get_kf_list(self):
        """获取所有客服账号, return kf_list"""
        return self._get('/cgi-bin/customservice/getkflist')

    def _send_service_msg(self, data):
        url = '/cgi-bin/message/custom/send'
        return self._post(url, data)

    ############素材管理API##########

    def get_material_count(self):
        """获取素材总数"""
        return self._get('/cgi-bin/material/get_materialcount')

    def get_material_list(self, type, offset, count):
        """获取素材列表"""
        assert type in ('image', 'video', 'voice', 'news'), "type must one of them:('image', 'video', 'voice', 'news')"
        assert count in range(1, 21), 'count must in [1,20]'
        data = {
            'type':type,
            'offset':offset,
            'count':count
        }
        return self._post('/cgi-bin/material/batchget_material', data)

    def download_tmp_material(self, media_id, **kwargs):
        """
        获取临时素材(下载多媒体文件)
        kwargs is same to urlretrieve,
        :return the same to the return value of urlretrieve
        """
        url = self._final_url('/cgi-bin/media/get?media_id=%s' % media_id)
        return urllib.urlretrieve(url, **kwargs)

    def get_material(self, media_id, type, **kwargs):
        """获取永久素材"""
        params = {'media_id' : media_id}
        if type == 'news' or type == 'video':
            return self._post('/cgi-bin/material/get_material', params)
        else:
            url = self._final_url('/cgi-bin/material/get_material')
            kwargs.update(data=urllib.urlencode(params))
            return urllib.urlretrieve(url, **kwargs)

    ############用户管理API##########

    def create_group(self, name):
        """创建分组"""
        data = {"group":{"name":name}}
        return self._post('/cgi-bin/groups/create', data)

    def get_groups(self):
        """获取全部分组"""
        return self._get('/cgi-bin/groups/get')

    def get_group_by_openid(self, openid):
        """获取用户所在组"""
        return self._post('/cgi-bin/groups/getid', {'openid':openid})

    def rename_group(self, group_id, new_name):
        """重命名分组"""
        data = {"group":{"id":group_id,"name":new_name}}
        return self._post('/cgi-bin/groups/update', data)

    def move_user(self, openid, to_group_id):
        """移动/批量移动 用户到新的分组， openid为str或list"""
        if isinstance(openid, basestring):
            data = {"openid":openid,"to_groupid":to_group_id}
            return self._post('/cgi-bin/groups/members/update', data)
        elif isinstance(openid, list):
            data = {
                "openid_list":openid,
                "to_groupid":108
            }
            return self._post('/cgi-bin/groups/members/batchupdate', data)
        else:
            raise ValueError, 'openid must be string or string-list'

    def delete_group(self, group_id):
        """删除分组"""
        data = {"group":{"id":group_id}}
        return self._post('/cgi-bin/groups/delete', data)

    def remark_user(self, openid, remark):
        """设置备注名"""
        data = {'openid': openid, 'remark': remark}
        return self._post('/cgi-bin/user/info/updateremark', data)

    def get_user_info(self, openids, lang='zh_CN'):
        """获取/批量获取用户信息
        :return:user-info=list or single user-info-dict
        """
        if isinstance(openids, list):
            ldata = []
            for openid in openids:
                ldata.append({'openid':openid, 'lang':lang})
            return self._post('/cgi-bin/user/info/batchget', {'user_list':ldata}).get('user_info_list',[])
        elif isinstance(openids, basestring):
            url = '/cgi-bin/user/info?openid=%s&lang=%s' % (openids, lang)
            return self._get(url)
        else:
            raise WxError('openids must be string or list')

    def get_user_list(self, next_openid=''):
        """获取用户列表dict"""
        return self._get('/cgi-bin/user/get?next_openid=%s' % next_openid)

    ###########自定义菜单API##########

    def create_menu(self, menu_dict):
        """
        创建自定义菜单
        全部菜单:http://mp.weixin.qq.com/wiki/10/0234e39a2025342c17a7d23595c6b40a.html
        个性化菜单:http://mp.weixin.qq.com/wiki/0/c48ccd12b69ae023159b4bfaa7c39c20.html
        :param menu_dict: 字典对象,包含matchrule时是创建自定义菜单
        :return:
        """
        if 'matchrule' in menu_dict:
            return self._post('/cgi-bin/menu/addconditional', menu_dict)
        else:
            return self._post('/cgi-bin/menu/create', menu_dict)

    def get_menu(self, userid=None):
        """
        获取菜单,
        1.userid为空——查询全部菜单和个性化菜单
        2.userid不为空时获取个性化菜单匹配结果,user_id可以是粉丝的OpenID，也可以是粉丝的微信号
        :return:menu dict
        """
        if userid:
            return self._post('/cgi-bin/menu/trymatch', {'user_id': userid})
        else:
            return self._get('/cgi-bin/menu/get')

    def delete_menu(self):
        """
        删除所有菜单
        """
        return self._get('/cgi-bin/menu/delete')

    def delete_condition_menu(self, menuid):
        """
        删除个性化菜单
        :param menuid: 个性化菜单id
        """
        return self._post('/cgi-bin/menu/delconditional', {'menuid':menuid})

    ##############功能#############

    def get_wechat_ips(self):
        """获取微信服务器ip地址"""
        return self._get('/cgi-bin/getcallbackip')

    def url_long2short(self, long_url):
        """长连接转短链接,return url-string"""
        data = {'action':'long2short', 'long_url':long_url}
        return self._post('/cgi-bin/shorturl', data)

    def create_qrcode(self, action_info, expire_seconds=None):
        """生成带参数的二维码，expires-seconds为None是永久二维码, 为''时有效期30s"""
        if expire_seconds is None:
            data = {"action_name": "QR_LIMIT_SCENE", "action_info": action_info}
        else:
            if expire_seconds=='':
                expire_seconds = 30
            else:
                assert isinstance(expire_seconds, int), 'expires_seconds must be int'
            data = {"expire_seconds": expire_seconds, "action_name": "QR_SCENE", "action_info": action_info}
        return self._post('/cgi-bin/qrcode/create', data)

    ###############################

    def _get(self, url, params=None):
        return HttpUtil.get(self._final_url(url), params)

    def _post(self, url, ddata):
        final_url = self._final_url(url)
        return HttpUtil.post(final_url, ddata, ctype='json')

    def _final_url(self, url):
        new_url = WxApi.BASE_URL + url
        final_url = HttpUtil.url_update_query(new_url, access_token=self.access_token)
        return final_url


class WxMsgApi(WxApi):
    pass
class WxUserApi(WxApi):
    pass
class WxMenuApi(WxApi):
    pass

class WxAuthApi(object):
    """
    网页授权获取用户基本信息, 基于OAuth2.0协议
    (access_token,expires_in,refresh_token,openid)是一组对应信息
    """
    _AUTHORIZE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    _ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    _REFRESH_TOKEN_UEL = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
    _CHECK_TOKEN_URL = 'https://api.weixin.qq.com/sns/auth'
    _USERINFO_URL = 'https://api.weixin.qq.com/sns/userinfo'

    @classmethod
    def authorized_redirect_url(cls, redirect_uri, appid, scope='snsapi_base', state=''):
        """
        构造授权url
        :param redirect_uri: 微信会重定向到redirect_uri/?code=&state=
        :param appid: 公众号appid
        :param scope: 分为snsapi_base(只获取openid)和snsapi_userinfo(获取个人信息)两种
        :param state: 业务状态描述, 微信重定向请求会原样带上此参数
        """
        url = '%s?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' % (
            cls._AUTHORIZE_URL, appid, urllib.quote_plus(redirect_uri), scope, state
        )
        return url

    @classmethod
    def get_access_token(cls, appid, appsecret, code):
        """
        通过code换取网页授权acces_token
        :return: 返回dict. keys:access_token,expires_in,refresh_token,openid,scope
        """
        params = {'appid': appid, 'secret': appsecret, 'code':code, 'grant_type':'authorization_code'}
        return HttpUtil.get(cls._ACCESS_TOKEN_URL, params)

    @classmethod
    def refresh_access_token(cls, appid, refresh_token):
        """
        刷新auth_access_token
        :return: 返回dict, keys:access_token,expires_in,refresh_token,openid,scope
        """
        params = {'appid':appid, 'grant_type':'refresh_token', 'refresh_token':refresh_token}
        return HttpUtil.get(cls._REFRESH_TOKEN_UEL, params)

    @classmethod
    def check_access_token(cls, openid, access_token):
        """
        检验授权凭证（access_token）是否有效
        """
        params = {'access_token':access_token, 'openid': openid}
        return HttpUtil.get(cls._CHECK_TOKEN_URL, params)

    @classmethod
    def get_user_info(cls, openid, access_token, lang='zh_CN'):
        """
        拉取用户信息, snsapi_base中不需此步骤
        :return:用户信息dict
        """
        params = {'access_token': access_token, 'openid': openid, 'lang':lang}
        return HttpUtil.get(cls._USERINFO_URL, params)


class WxJsApi(object):
    """
    微信JS-API所需功能
    jsapi_ticket通过WxApi类的request_jsapi_ticket方法获取(需要access_token),有有效期,需全局存储
    """
    @classmethod
    def sign(cls, appid, jsapi_ticket, page_url):
        """
        对页面进行签名.
        网页url, 不含#之后的部分(函数内会自动过滤)
        返回{'appid':'', 'timestamp':123456789, 'nonce_str':'', 'signature':''}
        """
        params = {
            'noncestr': Util.generate_nonce(15),
            'timestamp': Util.timestamp(),
            'jsapi_ticket': jsapi_ticket,
            'url': page_url.partition('#')[0],
        }
        string = '&'.join(['%s=%s' % (key.lower(), params[key]) for key in sorted(params.keys())])
        signature = Util.sha1(string)
        return {
            'appid': appid,
            'timestamp': params['timestamp'],
            'nonce_str': params['noncestr'],
            'signature':signature
        }



if __name__ == '__main__':
    pass



