# Скрипт для загрузки обоев с сайта [wallpaperscraft.com](https://wallpaperscraft.com)

## Установка зависимостей

```bash
$ sudo apt-get install -y libxml2-dev libxslt-dev
$ sudo pip install pycurl lxml
$ sudo pip install grab
```

### Установка пакета

**Способ 1:**

```bash
$ git clone git@github.com:yarkovaleksei/pygetwallpapers.git
$ cd pygetwallpapers
$ python setup.py install
```

**Способ 2:**

```bash
$ sudo pip install pygetwallpapers
```

**Запускаем скрипт:**

```bash
$ pgw -h
usage: pgw [-h] [-v] -d DOMAIN [-s SIZE] [-c CATEGORY] [-p PAGES] [-o OUTPUT]
           [-a] [-vv] [-m] [-dl] [-cl] [-sl]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d DOMAIN, --domain DOMAIN
                        Домен с которого нужно
                        собрать картинки. Можно
                        посмотреть все доступные
                        домены вызвав команду 'pgw --domain
                        example.com -dl'. Обязательный
                        аргумент!
  -s SIZE, --size SIZE  Желаемый размер в формате
                        'ШИРИНАxВЫСОТА'. Можно
                        посмотреть все доступные
                        размеры вызвав команду 'pgw
                        --domain example.com -sl' По-умолчанию
                        '1920x1080'
  -c CATEGORY, --category CATEGORY
                        Название категории. Можно
                        посмотреть все доступные
                        имена вызвав команду 'pgw --domain
                        example.com -cl'. По-умолчанию 'all'
  -p PAGES, --pages PAGES
                        Количество страниц, которые
                        надо обработать. Чтобы
                        обработать все страницы в
                        категории надо указать ключ
                        '-m[--use-max]'. По-умолчанию: 10
  -o OUTPUT, --output OUTPUT
                        Путь к файлу, в который будут
                        сохранены ссылки.
                        По-умолчанию будет создана
                        структура каталогов
                        'WallPapers/category/size' и файл с именем
                        'pgw_urls.txt'
  -a, --append          Если файл для сохранения
                        ссылок существует, то новые
                        ссылки будут добавлены в
                        конец файла
  -V, --verbose         Включить подробный лог
                        работы скрипта
  -m, --use-max         Ключ '-p' будет игнорироваться.
                        Скрипт сам определит
                        количество страниц и соберет
                        максимально возможное
                        количество ссылок
  -dl, --domain-list    Просмотреть все доступные
                        домены
  -cl, --category-list  Просмотреть все доступные
                        имена категорий
  -sl, --size-list      Просмотреть все доступные
                        размеры изображений
```

Скрипт пройдет по страницам и преобразует ссылки на превью картинок к нормальному виду, чтобы скачать их в указанном размере.

**Скачивание изображений:**

После того, как скрипт завершит работу, в текущем каталоге будет лежать файл с прямыми ссылками на изображения в нужном вам формате. В принципе вы можете скормить файл какому-нибудь менеджеру закачек, но зачем, если есть wget?!

Вводим в консоль команду:

```bash
# Выводим ход загрузки в консоль
$ wget --verbose -P /path/to/save -i ./WallPapers/category/size/pgw_urls.txt
# Или же запускаем скачивание в фоновом режиме
$ wget -b -P /path/to/save -i ./WallPapers/category/size/pgw_urls.txt
```

Все! Идем ставить чайник или покурить.

Согласитесь - это намного проще, чем кликать мышкой )))
