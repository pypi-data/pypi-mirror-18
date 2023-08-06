# coding:utf-8

import os

from leetcode_dl.utils import write_config, get_config_from_file
from leetcode_dl.const import CONFIG_FILE
from leetcode_dl.model import ProgLangDict
from leetcode_dl.leetcode import Leetcode

from clint.textui import prompt, puts, colored, validators
from clint.arguments import Args


def show_usage():
    """Usage:
    leetcode-dl
    leetcode-dl -h|help     help page
    leetcode-dl -set        set config
    leetcode-dl -show       show config
    leetcode-dl -readme     generate|update readme
    leetcode-dl -q qid      download by qid(like 1 2 16)
"""
    pass


def run():
    """ command: `leetcode-dl`"""

    puts('====== Leetcode-dl ======')
    if not os.path.exists(CONFIG_FILE):
        puts(colored.yellow('Can\'t load config.\nPlease Set config file First'))
        cli_set_config()
        puts()
        puts(colored.green('Now you can start download, just type `leetcode-dl` again'))
    else:
        config = get_config_from_file(CONFIG_FILE)
        puts('The solutions will download to folder:' + config['dist'])
        puts()

        leetcode = Leetcode(config)
        download(leetcode)
        leetcode.write_readme()
        puts('finish write readme')


def run_by_id(qids):
    """ command: `leetcode-dl -q qid`"""

    puts('====== Leetcode-dl ======')
    if not os.path.exists(CONFIG_FILE):
        puts(colored.yellow('Can\'t load config.\nPlease Set config file First'))
        cli_set_config()
        puts()
        puts(colored.green('Now you can start download, just type `leetcode-dl` again'))
    else:
        config = get_config_from_file(CONFIG_FILE)
        puts('The solutions will download to folder:' + config['dist'])
        puts()

        leetcode = Leetcode(config)
        download(leetcode, qids)


def show_help():
    """ command: `leetcode-dl -h|help`"""

    puts('====== Help   Info ======')
    puts(show_usage.__doc__)


def show_config():
    """ command: `leetcode-dl -show`"""

    puts('====== Config Info ======')
    if not os.path.exists(CONFIG_FILE):
        puts(colored.yellow('Can\'t load config.\nPlease Set config file First'))
        cli_set_config()
    else:
        config = get_config_from_file(CONFIG_FILE)
        puts(colored.green('Username:' + config['username']))
        puts(colored.green('Password:' + config['password']))
        puts(colored.green('Repo:' + config['repo']))
        puts(colored.green('Language:' + config['language']))
        puts(colored.green('Dist:' + config['dist']))


def cli_set_config():
    """ command: `leetcode-dl -set`"""

    puts('====== Leetcode-dl ======')
    all_languages = ProgLangDict.keys()
    username = prompt.query('Input your leetcode username: ')
    password = prompt.query('Input your leetcode password: ')
    repo = prompt.query('Input your repo url: ')
    while True:
        language = prompt.query('Input your leetcode coding languages(like python, javascript): ')
        languages = [x.lower().strip() for x in language.split(',')]
        if set(languages).issubset(set(all_languages)):
            break
        puts(colored.yellow('language set wrong'))

    dist = prompt.query('Input the path to save the solutions:', default=os.getcwd(), validators=[validators.PathValidator()])

    dct = dict(username=username, password=password, repo=repo, language=language, dist=dist)
    write_config(CONFIG_FILE, **dct)
    puts(colored.green('Set Completed!'))


def readme():
    """ command: `leetcode-dl -readme`"""
    puts('====== Leetcode-dl ======')
    if not os.path.exists(CONFIG_FILE):
        puts(colored.yellow('Can\'t load config.\nPlease Set config file First'))
        cli_set_config()
        puts()
        puts(colored.green('Now you can start download, just type `leetcode-dl` again'))
    else:
        config = get_config_from_file(CONFIG_FILE)
        puts('The readme will write to folder:' + config['dist'])
        puts()

        leetcode = Leetcode(config)
        write_readme(leetcode)


def write_readme(leetcode):
    leetcode.login()
    puts('Leetcode login succeed...')
    leetcode.load()
    puts('Leetcode load self info...')
    puts('begin to write readme...')
    leetcode.write_readme()
    puts('finish write readme')


def download(leetcode, pids=None):
    """
    :param leetcode: type Leetcode
    :param pids: type list
    """
    leetcode.login()
    puts('Leetcode login succeed...')
    leetcode.load()
    puts('Leetcode load self info...')
    puts('begin to download...\n')

    if not pids:
        leetcode.download_with_thread_pool()
    else:
        for pid in pids:
            leetcode.download_by_id(pid)
    puts('finish download')


def cli():
    # args = Args()
    # puts(colored.red('Aruments passed in: ') + str(args.all))
    # puts(colored.red('Aruments grouped passed in: ') + str(args.grouped))
    all_args = Args().grouped

    args_len = len(all_args)
    # print(args_len)
    if args_len == 1:
        run()

    elif args_len == 2:
        # print(all_args.keys())
        arg = list(all_args.keys())[1]
        # print(arg)

        if arg in ['-show']:
            show_config()

        elif arg in ['-q']:
            qids = [int(x.strip()) for x in all_args[arg].all]
            # print(qids)
            run_by_id(qids)

        elif arg in ['-h', '-help']:
            show_help()

        elif arg in ['-set']:
            cli_set_config()

        elif arg in ['-readme']:
            readme()

        else:
            puts('You entered wrong command')
            show_help()

    else:
        puts('You entered wrong command')
        show_help()
