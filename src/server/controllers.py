#! /usr/bin/python

import cgi
import io
import os
import re
import session
import time
import tornado.web

from helpers import HTTPSMixin, findInList
from chat import chat, getpeople, msgcheck, enterchat, chat, logout

import config

class SSLController(tornado.web.RequestHandler, HTTPSMixin):
    def get(self):
        if not self.is_secure():
            return self.redirect(self.httpsify_url())
        elif not self.get_current_user() and self.is_secure():
            return self.redirect(self.httpify_url('/not_allowed_https/'))

class MainController(tornado.web.RequestHandler):
    def get(self):
        self.session = session.TornadoSession(self.application.session_manager, self)
        _get_c = self.get_arguments('c')
        _get_redirect = self.get_arguments('redirect')
        _get_close  = self.get_arguments('close')
        _post_logout = self.get_arguments('logout')
        _made_of_chars = '^\w+$'
        _valid_url = '((mailto\:|(news|(ht|f)tp(s?))\:\/\/){1}\S+)'
        _user_agent = self.request.headers["User-Agent"]
        _browser = 'style'
        _mobile_browsers = ['iPhone', 'iPod', 'BlackBerry', 'Windows Phone', 'Fennec', 'Opera Mini', 'Opera Mobi', 'MeeGo']
        for b in _mobile_browsers:
            if _user_agent.find(b) > -1:
                _browser = 'mobile'
        if _get_redirect and re.findall(_valid_url,_get_redirect[0]):
            self.render('redirect.html', redirect=_get_redirect[0])
            return
        if ''.join(_get_close):
            self.render('close.html')
            return
        if _get_c:
            if re.findall(_made_of_chars, _get_c[0]):
                if len(_get_c) <= 32:
                    responseList = chat(_get_c)
                    self.render(responseList[0],browser='style',install=responseList[1], nick=responseList[2] , name=responseList[3], maxinput=responseList[4]) 
                else:
                    self.render('welcome.html',browser='style',install=config.INSTALL,name='chat name too large')
            else:
                self.render('welcome.html',browser='style',install=config.INSTALL,name='letters and numbers only')
        elif _post_logout and  re.findall(_made_of_chars, _post_logout):
                self.session['name'] ='s' + _post_logout
                self.session.save()
                logout(_post_logout, self.session['nick'], 0)
                self.render('welcome.html',browser='style',install=config.INSTALL,name='name your chat')
        else:
                self.render('welcome.html',browser='style',install=config.INSTALL,name='name your chat')

    def post(self):
        self.session = session.TornadoSession(self.application.session_manager, self)
        _valid_nick= '^[a-z]{1,12}$'
        _made_of_chars = '^\w+$'
        _valid_key = '^(\w|\/|\+|\?|\(|\)|\=)+$'
        _post_nick = ''.join(self.get_arguments('nick'))
        _post_name = ''.join(self.get_arguments('name'))
        _post_key = ''.join(self.get_arguments('key'))
        _post_pos = ''.join(self.get_arguments('pos'))
        _post_chat = ''.join(self.get_arguments('chat'))
        _post_input = ''.join(self.get_arguments('input'))
        if re.findall(_valid_nick, _post_nick) and re.findall(_made_of_chars, _post_name) and re.findall(_valid_key, _post_key):
            _post_name = _post_name.lower()
            self.session['name'] = 's' + _post_name
            self.session.save()
            if os.path.isfile(config.CHAT_LOGS + _post_name):
                _chatStat = os.stat(config.CHAT_LOGS + _post_name)
                chat = open(config.CHAT_LOGS + _post_name, "rb+")
                _chat_list = chat.readlines()
                _timestamp = int(time.time())
                if _timestamp - int(_chatStat.st_mtime) > config.TIME_LIMIT:
                    chat.close()
                    os.remove(config.CHAT_LOGS + _post_name)
                    enterchat(_post_name,_post_nick,_post_key,self)
                    return
            if _post_key == 'get' and self.session['check'] == 'OK':
                self.write(chat.readline().strip())
                return
            if len(getpeople(_chat_list)) >= config.MAXIMUM_USERS:
                self.write('full')
                return
            elif _post_nick in getpeople(_chat_list):
                self.write('inuse')
                return
            elif hasattr(self.session,'nick'):
                self.session.unset()
                self.session.destroy()
            if not hasattr(self.session,'nick'):
                enterchat(_post_name,_post_nick,_post_key,self)
                if not os.path.isfile(config.CHAT_LOGS + _post_name):
                    chat = open(config.CHAT_LOGS + _post_name, 'w+')
                    _chat_list = chat.readlines()
            else:
                self.write('error')
            return
        elif '_post_nick' in locals():
            self.write('error')
            return
        elif int(_post_pos) >= 0 and re.findall(_made_of_chars, _post_chat):
            _post_chat = _post_chat.lower()
            self.session['name'] = 's' + _post_chat
            self.session.save()
            if self.session['check'] == 'OK':
                if not os.path.isfile(config.CHAT_LOGS + _post_chat):
                    self.write('NOEXIST')
                    return
                else:
                    chat = open(config.CHAT_LOGS + _post_chat, "rb+")
                    _chat_list = chat.readlines() 
                    _pos = self.session['pos'] + int(_post_pos)
                    _sleepcounter = 0
                    while _pos >= len(_chat_list):
                        io.flush()
                        with open(config.CHAT_LOGS + _post_chat,'r+b') as _shared_mem:
                            if (_sleepcounter % (config.TIMEOUT / 4)) == 0:
                                _people = getpeople(chat)
                                _shm_id = mmap.mmap(_shared_mem.fileno(), 256, ACCESS_WRITE)
                                if not _shim_id:
                                    _last = []
                                else:
                                    _last = _shim_id
                                    for p in range(len(_people)):
                                        _timestamp = int(time.time())
                                        if _last[_people[p]] and (_timestamp - TIMEOUT) > _last[_people[p]]:
                                            _last[_people[p]] = []
                                            logout(_post_chat, _people[p], 1)
                                _timestamp = int(time.time())
                                _last[self.session['nick']] = _timestamp
                                _shm_id[0,len(_last)] = _last
                            _shim_id.close()
                            self.write(' ')
                            #if (connection_aborted()) {
                            #    return
                            #}
                            time.sleep(1)
                            _sleepcounter += 1;
                            chat = open(config.CHAT_LOGS + _post_chat, 'r+b');
                    if _pos < len(chat_list):
                        if msgcheck(_chat_list[_pos]) or re.findall(INFO_REG_EX , _chat_list[_pos]):
                            _match = re.findall('\([a-z]{1,12}\)[^\(^\[]+', _chat_list[_pos])
                            _nick = re.findall('^[a-z]{1,12}\|', _chat_list[_pos])
                            _nick = _nick[0][:-1]
                            _found = 0
                            for k in range(len(_match[0])):
                                if _match[0][k][:len(self.session['nick']) + 2] == '(%s)' % self.session['nick']:
                                    _match = _match[0][k][len(self.session['nick']) + 2:]
                                    _chat_list[_pos] = re.sub('\[:3\](.*)\[:3\]', '[:3]' + _match + '[:3]', _chat_list[_pos])
                                    _found = 1
                                    break
                            if not _nick or _nick != self.session['nick']:
                                if not _found and re.findall('\[:3\](.*)\[:3\]', _chat_list[_pos]):
                                    _chat_list[_pos] = '*'
                                else:
                                    _chat_list[_pos] = re.sub('^[a-z]{1,12}\|\w{8}', _nick, _chat_list[_pos])
                                print cgi.escape(_chat_list[_pos])
                            elif re.findall('\|\w{8}', _chat_list[_pos]):
                                _sentid = re.findall('\|\w{8}', _chat_list[_pos])
                                self.write(_sentid[:1])
            else:
                self.write('NOLOGIN')
            return
        elif _post_name and re.findall('^\w+$', _post_name) and len(_post_input) > 6:
            _post_name = _post_name.lower()
            self.session['name'] = 's' + _post_name
            self.session.save()
            chat = open(config.CHAT_LOGS + _post_name, "rb+")
            _thisnick = re.findall('^[a-z]{1,12}\|', _post_input)
            if msgcheck(_post_input) and  self.session['nick'] == _thisnick[0][0: -1]:
                if os.path.isfile(config.CHAT_LOGS + _post_name):
                    _log_it = os.open(config.CHAT_LOGS + _post_name, os.O_APPEND|os.O_EXLOCK )
                    os.write(_log_it, _post_input+"\n")
                    os.close(_log_it)
            return