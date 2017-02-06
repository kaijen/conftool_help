import requests
import csv
import configparser
from datetime import datetime

cfg = configparser.ConfigParser()
cfg.read('./config.ini')
user = cfg['Authentication']['user']
password = cfg['Authentication']['password']
conftool_id = cfg['Authentication']['conftool_id']
talks_csv = cfg['Files']['csv']

s = requests.Session()
# s.proxies = {
#   'http': 'http://127.0.0.1:8080',
#   'https': 'http://127.0.0.1:8080',
# }
# s.verify = False

paramsGet = {"page": "login"}
login = {'ctusername': user, 'ctpassword': password, 'cmd_login': 'yes'}

r = s.get("https://www.conftool.net/entwicklertag2017/index.php")
r = s.post("https://www.conftool.net/entwicklertag2017/index.php",data=login,params=paramsGet)

paramsGet = {"page": "editReview"}

date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

paramsPost = {
                "path": "browseAssignedPapers",
                "form_pccomments": "",
                "cmd_savereview": "Gutachten speichern",
                "form_creationdate": date,
                "form_personID": conftool_id,
}

with open(talks_csv, 'r', newline='') as csvfile:
    talkreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in talkreader:
        paramsPost['form_paperID'] = row[0]
        paramsPost['form_overall'] = row[1]
        r = s.post("https://www.conftool.net/entwicklertag2017/index.php", data=paramsPost, params=paramsGet)
# print(s.cookies)
# print(r.status_code)
