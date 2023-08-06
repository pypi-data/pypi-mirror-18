# coding:utf-8

import re
import configparser
import os


def get_config_from_file(filename):
    """ Get config from file

    :param filename: type str
    :return: type dict
    """
    cp = configparser.ConfigParser()
    cp.read(filename)

    if 'leetcode' not in list(cp.sections()):
        raise Exception('Please create config.cfg first.')

    username = cp.get('leetcode', 'username')
    password = cp.get('leetcode', 'password')

    if not username or not password:    # username and password not none
        raise Exception('Please set your username and password first\nYou can use `leetcode-dl -u username -p password`')

    language = cp.get('leetcode', 'language')
    if not language:
        language = 'python'    # language default python

    repo = cp.get('leetcode', 'repo')
    if not repo:
        raise Exception('Please set your Github repo address\nYou can use `leetcode-dl -r repo`')

    dist = cp.get('leetcode', 'dist')
    if not dist:
        dist = os.getcwd()

    rst = dict(username=username, password=password, language=language.lower(), repo=repo, dist=dist)
    return rst


def rep_unicode_in_code(code):
    """ Replace unicode to str in the code
    like '\u003D' to '='

    :param code: type str
    :return: type str
    """
    pattern = re.compile('(\\\\u[0-9a-zA-Z]{4})')
    m = pattern.findall(code)
    for item in set(m):
        code = code.replace(item, chr(int(item[2:], 16)))    # item[2:]去掉\u
    return code


def check_and_make_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)


######################
#
# config set from cli
#
######################

def write_config(filename, **kw):
    """ Write config to file

    :param filename: type str
    :param kw: type dict
    """
    config = configparser.ConfigParser()

    if os.path.exists(filename):
        config.read(filename)
    else:
        config['leetcode'] = {}

    for k, v in kw.items():
        config.set('leetcode', k, v)

    # must write to the file
    # otherwise set can not effect
    with open(filename, 'w') as configfile:
        config.write(configfile)
