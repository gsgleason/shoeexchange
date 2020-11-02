import requests
from config import config
from lxml import etree

#create session to share cookies and socket
s = requests.Session()

#get login page
url = 'https://www.pythonanywhere.com/login/'
r = s.get(url)

#load html
doc = etree.HTML(r.text)

#get value of input csrfmiddlewaretoken
token = doc.xpath("//input[@name='csrfmiddlewaretoken']")[0].attrib['value']

# data to be posted
payload = {
        'auth-username': config['pythonanywhere']['username'],
        'auth-password': config['pythonanywhere']['password'],
        'csrfmiddlewaretoken': token,
        'login_view-current_step': 'auth'
        }

# set referer header to match current page
s.headers.update({'referer': url})

#submit login form
r = s.post(url, data=payload, )

# update referer to be the last response location header
if r.history:
    s.headers.update({'referer': 'https://www.pythonanywhere.com{}'.format(r.history[-1].headers.get('Location'))})

url = 'https://www.pythonanywhere.com/user/{0}/webapps/#tab_id_{0}_pythonanywhere_com'.format(config['pythonanywhere']['username'])

r = s.get(url)
doc = etree.HTML(r.text)

token = doc.xpath("//form[@action='/user/{0}/webapps/{0}.pythonanywhere.com/extend']/input[@name='csrfmiddlewaretoken']".format(config['pythonanywhere']['username']))[0].attrib['value']


s.headers.update({'referer': 'https://www.pythonanywhere.com/user/{}/webapps/'.format(config['pythonanywhere']['username'])})

payload = {
        'csrfmiddlewaretoken': token
        }

url = "https://www.pythonanywhere.com/user/{0}/webapps/{0}.pythonanywhere.com/extend".format(config['pythonanywhere']['username'])

r = s.post(url, data=payload)

# GET the tasks tab
url = "https://www.pythonanywhere.com/user/{}/tasks_tab/".format(config['pythonanywhere']['username'])
r = s.get(url)
s.headers.update({'referer': url})
token = doc.xpath("//input[@name='csrfmiddlewaretoken']")[0].attrib['value']

#get schedule
url = "https://www.pythonanywhere.com/api/v0/user/shoeexchange/schedule/".format(config['pythonanywhere']['username'])
r = s.get(url)
schedule = r.json()

# extend scheduled task
extend_url = schedule[0]['extend_url']
url = "https://www.pythonanywhere.com{}".format(extend_url)
s.headers.update({'X-CSRFToken': token})
r = s.post(url)
