import requests
from lxml import html
import csv
import configparser

cfg = configparser.ConfigParser()
cfg.read('./config.ini')
user = cfg['Authentication']['user']
password = cfg['Authentication']['password']
talks_csv = cfg['Files']['csv']

s = requests.Session()
# s.proxies = {
#   'http': 'http://127.0.0.1:8080',
#   'https': 'http://127.0.0.1:8080',
# }
# s.verify = False

r = s.get("https://www.conftool.net/entwicklertag2017/index.php")

paramsGet = {"page": "login"}
login = {'ctusername': user, 'ctpassword': password, 'cmd_login': 'yes'}
r = s.post("https://www.conftool.net/entwicklertag2017/index.php", data=login, params=paramsGet)

paramsGet = {"page": "browseAssignedPapers"}
r = s.get("https://www.conftool.net/entwicklertag2017/index.php", params=paramsGet)

h = html.fromstring(r.text)

xpath_talks = '//*[@id="inner_content"]/div/table'
xpath_id = './tr[1]/td[1]/span[1]'
xpath_title = './tr[1]/td[2]/span[4]'
xpath_typ = './tr[1]/td[2]/span[3]'
xpath_author = './tr[1]/td[2]/span[5]'
xpath_org = './tr[1]/td[2]/span[7]'

with open(talks_csv, 'w', newline='',encoding='utf-8') as csvfile:
    talkwriter = csv.writer(csvfile,delimiter=';', quotechar="'",  quoting=csv.QUOTE_MINIMAL)
    for talk in h.xpath(xpath_talks):
        id = talk.xpath(xpath_id)[0].text.strip()
        title = talk.xpath(xpath_title)[0].text.strip()
        typ = talk.xpath(xpath_typ)[0].text.strip()
        author = talk.xpath(xpath_author)[0].text.strip().replace('\n', ' ')
        org = talk.xpath(xpath_org)[0].text.strip().replace('\n', ' ')
        talkwriter.writerow([id, title, typ, author, org])
