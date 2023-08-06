# coding:utf-8

import os
# from bonfy_dl.utils import get_config_from_file

__all__ = ['is_win32', 'CONFIG_FILE', 'HOME', 'PROXIES', 'HEADERS', 'MD_TEMPLATE']


is_win32 = os.name == "nt"
HOME = os.getcwd()


if is_win32:
    APPDATA = os.environ["APPDATA"]
    CONFIG_FILE = os.path.join(APPDATA, "leetcode-dl.cfg")
else:
    XDG_CONFIG_HOME = os.environ.get("LEETCODE_HOME", "~/.config")
    CONFIG_FILE = os.path.expanduser(XDG_CONFIG_HOME + "/leetcode-dl.cfg")

# CONFIG_FILE = os.path.join(HOME, 'config.cfg')

# If you have proxy, change PROXIES below
PROXIES = None

HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'leetcode.com',
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
}

# CONFIG = get_config_from_file(CONFIG_FILE)


# Markdown Template
# tm, num_solved, num_total, num_lock, repo
MD_TEMPLATE = '''# :pencil2: Leetcode Solutions with {language}
Update time:  {tm}

Auto created by [leetcode_generate](https://github.com/bonfy/leetcode) [Usage](https://github.com/bonfy/leetcode/blob/master/README_leetcode_generate.md)

I have solved **{num_solved}   /   {num_total}** problems
while there are **{num_lock}** problems still locked.

If you have any question, please give me an [issue]({repo}/issues).

If you are loving solving problems in leetcode, please contact me to enjoy it together!

(Notes: :lock: means you need to buy a book from Leetcode to unlock the problem)

| # | Title | Source Code | Article | Difficulty |
|:---:|:---:|:---:|:---:|:---:|
'''
