#! /usr/bin/python

import cgi
import io
import os
import re
import session
import time
import tornado.web

from helpers import HTTPSMixin, findInList


class SSLController(tornado.web.RequestHandler, HTTPSMixin):
    def get(self):
        if not self.is_secure():
            return self.redirect(self.httpsify_url())
        elif not self.get_current_user() and self.is_secure():
            return self.redirect(self.httpify_url('/not_allowed_https/'))

class MainController(tornado.web.RequestHandler):
    def get(self):
        _get_c = self.get_arguments('c')
        print _get_c
        _post_logout = self.get_arguments('logout')
        _made_of_chars = '^\w+$'
        if _get_c:
            if re.findall(_made_of_chars, _get_c[0]):
                if len(_get_c) <= 32:
                    chat(_get_c);
                else:
                    welcome('chat name too large')
            else:
                welcome('letters and numbers only')
        elif _post_logout and  re.findall(_made_of_chars, _post_logout):
                self.session['name'] ='s' + _post_logout
                self.save()
                logout(_post_logout, self.session['nick'], 0)
                welcome('name your chat')
        else:
                welcome('name your chat')

    def post(self):
        self.session = session.TornadoSession(self.application.session_manager, self)
        _valid_nick= '^[a-z]{1,12}$'
        _made_of_chars = '^\w+$'
        _valid_key = '^(\w|\/|\+|\?|\(|\)|\=)+$'
        _post_nick = self.get_arguments('nick')
        _post_name = self.get_arguments('name')
        _post_key = self.get_arguments('key')
        _post_pos = self.get_arguments('pos')
        _post_chat = self.get_arguments('chat')
        _post_input = self.get_arguments('input')
        if re.findall(_valid_nick, _post_nick) and re.findall(_made_of_chars, _post_name) and re.findall(_valid_key, _post_key):
            _post_name = _post_name.lower()
            self.session['name'] = 's' + _post_name
            self.save()
            if os.path.isfile(CHAT_LOGS + _post_name):
                _chatStat = os.stat(CHAT_LOGS + _post_name)
                chat = open(CHAT_LOGS + _post_name, "rb+")
                _timestamp = int(time.time())
                if _timestamp - int(_chatStat.st_mtime) > TIME_LIMIT:
                    chat.close()
                    os.remove(CHAT_LOGS + _post_name)
                    enterchat(_post_name,_post_nick,_post_key)
                    return
            if _post_key == 'get' and self.session['check'] == 'OK':
                print chat.readline().strip()
                return
            if len(getpeople(chat)) >= MAXIMUM_USERS:
                print 'full'
                return
            elif findInList(_post_nick,getpeople(chat)):
                print 'inuse'
                return
            elif hasattr(self.session,'nick'):
                self.session.unset()
                self.session.destroy()
            if not hasattr(self.session,'nick'):
                enterchat(_post_name,_post_nick,_post_key)
                if not os.path.isfile(CHAT_LOGS + _post_name):
                    chat = open(CHAT_LOGS + _post_name, 'w+')
            else:
                print 'error'
            return
        elif '_post_nick' in locals():
            print 'error'
            return
        elif int(_post_pos) >= 0 and re.findall(_made_of_chars, _post_chat):
            _post_chat = _post_chat.lower()
            self.session['name'] = 's' + _post_chat
            self.save()
            if self.session['check'] == 'OK':
                if not os.path.isfile(CHAT_LOGS + _post_chat):
                    print 'NOEXIST'
                    return
                else:
                    chat = open(CHAT_LOGS + _post_chat, "rb+")
                    chat_list = chat.readlines() 
                    _pos = self.session['pos'] + int(_post_pos)
                    _sleepcounter = 0
                    while _pos >= len(chat_list):
                        io.flush()
                        with open(CHAT_LOGS + _post_chat,'r+b') as _shared_mem:
                            if (_sleepcounter % (TIMEOUT / 4)) == 0:
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
                            print' '
                            #if (connection_aborted()) {
                            #    return
                            #}
                            time.sleep(1)
                            _sleepcounter += 1;
                            chat = open(CHAT_LOGS + _post_chat, 'r+b');
                    if _pos < len(chat_list):
                        if msgcheck(chat_list[_pos]) or re.findall(INFO_REG_EX , chat_list[_pos]):
                            _match = re.findall('\([a-z]{1,12}\)[^\(^\[]+', chat_list[_pos])
                            _nick = re.findall('^[a-z]{1,12}\|', chat_list[_pos])
                            _nick = _nick[0][:-1]
                            _found = 0
                            for k in range(len(_match[0])):
                                if _match[0][k][:len(self.session['nick']) + 2] == '(%s)' % self.session['nick']:
                                    _match = _match[0][k][len(self.session['nick']) + 2:]
                                    chat_list[_pos] = re.sub('\[:3\](.*)\[:3\]', '[:3]' + _match + '[:3]', chat_list[_pos])
                                    _found = 1
                                    break
                            if not _nick or _nick != self.session['nick']:
                                if not _found and re.findall('\[:3\](.*)\[:3\]', chat_list[_pos]):
                                    chat_list[_pos] = '*'
                                else:
                                    chat_list[_pos] = re.sub('^[a-z]{1,12}\|\w{8}', _nick, chat_list[_pos])
                                print cgi.escape(chat_list[_pos])
                            elif re.findall('\|\w{8}', chat_list[_pos]):
                                _sentid = re.findall('\|\w{8}', chat_list[_pos])
                                print _sentid[:1]
            else:
                print 'NOLOGIN'
            return
        elif _post_name and re.findall('^\w+$', _post_name) and len(_post_input) > 6:
            _post_name = _post_name.lower()
            self.session['name'] = 's' + _post_name
            self.save()
            chat = open(CHAT_LOGS + _post_name, "rb+")
            _thisnick = re.findall('^[a-z]{1,12}\|', _post_input)
            if msgcheck(_post_input) and  self.session['nick'] == _thisnick[0][0: -1]:
                if os.path.isfile(CHAT_LOGS + _post_name):
                    _log_it = os.open(CHAT_LOGS + _post_name, os.O_APPEND|os.O_EXLOCK )
                    os.write(_log_it, _post_input+"\n")
                    os.close(_log_it)
            return