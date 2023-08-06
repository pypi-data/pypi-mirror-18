import jieba
import jieba.analyse
from bs4 import BeautifulSoup
from analyzerlibs.wordslib import stat


def init(parallel=1):
    jieba.initialize()

class WebSta:
    def __init__(self, ana_instance, num=100, pro=1):
        self.processer_num = pro
        self.keys_num = num
        self._res = ana_instance
        self.text = ana_instance.text()
        self.links = ana_instance.links
        self.keys = jieba.analyse.extract_tags(self.text, num)
        self.words = list(jieba.cut(self.text))

    @property
    def words_sta(self):
        return stat.w_stat(self.words, self.processer_num, words=self.keys)


