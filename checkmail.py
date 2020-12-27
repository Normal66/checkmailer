# Класс для разборок :)
import requests
import random
import time
import json
from proxysocks import SocksIMAP4, SocksIMAP4SSL
from urllib.parse import urlparse
import imaplib

class BaseMail:
    _base_url = ''
    _src_key = []
    _src_proxy = {}
    _src_server = {}
    _Good = 0
    _Bad = 0
    _Well = []
    # --------------------------------------------------------------------------------------------------------------- #
    def __init__(self, _sUser, _sPass, _sProxy, _sKeywords, _sUseProxy=False, _sUsekeywords=False,):
        self.lUser = _sUser
        self.lPass = _sPass
        self.lUseProxy = _sUseProxy
        self.lUseKeywords = _sUsekeywords
        self._src_proxy = _sProxy
        self._src_key = _sKeywords
        self._base_url = 'https://emailsettings.firetrust.com/settings?q='+_sUser
        self.do_make_servers()
        return
    # ----------------------------------------------------------------------------------------------- #
    def get_good(self):
        return self._Good
    # ----------------------------------------------------------------------------------------------- #
    def get_bad(self):
        return self._Bad
    # ----------------------------------------------------------------------------------------------- #
    def get_well(self):
        return self._Well
    # ----------------------------------------------------------------------------------------------- #
    def do_get_page(self):
        session = requests.Session()
        user_agent_list = [
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
            ]
        referer_list = ['https://www.yandex.ru/', 'https://yahoo.com/', 'https://www.msn.com/', 'https://www.tut.by/',
                       'http://www.br.by/', 'http://www.zubr.com/', 'http://www.tit.by/', 'https://google.com']
        referer = random.choice(referer_list)
        user_agent = random.choice(user_agent_list)
        # Set the headers
        headers = {'User-Agent': user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Referer': referer}
        req = session.get(self._base_url, headers=headers)
        time.sleep(1)
        req.encoding = 'utf-8'
        self._src_text = req.text
        session.close()
        return
    # --------------------------------------------------------------------------------------------------------------- #
    # Формирует список почтовых адресов для разных протоколов эл. почтового адреса
    def do_make_servers(self):
        self.do_get_page()
        _loc_data = json.loads(self._src_text)
        for _items in _loc_data['settings']:
            if _items['protocol'] == 'SMTP':
                self._src_server['SMTP'] = [_items['address'], _items['port'], _items['username']]
            if _items['protocol'] == 'POP3':
                self._src_server['POP3'] = [_items['address'], _items['port'], _items['username']]
            if _items['protocol'] == 'IMAP':
                self._src_server['IMAP'] = [_items['address'], _items['port'], _items['username']]
    # ----------------------------------------------------------------------------------------------- #
    def do_check_imap(self):
        _tmp = self._src_server.get('IMAP')
        _server = _tmp[0]
        _port = _tmp[1]
        _user = _tmp[2]
        try:
            mail = imaplib.IMAP4_SSL(_server, _port)
            mail.login(_user, self.lPass)
            mail.select()   # INBOX по умолчанию
            self._Good += 1
            if self.lUseKeywords:
                mail.list()
                mail.select('INBOX')
                for ters in self._src_key:
                    typ, data = mail.search(None, '(FROM "' + ters + '")', '(SINCE "01-Jan-2020")')
                    if data != [b'']:
                        listOfSplitStrings = str(data[0], encoding='utf8').split(" ")
                        self._Well.append(_user + ' ' + '|' + ' ' + str(len(listOfSplitStrings)) + ' ' + '|' + ' ' + ters + "\n")
                mail.close()
            mail.logout()
        except:
            self._Bad += 1
    # ----------------------------------------------------------------------------------------------- #
    def do_check_imap_proxy(self):
        _tmp = self._src_server.get('IMAP')
        _server = _tmp[0]
        _port = _tmp[1]
        _user = _tmp[2]
        proxy_type = proxy_type = "socks5"
        try:
            mail = SocksIMAP4SSL(host=_server, port=_port,
                                    proxy_addr='', proxy_port='', proxy_type=proxy_type)
            mail.login(_user, self.lPass)
            mail.select()   # INBOX по умолчанию
            self._Good += 1
            if self.lUseKeywords:
                mail.list()
                mail.select()
                for ters in self._src_key:
                    typ, data = mail.search(None, '(FROM "' + ters + '")', '(SINCE "01-Jan-2020")')
                    if data != [b'']:
                        listOfSplitStrings = str(data[0], encoding='utf8').split(" ")
                        self._Well.append(_user + ' ' + '|' + ' ' + str(len(listOfSplitStrings)) + ' ' + '|' + ' ' + ters + "\n")
                mail.close()
            mail.logout()
        except:
            self._Bad += 1
    # ----------------------------------------------------------------------------------------------- #
    def do_check_pop(self):
        pass
    def do_check_pop_proxy(self):
        pass
    def do_check_smtp(self):
        pass
    def do_check_smtp_proxy(self):
        pass



    def test(self):
        return self._src_server