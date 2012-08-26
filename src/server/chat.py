import os
import re

def getpeople(chat):
        _people_re = re.
        compile('[a-z]{1,12}:')
        people = re.findall(_people_re, chat[0])
        for i in range(len(people[0])):
            people[0][i] = people[0][i][:-1]
        return people[0]

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
                elif i !=(count($msgarray)-1) and not re.findall(_msgmid, _msgarray[i])):
                    return 0
                elif not re.findall(_msgend, _msgarray[i])):
                    return 0
            return 1
        elif re.findall(_msgregex, _msg):
            return 1
    return 0

#def welcome(name):
#           global INSTALL;
#           template that uses INSTALL and name

def enterchat(name, nick, key):
            global $data, $_SESSION;
            name = name.lower();
            session_name('s'+ $name);
            session_start();
            if os.path.isfile(CHAT_LOGS + name):
                chat = open(CHAT_LOGS + name, 'r+b')
            if not self.session['nick']):
                if not getpeople(chat) and in_array($nick, getpeople($chat))) {
                    print "error"
                    return
                else:
                    self.session['nick'] = nick
                    self.session['check'] = 'OK'
                    #fix this for readline
                    chat[0] = trim($chat[0]).$nick.':'.$key."|\n"
                    chat[count($chat)] = '> '.$nick." has arrived\n"
                    file_put_contents($data.$name, implode('', $chat), LOCK_EX)
                    self.session['pos'] = len(open(CHAT_LOGS + name).readlines()) - 1

def chat(name):
            global $data, $nicks, $timelimit, $maxinput, $install, $_SESSION, $genurl, $filesize;
            name = name.lower();
            _datafile = open(CHAT_LOGS + name)
            _chat = _datafile.readlines()
            _datafile.close()
            _nickname = NICKNAMES[mt_rand(0, len(NICKNAMES) - 1)];
            while (in_array(_nickname, getpeople(_chat))) {
                _nickname = NICKNAMES[mt_rand(0, len(NICKNAMES) - 1)];
        #template loader
            
def logout(name, nick, ghost) {
            name = name.lower()
            session_name('s'.$name);
            session_start();
            if ($_SESSION['check'] == "OK") {
                $chat = file($data.$name);
                preg_match('/'.$nick.'\:[^\|]+\|/', $chat[0], $public);
                $chat[0] = str_replace($public[0], '', $chat[0]);
                $chat[count($chat)+1] = '< '.$nick." has left\n";
                if (!$ghost) {
                    session_unset();
                    session_destroy();
                }
                if (file_exists($data.$name)) {
                    file_put_contents($data.$name, implode('', $chat), LOCK_EX);
                    if (function_exists('shmop_delete')) {
                        shmop_delete(shmop_open(ftok($data.$name, 'c'), "c", 0600, 256));
                    }
                }
            }
        }