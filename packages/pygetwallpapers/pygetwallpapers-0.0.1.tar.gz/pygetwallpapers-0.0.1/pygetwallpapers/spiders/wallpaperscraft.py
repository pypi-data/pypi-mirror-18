#!/usr/bin/python
# -*- coding: utf-8

from grab import Grab
from grab.spider import Spider, Task
import re
import codecs


__DOMAIN__ = "wallpaperscraft.com"

__SIZES__ = ['240x320', '240x400', '320x240', '320x480', '360x640', '400x480', '480x800', '480x854', '540x960', '640x960', '640x1136', '720x1280', '750x1334', '800x600', '800x1280', '960x544', '1024x600', '1024x768', '1024x1024', '1080x1920', '1152x864', '1280x720', '1280x800', '1280x900',
             '1280x960', '1280x1024', '1366x768', '1400x1050', '1440x900', '1440x2560', '1600x900', '1600x1200', '1680x1050', '1920x1080', '1920x1200', '2048x1152', '2048x2048', '2160x3840', '2560x1024', '2560x1080', '2560x1440', '2560x1600', '2732x2732', '3840x1200', '3840x2160', '3840x2400']

__CATEGORYES__ = ['all',  '3d',  'abstract',  'animals',  'anime',  'brands',  'cars',  'city',  'fantasy',
                  'flowers',  'food',  'games',  'girls',  'hi-tech',  'holidays',  'macro',  'men',  'movies',
                  'music',  'nature',  'other',  'space',  'sport',  'textures',  'tv-series',  'vector']


class WallpaperSpider(Spider):

    base_url = "https://%s" % (__DOMAIN__)
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0")
    current_page = 0
    images_on_page = 15
    img_XPath = '//div[@class="wallpapers"]/descendant::img/@src'
    total_pages_XPath = '//div[@class="pages"]/a[last()]/text()'

    @staticmethod
    def sizes_list():
        def cmp(x):
            x = x.split('x')
            return int(x[0]) * int(x[1])
        return sorted(__SIZES__, key=cmp)

    @staticmethod
    def categoryes_list():
        return __CATEGORYES__

    def __init__(self, ARGS=None):
        super(self.__class__, self).__init__()

        self.args = ARGS

        self.pages = self.args['pages']
        self.category = self.args['category']
        self.size = self.args['size']
        self.output = self.args['output']

        if self.category != "all":
            self.category = "catalog/%s" % (self.category)
        self.url_template = "%s/%s/%s" % (self.base_url,
                                          self.category, self.size)

        # Получаем настоящее количество страниц, независимо от выбора
        # пользователя
        self.real_max_pages = int(self.get_total_pages(self.url_template) - 1)

        if self.args['useMax'] == True:
            self.pages = self.real_max_pages

        self.urls = ["%s/page%d" % (self.url_template, page)
                     for page in xrange(2, self.pages + 1)]

        self.urls.insert(0, self.url_template)
        self.outputBuffer = codecs.open(
            self.output, self.args['append'], encoding='utf-8')

    def banner(self):
        print "*" * 40
        print "Parse domain: %s" % (__DOMAIN__)
        print "*" * 40
        print "Category: %s" % (self.category)
        print "Size: %s" % (self.size)
        print "Pages: %d of %d" % (self.pages, self.real_max_pages)
        print "Images total: %d" % (self.pages * self.images_on_page)
        print "%s" % ("Start...")
        print "#" * 40

    def task_generator(self):
        """Проходим в цикле по всем страницам и генерируем задачи для парсера Spider"""
        try:
            while (self.current_page < self.pages):
                self.target_url = self.get_url()
                yield Task('search', url=self.target_url)
        finally:
            pass

    def get_url(self):
        """Вернет URL страницы из сгенерированного массива"""
        url = self.urls[self.current_page]
        self.current_page = self.current_page + 1
        return url

    def get_total_pages(self, url=None):
        """Вернет число страниц для построения цикла"""
        g = Grab()
        g.go(self.url_template)
        return int(g.doc.select(self.total_pages_XPath).text())

    def writeUrl(self, url=""):
        """Приводим ссылки в нужный формат для скачивания"""
        dl_domain = url.index(__DOMAIN__)
        result = re.search(r"^" + re.escape(url[:dl_domain]) + "(" + re.escape(__DOMAIN__) +
                           r")\/(image)\/(.+)_([x0-9]+)\.([a-z]+)", url)
        newUrl = "%s/%s/%s_%s.%s" % ("https:" + url[:dl_domain] + __DOMAIN__,
                                     str(result.group(2)),
                                     str(result.group(3)),
                                     self.size,
                                     str(result.group(5)))
        self.outputBuffer.write(newUrl + '\n')

    def task_search(self, grab, task):
        """Собираем ссылки на превью картинки со страницы"""
        for elem in grab.doc.select(self.img_XPath):
            try:
                self.writeUrl(elem.html())
            except StandardError:
                continue
