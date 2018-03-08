# -*- coding: utf-8 -*-

from pywe_base import BaseWechat
from pywe_decrypt import decrypt
from pywe_storage import MemoryStorage


class MiniApp(BaseWechat):
    def __init__(self, appid=None, storage=None):
        super(MiniApp, self).__init__()
        self.appid = appid
        self.storage = storage or MemoryStorage()
        # wx.login(OBJECT), Refer: https://mp.weixin.qq.com/debug/wxadoc/dev/api/api-login.html
        # wx.getUserInfo(OBJECT), Refer: https://mp.weixin.qq.com/debug/wxadoc/dev/api/open.html#wxgetuserinfoobject
        self.JSCODE2SESSION = self.API_DOMAIN + '/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type={grant_type}'

    @property
    def sessionKey(self):
        return '{0}:sessionKey'.format(self.appid)

    def get_session_key(self, appid=None, secret=None, code=None, grant_type='authorization_code', storage=None):
        # Update storage
        self.appid = appid or self.appid
        self.storage = storage or self.storage
        # Fetch sessionKey
        session_key = '' if code else self.storage.get(self.sessionKey)
        if not session_key:
            session_key = self.get(self.JSCODE2SESSION, appid=appid, secret=secret, code=code, grant_type=grant_type).get('session_key', '')
            self.storage.set(self.sessionKey, session_key)
        return session_key

    def get_userinfo(self, appid=None, secret=None, code=None, grant_type='authorization_code', session_key=None, encryptedData=None, iv=None, storage=None):
        if not session_key:
            session_key = self.get_session_key(appid=appid, secret=secret, code=code, grant_type=grant_type, storage=storage)
        return decrypt(appId=appid, sessionKey=session_key, encryptedData=encryptedData, iv=iv)

    def get_phone_number(self, appid=None, secret=None, code=None, grant_type='authorization_code', session_key=None, encryptedData=None, iv=None, storage=None):
        if not session_key:
            session_key = self.get_session_key(appid=appid, secret=secret, code=code, grant_type=grant_type, storage=storage)
        return decrypt(appId=appid, sessionKey=session_key, encryptedData=encryptedData, iv=iv)


miniapp = MiniApp()
get_session_key = miniapp.get_session_key
get_userinfo = miniapp.get_userinfo
get_phone_number = miniapp.get_phone_number
