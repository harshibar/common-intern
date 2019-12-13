from bs4 import BeautifulSoup
import requests
import pprint
import json
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin

pp = pprint.PrettyPrinter(indent=4)

URL = 'https://boards.greenhouse.io/braintree/jobs/1316736?gh_jid=1316736&gh_src=1d1244401'
s = requests.Session()

JOB_APP = {
    "first_name": "Harshi",
    "last_name": "Bar",
    "email": "info.harshibar@gmail.com",
    "phone": "123-456-7890",
    "resume": "resume.pdf", # figure out how to add file
    "linkedin": "https://www.linkedin.com/in/hyerramreddy/",
    "website": "www.harshi.me",
    "github": "https://github.com/harshibar"
}

def fetch(url, data=None):
    if data is None:
        return s.get(url).content
    else:
        return s.post(url, data=data).content

def greenhouse(empty_form):
    print (empty_form.keys())
    for key in empty_form.keys():
        try:
            key.encode('utf-8')
            print(key)
        except:
            print ('fail')
    app = empty_form.job_application
    pp.pprint(app)
    pass

def lever():
    pass

if __name__ == '__main__':
    soup = BeautifulSoup(fetch(URL), 'html.parser')
    form = soup.find('form')
    soup_fields = form.findAll('input')
    fields = soup.findAll('div', {'class': 'field'})

    # make dictionary between field name and input id
    form_fields = {}
    for field in fields:
        print ("\n\n FIELD", field)
        if (field.input):
            # print (field.label.contents[0], type(field.label.contents[0]))
            print ("INPUT", field.input, field.input['id'])
            form_fields[field.label.contents[0]] = field.input.id

    print ("\n\n RES", form_fields)

    # pp.pprint (fields)
    # fields = form.findAll('input')

    empty_form = dict( (field.get('id'), field.get('value')) for field in soup_fields)
    print("\n\n EMPTY", empty_form)
    complete_form = empty_form

    if "greenhouse" in URL:
        complete_form = greenhouse(form)

    # print (empty)
    posturl = urljoin(URL, form['action'])
    # print (posturl)

    r = s.post(posturl, data=complete_form)
    # print (r.text)

    # print (s.get(URL).text)