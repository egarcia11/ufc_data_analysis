'''extraction of data from ufc website
extracts all information for each fighter '''

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import json
import string

BASESITE = 'http://ufcstats.com/statistics/fighters?char=a&page=all'

def website_soup(URL):
	'''requests website content and then
	   converts HTML content into a beutiful soup'''
	try:
		response = requests.get(URL)
		response.raise_for_status()
	except HTTPError:
		print("error occured")
	except Exception as err:
		print("Other error occure")

	return BeautifulSoup(response.content,"lxml")

'''The URL to fighter's statistics is contained within the a tags
inside the website's tbody'''

def get_children_urls(www):
	'''gets the list of URLS contained within a website's tbody tag'''
	wb_soup = website_soup(www)
	container = wb_soup.tbody
	tags = container.find_all('a')

	for tag in tags:
		yield tag.get('href')
	#return [tag.attrs['href'] for tag in tags]

def alphabetize_urls(URL, var_index):
	'''Generator of a list of alphabatized websites. Replaces 1 letter
	in the parent URL with every letter of the alphabet.

	string parentURL: the full URL of ANY version of the parent website
	int var_index: index of the varying letter in the URL'''
	website = list(URL)
	for letter in string.ascii_lowercase:
		website[var_index] = letter
		yield ''.join(website)

def get_fighter_urls():																																																									

	'''returns the list of all of the fighter links'''
	urls=[]

	for url in alphabetize_urls(BASESITE,-10):
			urls.extend(get_children_urls(url))

	return urls

def remove_duplicates(x):
  return list(dict.fromkeys(x))

"""if __name__ == '__main__':
	all_urls = get_fighter_urls()"""