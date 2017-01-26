'''The purpose of this app is to provide fast, responsive searches of the Goodreads API'''

import requests
import json
from xml.etree import ElementTree as ET

api_key = 'key=nt4K4tcITuTOR11SDbX1Mg'
user_id_allen = '11210913'


# get_read_shelf = requests.get('https://www.goodreads.com/review/list?format=xml&id=' + user_id_allen + '&shelf=read&sort=date_read&v=2&' + api_key)
#
# # print(get_read_shelf)
#
# #get a series by author id
# #use find author id by name
author_id = 227840
# get_series_author = requests.get('https://www.goodreads.com/series/list/' + author_id + '.xml?' + api_key)
#
# #get review by title and (optional) author
title = 'A+GAME+OF+THRONES'
author = 'George+Martin'
# get_reviews = requests.get('https://www.goodreads.com/book/' + title + '.FORMAT')

#search by title, author, or isbn
get_books = requests.get('https://www.goodreads.com/search.xml?' + api_key + '&q=' + title + '+ '+ author)
root = ET.fromstring(get_books.content)
books = []

for title in root[1].iter('title'):
    books.append(title.text)
for url in root[1].iter('image_url'):
    book_cover = url.text

print(books[:2])
