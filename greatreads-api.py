'''The purpose of this app is to provide fast, responsive searches of the Goodreads API'''

import requests
import json

api_key = key=nt4K4tcITuTOR11SDbX1Mg
user_id_allen = 11210913

get-read-shelf = requests.get('https://www.goodreads.com/review/list?format=xml&id=' + user_id_allen + '&shelf=read&sort=date_read&v=2&' + api_key)

# print(get-read-shelf)
