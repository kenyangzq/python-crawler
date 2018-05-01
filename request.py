import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.1point3acres.com/bbs/')

soup = BeautifulSoup(r.text, 'lxml')
print(soup)