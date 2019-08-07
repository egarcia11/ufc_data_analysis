'''extraction of data from ufc website
extracts all information for each fighter '''

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup, SoupStrainer
from numpy import NaN

import pandas as pd
import json
import string

"""
	Description

	Parameters
	----------
	arg : type
		description
	Returns
	-------
	type
		beautifulSoup object parsed from the desired segment
	"""

def website_soup(url, segment):
	"""
	requests website content and then converts
	an HTML segment into a beautifulSoup object

	Parameters
	----------
	url : str
		website link
	segment : str
		html tag in which the desired information is stored
	Returns
	-------
	beautifulSoup object parsed from the desired segment
	"""
	try:
		response = requests.get(url)
		response.raise_for_status()
		strainer = SoupStrainer(segment)
		soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
		return soup
	except HTTPError:
		print("HTTP error occured")
	except Exception as err:
		print("Other error occured")


class UrlExtraction(object):

	# TODO: class docstring please
	# TODO: have the urls be an attribute of urlExtraction

	BASESITE = 'http://ufcstats.com/statistics/fighters?char=a&page=all'

	@staticmethod
	def alphabetize_urls(url, var_index):
		"""
        Generator of a list of alphabatized urls. Replaces 1 letter
        in the base URL with every lower-case letter of the alphabet (a-z)

        Parameters
        ----------
        url: str
            the full URL of ANY version of the parent website
        var_index: int
            index of the varying letter in the URL
        Yields:
        ------
        generator
            27 alphabetized urls (a-z)
        """
		for letter in string.ascii_lowercase:
			new_url = url[:var_index] + letter + url[var_index + 1:]
			yield new_url

	@staticmethod
	def get_children_urls(url):
		"""
		parses fighter's urls from the given website

		Parameters
		----------
		url : str
			alphabetical url
			for example; http://ufcstats.com/statistics/fighters?char=a&page=all
			which contains all fighters with who's name start with the letter a
		Yields
		-------
		str
			list of fighter urls in the given alphabetical url
		"""
		container = website_soup(url, 'tbody')
		tags = container.find_all('a')
		for tag in tags:
			yield tag.get('href')

	def get_all_fighter_urls(self):
		"""
		Creates a list of all the fighter's url in the ufc website.

		Returns:
		---------
		list[str]
			list of all fighter's url in the http://ufcstats.com website
			with no duplicates
		"""
		all_urls=[]
		for url in self.alphabetize_urls(self.BASESITE,-10):
				all_urls.extend(self.get_children_urls(url))
		return all_urls


class AtributesExtraction(object):
	#TODO: class docstring please
	def get_fighter_statistics(self, www):
		"""
		Creates a list of all the fighter's url in the ufc website.

		Returns:
		-----
		list[str]
			list of all of fighter urls in the http://ufcstats.com website
			with no duplicates
		"""
		wb_soup = website_soup(www, 'section')

		'''Parsing fighter's name'''
		name_and_record = self.get_name_and_record(wb_soup)
		name = str(name_and_record['name'])

		'''Parsing fighter's record'''
		record = self.clean_record(name_and_record['record'])
		wins = record['wins']
		draws = record['draws']
		losses = record['losses']

		'''Parsing remaining attributes'''
		tags = wb_soup.find_all("li", "b-list__box-list-item b-list__box-list-item_type_block")
		fighter_stats = [item.text.split() for item in tags]

		for i, stat in enumerate(fighter_stats):
			if i is 0:
				height = self.clean_height(' '.join(stat[1:4]))
			elif i is 1:
				weight = self.clean_data(stat[1])
			elif i is 2:
				reach = self.clean_data(stat[1])
			elif i is 3:
				try:
					stance = str(stat[1])
				except:
					stance = None
			elif i is 4:
				dob = self.clean_date(stat)
			elif i is 5:
				slpm = self.clean_data(stat[1])
			elif i is 6:
				stracc = self.clean_data(stat[2])
			elif i is 7:
				sapm = self.clean_data(stat[1])
			elif i is 8:
				strdef = self.clean_data(stat[2])
			elif i is 9:
				continue
			elif i is 10:
				tdavg = self.clean_data(stat[2])
			elif i is 11:
				tdacc = self.clean_data(stat[2])
			elif i is 12:
				tddef = self.clean_data(stat[2])
			elif i is 13:
				subavg = self.clean_data(stat[2])

		fighterDict = dict(url=www, name=name, wins=wins, draws=draws,
						   losses=losses, height=height, weight=weight, reach=reach,
						   stance=stance, dob=dob, slpm=slpm, stracc=stracc, sapm=sapm,
						   strdef=strdef, tdavg=tdavg, tdacc=tdacc, tddef=tddef, subavg=subavg)

		return fighterDict

	@staticmethod
	def clean_height(data):
		clean_data = [integer for integer in data if integer.isnumeric()]
		try:
			feet = clean_data[0]
			inches = ''.join(clean_data[1:])
			height_feet = float(feet) + float(inches) / 12.0
			return round(height_feet, 2)
		except:
			return NaN

	@staticmethod
	def clean_data(data):
		"""
		cleans the string and converts str to int

		Parameters
		----------
		data : str
			data scraped from the website
		Returns
		-------
		int
			cleaned string, converted into an int
		"""
		'''cleans data from '%' and '/' and converts unicode data to a float'''
		digits = [integer for integer in data if integer.isnumeric() or '.' in integer]

		if len(digits):
			cleaned_digits = ''.join(digits)
			return float(cleaned_digits)
		else:
			return None

	def clean_date(self,date):
		#TODO: better docstring
		'''
		cleans and reformats the date
			date string: the unformated version of the date
		'''
		stringDate = ''.join(date[1:4])
		if '--' not in stringDate:

			month = self.get_month(stringDate)
			day = stringDate[3:5]
			year = stringDate[6:10]

			date = '{}-{}-{}'.format(month, day, year)

			return date
		else:
			return None

	@staticmethod
	def get_month(date):
	#TODO: figure out if there is a better way of doing this? or maybe move this all the way to the top?
	#TODO: also docstring please, you piece of poop!
		if 'Jan' in date:
			return 1
		elif 'Feb' in date:
			return 2
		elif 'Mar' in date:
			return 3
		elif 'Apr' in date:
			return 4
		elif 'May' in date:
			return 5
		elif 'Jun' in date:
			return 6
		elif 'Jul' in date:
			return 7
		elif 'Aug' in date:
			return 8
		elif 'Sep' in date:
			return 9
		elif 'oct' in date:
			return 10
		elif 'Nov' in date:
			return 11
		elif 'Dec' in date:
			return 12

	@staticmethod
	def get_name_and_record(self, soup):
		#TODO: Docstring PLEASE!!!!!!
		container = soup.h2.text.split()
		recordIndex = [i for i, attribute in enumerate(container) if attribute == 'Record:'][0]

		#TODO: replace this in the futre, maybe reverse the order of the arguments?
		recordIndexPlus1 = recordIndex + 1

		#TODO: why are you creating a dictionary here? turn this into a list, and return 2 arguments instead of a dictionary
		nameAndRecord = dict(name='', record='')
		nameAndRecord['name'] = ' '.join(container[0:recordIndex])
		nameAndRecord['record'] = container[recordIndexPlus1:][0]

		return nameAndRecord

	@staticmethod
	def clean_record(data):

		#TODO: this initializes everything to a 0, and thats important because we need to know if value is a 0 or a NaN...
		record = dict(wins=0, losses=0, draws=0)
		hyphenLocation = [i for i, letter in enumerate(data) if letter is '-']

		temp = []
		for i, item in enumerate(data):
			if i is hyphenLocation[0]:
				record['wins'] = int(''.join(temp))
				temp = []
				continue
			elif i is hyphenLocation[1]:
				record['draws'] = int(''.join(temp))
				temp = []
				continue
			elif i is len(data):
				record['losses'] = int(''.join(temp))
			temp.append(item)
		return record

if __name__ == '__main__':
	urlExtraction = UrlExtraction()

	all = urlExtraction.get_all_fighter_urls()

	atribuesExtraction = AtributesExtraction()

	test = atribuesExtraction.get_fighter_statistics(all[1])
	print(test)
