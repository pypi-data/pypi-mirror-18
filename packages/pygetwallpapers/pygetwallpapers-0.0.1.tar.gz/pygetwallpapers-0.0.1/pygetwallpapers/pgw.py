#!/usr/bin/python
# -*- coding: utf-8

import argparse
import os
import sys
import logging

import spiders

from pgw_tools import functions
from pgw_tools import constants


def parse_args():
    example = "%s --domain example.com" % constants.PKG['BIN_NAME']

    parser = argparse.ArgumentParser(
        add_help=True, version='v%s' % constants.PKG['VERSION'])
    parser.add_argument("-d", "--domain", dest='domain', type=str, default=None, required=True,
                        help="Домен с которого нужно собрать картинки. Можно посмотреть все доступные домены вызвав команду '%s -dl'. Обязательный аргумент!" % example)
    parser.add_argument("-s", "--size", dest='size', type=str, default="1920x1080",
                        help="Желаемый размер в формате 'ШИРИНАxВЫСОТА'. Можно посмотреть все доступные размеры вызвав команду '%s -sl' По-умолчанию '1920x1080'" % example)
    parser.add_argument("-c", "--category", dest='category', type=str, default="all",
                        help="Название категории. Можно посмотреть все доступные имена вызвав команду '%s -cl'. По-умолчанию 'all'" % example)
    parser.add_argument("-p", "--pages", dest='pages', type=int, default=10,
                        help="Количество страниц, которые надо обработать. Чтобы обработать все страницы в категории надо указать ключ '-m[--use-max]'. По-умолчанию: 10")
    parser.add_argument("-o", "--output", dest='output', type=str, default=None,
                        help="Путь к файлу, в который будут сохранены ссылки. По-умолчанию будет создана структура каталогов '%s/category/size' и файл с именем '%s'" % (constants.SAVE_DIR, constants.URLS_FILE))

    parser.add_argument("-a", "--append", dest='append', action='store_true',
                        help="Если файл для сохранения ссылок существует, то новые ссылки будут добавлены в конец файла")
    parser.add_argument("-V", "--verbose", dest='verbose', action='store_true',
                        help="Включить подробный лог работы скрипта")
    parser.add_argument("-m", "--use-max", dest='useMax', action='store_true',
                        help="Ключ '-p' будет игнорироваться. Скрипт сам определит количество страниц и соберет максимально возможное количество ссылок")
    parser.add_argument("-dl", "--domain-list", dest='domainList', action='store_true',
                        help="Просмотреть все доступные домены")
    parser.add_argument("-cl", "--category-list", dest='categoryList', action='store_true',
                        help="Просмотреть все доступные имена категорий")
    parser.add_argument("-sl", "--size-list", dest='sizeList', action='store_true',
                        help="Просмотреть все доступные размеры изображений")
    return parser.parse_args()


def run():
    arguments = parse_args()

    args = arguments.__dict__

    if args['domain'] not in spiders.DOMAIN_LIST:
        functions.print_("Not domain in domain list!", False)
        functions.print_(
            "For show domain list use command: %s -dl" % constants.PKG['NAME'], False)
        functions.exit(1)

    domain = args['domain'].split('.')[0]

    try:
        spider = __import__("spiders.%s" % domain, globals(),
                            locals(), ["spiders.%s" % domain], -1)
        spider = spider.WallpaperSpider
    except ImportError:
        functions.print_("Import module name '%s' failed!" % domain, False)
        functions.exit(1)

    CATEGORYES = spider.categoryes_list()
    SIZES = spider.sizes_list()

    if args['domainList'] == True:
        functions.print_(spiders.DOMAIN_LIST)
        functions.exit(0)

    if args['categoryList'] == True:
        functions.print_(CATEGORYES)
        functions.exit(0)

    if args['sizeList'] == True:
        functions.print_(SIZES)
        functions.exit(0)

    if args['category'] not in CATEGORYES:
        args['category'] = CATEGORYES[0]

    if args['size'] not in SIZES:
        args['size'] = SIZES[0]

    if args['output'] is None:
        args['output'] = functions.mkdirp(
            constants.SAVE_DIR, args['category'], args['size'])
        args['output'] = os.path.join(args['output'], constants.URLS_FILE)
    else:
        if not os.path.isfile(args['output']):
            functions.print_("Path '%s' is not file!" % args['output'], False)
            functions.exit(1)

    if args['verbose'] == True:
        logging.basicConfig(level=logging.DEBUG)

    if args['append'] == True:
        args['append'] = 'a'
    else:
        args['append'] = 'w'

    wpParser = spider(args)
    wpParser.banner()
    wpParser.run()
    functions.print_(wpParser.render_stats(), False)
