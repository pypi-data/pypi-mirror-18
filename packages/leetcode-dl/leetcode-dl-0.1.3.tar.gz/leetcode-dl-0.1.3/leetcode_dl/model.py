# coding:utf-8

from collections import namedtuple


__all__ = ['ProgLang', 'ProgLangList', 'ProgLangDict', 'Solution', 'Quiz']

ProgLang = namedtuple('ProgLang', ['language', 'ext', 'annotation'])

ProgLangList = [ProgLang('c++', 'cpp', '//'),
                ProgLang('java', 'java', '//'),
                ProgLang('python', 'py', '#'),
                ProgLang('c', 'c', '//'),
                ProgLang('c#', 'cs', '//'),
                ProgLang('javascript', 'js', '//'),
                ProgLang('ruby', 'rb', '#'),
                ProgLang('swift', 'swift', '//'),
                ProgLang('go', 'go', '//')]

ProgLangDict = dict((item.language, item) for item in ProgLangList)

Solution = namedtuple('Solution', ['id', 'title', 'capital_title', 'pass_language'])


class Quiz:
    def __init__(self, data):
        self.id = int(data['id'])
        self.title = data['title']
        self.capital_title = data['capital_title']
        self.url = data['url']
        self.acceptance = data['acceptance']
        self.difficulty = data['difficulty']
        self.lock = data['lock']
        self.pass_status = True if data['pass'] == 'ac' else False  # 'None', 'ac', 'notac'
        self.article = data['article']
        self.sample_code = None
        self.pass_language = []

    def __repr__(self):
        return '<Quiz: {id}-{title}({difficulty})-{pass_status}>'.format(
            id=self.id, title=self.title, difficulty=self.difficulty, pass_status=self.pass_status)
