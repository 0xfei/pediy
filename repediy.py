# coding=utf-8

import re
import sys

class RePediy:

    def __init__(self):
        self.goodness = '<a href=\"(?P<gn>.*)\">最新精华</a>'
        self.article = '<a href="(.*)" id=".*">([^<>]*)</a>'
        self.lists = '<a class=\".*?\" href=\"(.*?)\d{1,5}\" title=\".*\">\d{1,5}</a>'

    def get_goodness(self, content):
        if not content:
            return 'Not content!'
        pattern = re.compile(self.goodness)
        match = pattern.search(content)
        return ((match) and [match.group(1)] or ['NotMatch!'])[0]

    def get_articles(self, content):
        if not content:
            return ['Not content!']
        pattern = re.compile(self.article)
        match = pattern.findall(content)
        return match

    def get_article_list(self, content):
        if not content:
            return 'Not content!'
        pattern = re.compile(self.lists)
        match = pattern.search(content)
        return ((match) and [match.group(1)] or ['NotMatch!'])[0]

reload(sys)
sys.setdefaultencoding('utf8')
