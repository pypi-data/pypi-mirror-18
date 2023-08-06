#!/usr/bin/env python
#encoding=utf-8

'''
Usage:
    say [options] TEXT
    say --default=LANG
    say --status
    say --help
    say --version

Arguments:
    TEXT                文本或文本路径
    LANG                语种

Options:
    -h, --help          显示帮助

    -c, --chinese       中文
    -e, --american      美音
    -u, --british       英音
    -y, --cantonese     粤语
    -j, --japanese      日语
    -k, --korean        韩语
    -f, --french        法语
    -s, --spanish       西班牙语
    -t, --thai          泰语
    -a, --arabic        阿拉伯语
    -r, --russian       俄语
    -p, --portuguese    葡萄牙语

    --auto              自动检测语种

    --default=LANG      配置默认语种，有效值为：
                            auto, chinese, american, british, cantonese, 
                            japanese, korean, french, spanish, thai, arabic,  
                            russian, portuguese
    --status            显示当前配置
    --v, --version      显示当前版本

Example:
    say 你好
    say -u "hello world"
    say path/to/text/text.txt
    say --default=auto

'''
version = '0.1.4'

import sys, os
import json, re

from docopt import docopt
try: # python3
    import requests
    from urllib.parse import quote 
    PYTHON_VERSION = 3
except: # python
    reload(sys)
    sys.setdefaultencoding('utf-8')
    import urllib2
    from urllib import quote, urlencode
    PYTHON_VERSION = 2


LANGS = {'auto':        'auto', 
        'chinese':      'zh',
        'american':     'en',
        'british':      'uk',
        'cantonese':    'cte',
        'japanese':     'jp',
        'korean':       'kor',
        'french':       'fra',
        'spanish':      'spa',
        'thai':         'th',
        'arabic':       'ara',
        'russian':      'ru',
        'portuguese':   'pt',
        }

def detect_lang(text):
    '''
    自动检测语种时调用
    向百度 POST 文本，获取百度检测出的文本语种
    '''
    url = 'http://fanyi.baidu.com/langdetect'
    data = {'query': text[:30]}
    if PYTHON_VERSION == 2:
        req = urllib2.Request(url)
        data = urlencode(data)
        response = urllib2.urlopen(url, data)
        lang = json.loads(response.read())['lan']
    elif PYTHON_VERSION == 3:
        response = requests.post(url, data)
        lang = response.json()['lan']
    return lang


def get_lang(args, text):
    '''
    根据参数，获取语种
    '''
    lang = ''
    for language in LANGS:
        if args['--%s' % language]:
            if language == 'auto':
                lang = detect_lang(text)
            else:
                lang = LANGS[language]

    if not lang: # 如果没有指定哪种语言，则使用默认语种
        lang = LANGS.get(get_default_language())
        if not lang or lang == 'auto': # 如果没有默认语种或默认自动检测，则自动检测语种
            lang = detect_lang(text)
    return lang

def get_default_language():
    '''
    读取默认语种
    '''
    config = {}
    try:
        config_path = os.path.expanduser('~') + '/.say'
        with open(config_path) as f:
            config = json.loads(f.read())
    except:
        pass
    return config.get('default_language')


def set_default_language(language):
    '''
    设置默认语种
    '''
    if language not in LANGS:
        print('设置失败，%s 不是有效值' % language)
        return

    try:
        config_path = os.path.expanduser('~') + '/.say'
        with open(config_path, 'w') as f:
            config_json = json.dumps({'default_language': language})
            f.write(config_json)
            print('设置成功，当前默认语种为 %s ' % language)
    except:
        print('设置失败')

def handle_args(args):
    '''
    处理参数，返回语种和文本
    '''
    if args['--default']:
        set_default_language(args['--default'])
        exit()
    if args['--version']:
        exit(version)
    if args['--status']:
        current_default_language = get_default_language()
        if not current_default_language:
            set_default_language('auto')
            current_default_language = 'auto'
        exit('当前默认语种: %s' % current_default_language)

    text = args['TEXT']
   
    # 如果是文件，就阅读文件内容；如果不是文件，就阅读命令行中的文本
    try:
        text_dir = os.path.expanduser(os.path.dirname(text))
        if not text_dir:
            text_dir = '.'
        os.chdir(text_dir)
        with open(os.path.basename(text), 'r') as f:
            text = f.read()
    except:
        pass
    lang = get_lang(args, text)
    return lang, text

def run():
    '''
    处理参数，向百度发送请求，调用 mplayer 读取声音
    '''
    args = docopt(__doc__)
    lang, text = handle_args(args)
    
    if len(text) > 255:
        if PYTHON_VERSION == 2:
            text = text.decode('utf-8')
            texts = re.split(u'[.,;:?，。？：；]', text)
        elif PYTHON_VERSION == 3:
            texts = re.split('[.,;:?，。？：；]', text)

        for text in texts:
            if text:
                print(text)
                url = 'http://fanyi.baidu.com/gettts?lan=%s&text=%s' % (lang, quote(text.encode('utf-8')))
                os.system('mplayer "%s" -msglevel all=-1 -nolirc' % url) 
    else:
        if text:
            url = 'http://fanyi.baidu.com/gettts?lan=%s&text=%s' % (lang, quote(text))
            os.system('mplayer "%s" -msglevel all=-1 -nolirc' % url) 


if __name__ == '__main__':
    run()
