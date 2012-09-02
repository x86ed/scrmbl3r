#! /usr/bin/python

import os
import random
import re

from helpers import findInList

import config

def getpeople(chat):
    _people_re = re.compile('[a-z]{1,12}:')
    if chat:
        people = re.findall(_people_re, chat[0])
        if people:
            for i in range(len(people[0])):
                people[0][i] = people[0][i][:-1]
            return people[0]
    else:
        return [0]

def msgcheck(msg):
    _msgarray = []
    _msgregex = '^[a-z]{1,12}\|\w{8}:\s\[:3\]((\w|\/|\+|\?|\(|\)|\=)*\|(\d|a|b|c|d|e|f){128})*\[:3\]$'
    _msgbeg   = '^[a-z]{1,12}\|\w{8}:\s\[:3\](\w|\/|\+|\?|\(|\)|\=)*$'
    _msgmid   = '^(\w|\/|\+|\?|\(|\)|\=)*$'
    _msgend   = '^(\w|\/|\+|\?|\(|\)|\=)*\|(\d|a|b|c|d|e|f){128}\[:3\]$'
    if len(msg) > 4096:
        for i in range(0, len(msg), 4096):
            _msgarray.append(msg[i:i+4096])
        for i in range(len(_msgarray)):
            if _msgarray[i] and i == 0 and not re.findall(_msgbeg, _msgarray[i]):
                return 0
            elif i != len(_msgarray)-1 and not re.findall(_msgmid, _msgarray[i]):
                return 0
            elif not re.findall(_msgend, _msgarray[i]):
                return 0
        return 1
    elif re.findall(_msgregex, _msg):
        return 1
    return 0

def enterchat(name, nick, key):
    #global $data, $_SESSION;name = name.lower();
    self.session['name'] = 's'+ name 
    if os.path.isfile(config.CHAT_LOGS + name):
        chat = open(config.CHAT_LOGS + name, 'r+b')
        chat = chat.readlines()
    if not self.session['nick']:
        if not getpeople(chat) and in_array(nick, getpeople(chat)):
            print "error"
            return
        else:
            self.session['nick'] = nick
            self.session['check'] = 'OK'
            chat[0] = chat[0].strip() + nick + ':' + key + "|\n"
            chat[len(chat)] = '> ' + nick + " has arrived\n"
            _log_it = os.open(config.CHAT_LOGS + name, os.O_EXLOCK )
            os.write(_log_it, ''.join(chat))
            os.close(_log_it)
            self.session['pos'] = len(open(config.CHAT_LOGS + name).readlines()) - 1

def chat(name):
    #global $data, $nicks, $timelimit, $maxinput, $install, $_SESSION, $genurl, $filesize;
    #global config.CHAT_LOGS, config.NICKNAMES
    name = ''.join(name)
    name = name.lower();
    _datafile = open(config.CHAT_LOGS + name, 'w+')
    _chat = _datafile.readlines()
    _datafile.close()
    _nickname = config.NICKNAMES[random.randrange(0, len(config.NICKNAMES) - 1)]
    while _nickname in getpeople(_chat):
        _nickname = config.NICKNAMES[random.randrange(0, len(config.NICKNAMES) - 1)]
    return ["chat.html", config.INSTALL, _nickname, name, str(config.MAXIMUM_MESSAGE_LENGTH)]
            
def logout(name, nick, ghost):
    name = name.lower()
    self.session['name'] = 's'+ name
    if  self.session['check'] == "OK":
        chat = open(config.CHAT_LOGS + name, 'r+b')
        chat = chat.readlines()
        _public = re.findall(nick + '\:[^\|]+\|', chat[0])
        chat[0] = chat[0].replace(_public[0], '')
        chat[len(chat)+1] = '< '+ nick + " has left\n"
        if not ghost:
            self.session.unset()
            self.session.destroy()
        if os.path.isfile(config.CHAT_LOGS + name):
            _log_it = os.open(config.CHAT_LOGS + name, os.O_EXLOCK )
            os.write(_log_it, ''.join(chat))
            os.close(_log_it)