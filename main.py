# coding=utf-8

import urllib
import urllib2
import cookielib

import time
import hashlib

from repediy import RePediy
from cache import Cache

def get_token(s, begin='token\":\"', end='\"}}'):
    start = s.find(begin)+len(begin)
    return s[start: s.find(end, start)]

class PeDiy:

    def __init__(self, filename=''):
        self.error_message = 'Error: '
        self.headers = dict()
        self.cookie = cookielib.MozillaCookieJar()
        self.filename = filename
        if filename:
            self.cookie.load(filename, True, True)
        self.login_url = 'http://passport.kanxue.com/user-login.htm'
        self.homepage = 'http://bbs.pediy.com/'
        self.article = 'http://bbs.pediy.com/showthread.php?t='
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

    def __del__(self):
        if self.filename:
            self.cookie.save(filename=self.filename, ignore_expires=True, ignore_discard=True)

    def failed(self, message):
        return message.startswith(self.error_message)

    def login(self, account='', password=''):
        md5 = hashlib.md5()
        md5.update(password)
        data = {
            'account': account,
            'password': md5.hexdigest()
        }
        self.headers = {
            'Host': 'passport.kanxue.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://passport.kanxue.com/my.htm?1468845541',
            'Connection': 'close'
        }
        try:
            # first request
            request = urllib2.Request(
                self.login_url,
                data=urllib.urlencode(data),
                headers=self.headers
            )
            response_token = self.opener.open(request)

            # get token
            token = get_token(response_token.read())

            # get data
            data = {
                'action': 'synlogin',
                'token': token,
                'time': str(int(time.time()))
            }
            url = 'http://ce.kanxue.com/ucenter/user.php' + '?' + urllib.urlencode(data)

            # set headers
            self.headers['Host'] = 'ce.kanxue.com'
            self.headers['Accept'] = '*.*'
            self.headers['Referer'] = 'http://passport.kanxue.com/user-login.htm'
            del self.headers['X-Requested-With']

            # get
            request = urllib2.Request(url, headers=self.headers)
            response_cookie = self.opener.open(request)
            ce_token = response_cookie.info().getheader('Set-Cookie')

            # get 2
            data['time'] = str(int(time.time()))
            data['token'] = get_token(ce_token, 'ce_token=', ';')
            url = 'http://bbs.pediy.com/ucenter/user.php' + '?' + urllib.urlencode(data)
            self.headers['Host'] = 'bbs.pediy.com'
            self.headers['Referer'] = 'http://passport.kanxue.com/user-login.htm'
            request = urllib2.Request(url, headers=self.headers)
            self.opener.open(request)

            return 'login success!'
            # cookie
            # print self.cookie
        except urllib2.URLError, e:
            return self.error_message + e.reason
            # print e.reason + 'error!'
        except Exception, e:
            return self.error_message + e.message

    def get_page(self, url=r'http://bbs.pediy.com'):
        self.headers['Host'] = 'bbs.pediy.com'
        self.headers['Referer'] = ''
        request = urllib2.Request(url, headers=self.headers)
        try:
            response = self.opener.open(request).read()
        except urllib2.HTTPError, e:
            response = self.error_message + e.reason
        except urllib2.URLError, e:
            response = self.error_message + e.reason
        except Exception, e:
            response = self.error_message + e.message
        return response

    @staticmethod
    def save_data(_data='', _filename='1.html'):
        f = open(_filename, 'w')
        f.write(_data)
        f.close()


def get_tid(content):
    return content[content.find('t=')+2:]

def insert_to_database(tid, title):
    ca = Cache()
    if ca.lookup(tid):
        return ''
    else:
        print ca.insert(tid, title)
        return 'Success'

'''
    get all good articles
'''
def get_all_goodness():
    pediy = PeDiy('pediy.cookie')
    try:
        exited = False
        r = RePediy()
        page = 2
        goodpage_url = r.get_goodness(pediy.get_page(pediy.homepage))
        goodpage = pediy.get_page(goodpage_url)
        search_suffix = r.get_article_list(goodpage).replace('&amp;', '&')
        articles = r.get_articles(goodpage)
        while True:
            number = 0
            for i in articles:
                number += 1
                if not insert_to_database(get_tid(i[0]), i[1].encode('utf-8')):
                    print 'Not new articles!'
                    exited = True
                    break
            if exited or number != 20:
                break
            goodpage_url = pediy.homepage + search_suffix + '%s' % page
            print goodpage_url
            page += 1
            articles = r.get_articles(pediy.get_page(goodpage_url))
    except urllib2.HTTPError, e:
        return pediy.error_message + e.reason
    except Exception, e:
        return pediy.error_message + e.message

if __name__ == '__main__':
    get_all_goodness()
