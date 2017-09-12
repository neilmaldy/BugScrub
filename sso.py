import requests
# import pdb
from lxml.html import fromstring
import urllib.parse


def get_authenticated_session(user, passwd, env='prod'):
    '''

    :param user: SSO username
    :param passwd: Password
    :param env: Optional parameter defining the environment (prod or stage)
    :return: requests Session object
    '''
    if env == 'stage':
        get_url = 'https://mysupport-stg.netapp.com/myautosupport/ManualAsupUpload.html'
        post_url = 'https://signin-stage.netapp.com/netapp_action.html'
        user_key = 'user'
    elif env == 'prod':
        # get_url = 'https://signin.netapp.com/oamext/login.html'
        get_url = 'https://smartsolve.netapp.com'
        post_url = 'https://login.netapp.com/oam/server/auth_cred_submit'
        user_key = 'username'

    sess = requests.Session()
    resp = sess.get(get_url, allow_redirects=True)
    urldata = urllib.parse.urlparse(resp.url)
    action = '/oam/server/auth_cred_submit'

    root = fromstring(resp.text)
    form_list = root.xpath('//form')
    if len(form_list) == 1:
        action = form_list[0].attrib.get('action')


    post_url = '{scheme}://{host}{path}'.format(scheme=urldata.scheme, host=urldata.netloc,
                                                 path=action)
    data = {
        'action': 'login',
        'password': passwd,
        'presevationdata': '',
        'user': user,
        'username': user,
    }

    sess.post(post_url, data=data)
    resp2 = sess.get(get_url)
    if '<title>NetApp Login Page</title>' in resp2.text:
        return None
    else:
        return sess
