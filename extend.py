import requests
from config import config
from lxml import etree

username = config['pythonanywhere']['username']
password = config['pythonanywhere']['password']

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
        'auth-username': username,
        'auth-password': password,
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

# load the webapp tab
url = 'https://www.pythonanywhere.com/user/{0}/webapps/#tab_id_{0}_pythonanywhere_com'.format(username)
r = s.get(url)
doc = etree.HTML(r.text)

# find the token
token = doc.xpath("//form[@action='/user/{0}/webapps/{0}.pythonanywhere.com/extend']/input[@name='csrfmiddlewaretoken']".format(username))[0].attrib['value']

#set referer header
s.headers.update({'referer': 'https://www.pythonanywhere.com/user/{}/webapps/'.format(username)})

#post to extend web app
payload = {
        'csrfmiddlewaretoken': token
        }
url = "https://www.pythonanywhere.com/user/{0}/webapps/{0}.pythonanywhere.com/extend".format(username)
r = s.post(url, data=payload)

# GET the tasks tab
url = "https://www.pythonanywhere.com/user/{}/tasks_tab/".format(username)
r = s.get(url)
s.headers.update({'referer': url})
token = doc.xpath("//input[@name='csrfmiddlewaretoken']")[0].attrib['value']

#get schedule
url = "https://www.pythonanywhere.com/api/v0/user/shoeexchange/schedule/".format(username)
r = s.get(url)
schedule = r.json()

# extend scheduled task
extend_url = schedule[0]['extend_url']
url = "https://www.pythonanywhere.com{}".format(extend_url)
s.headers.update({'X-CSRFToken': token})
r = s.post(url)
