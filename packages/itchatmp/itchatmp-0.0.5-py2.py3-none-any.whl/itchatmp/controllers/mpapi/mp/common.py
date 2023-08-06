from itchatmp.config import SERVER_URL
from itchatmp.returnvalues import ReturnValue
from itchatmp.server import WechatServer
from itchatmp.utils import retry
from ..base.common import (update_access_token_producer,
    access_token_producer, filter_request_producer)
from ..requests import requests

__all__ = ['update_access_token', 'access_token', 'get_server_ip', 'filter_request', 'clear_quota']

server = WechatServer(None, None, None)

update_access_token = update_access_token_producer(
    SERVER_URL + '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s',
    lambda x: x.config.appId)

access_token = access_token_producer(update_access_token)

def get_server_ip():
    @retry(n=3, waitTime=3)
    @access_token
    def _get_server_ip(accessToken=None):
        url = '%s/cgi-bin/getcallbackip?access_token=%s' % \
            (SERVER_URL, accessToken)
        r = requests.get(url).json()
        if 'ip_list' in r:
            r['errcode'] = 0
            for i, v in enumerate(r['ip_list']):
                r['ip_list'][i] = v[:v.rfind('/')]
        return ReturnValue(r)
    return _get_server_ip()

filter_request = filter_request_producer(get_server_ip)

@retry(n=3, waitTime=3)
@access_token
def clear_quota(accessToken=None):
    data = {'appid': server.config.appId}
    r = requests.post('%s/cgi-bin/clear_quota?access_token=%s' %
        (SERVER_URL, accessToken), data=data).json()
    return ReturnValue(r)
