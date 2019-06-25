from bs4 import BeautifulSoup, SoupStrainer
import extract_fighter_urls
import json
import string
import decimal
import requests

def get_children_urls(www):
	'''gets the list of URLS contained within a website's tbody tag'''
	wb_soup = get_website_soup(www)
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
	BASESITE = 'http://ufcstats.com/statistics/fighters?char=a&page=all'
	for url in alphabetize_urls(BASESITE,-10):
			urls.extend(get_children_urls(url))
	return urls

def remove_duplicates(x):
	return list(dict.fromkeys(x))


def get_website_soup(URL, segment):
	"""Parses  a segment from a URL
		string: segment = name of the tag enclosing the desired segment
		string: url = desired url"""

	response = check_response(requests.get(URL))
	strainer = SoupStrainer(segment)
	soup = BeautifulSoup(response.content,'lxml',parse_only=strainer)

	return soup

def check_response(response):
	'''checks response of a website'''
	if response.status_code == 200:
		return response
	else:
		print("Error: {}".format(response.reason))

def get_fighter_statistics(www):
	url = www
	wb_soup = get_website_soup(www,'section')

	'''Parsing fighter's name'''
	nameAndRecord = get_name_and_record(wb_soup)
	name = str(nameAndRecord['name'])

	'''Parsing fighter's record'''
	record = clean_record(nameAndRecord['record'])
	wins = record['wins']
	draws = record['draws']
	losses = record['losses']

	tags = wb_soup.find_all("li","b-list__box-list-item b-list__box-list-item_type_block")
	fighterStats = [item.text.split() for item in tags]

	for i,stat in enumerate(fighterStats):
		#searching fighterstats is made easier by the fact that we know the order of each statistic
		if i is 0:
			height = clean_data(' '.join(stat[1:4]),i)
		elif i is 1:
			weight = clean_data(stat[1])
		elif i is 2:
			reach = clean_data(stat[1])
		elif i is 3:
			try:
				stance = str(stat[1])
			except:
				stance = None
		elif i is 4:
			dob = clean_date(stat)
		elif i is 5:
			slpm = clean_data(stat[1])
		elif i is 6:
			stracc = clean_data(stat[2])
		elif i is 7:
			sapm = clean_data(stat[1])
		elif i is 8:
			strdef = clean_data(stat[2])
		elif i is 9:
			continue
		elif i is 10: 
			tdavg = clean_data(stat[2])
		elif i is 11:
			tdacc = clean_data(stat[2])
		elif i is 12:
			tddef = clean_data(stat[2])
		elif i is 13:
			subavg = clean_data(stat[2])

	fighterDict = dict(url = url,name = name,wins = wins,draws = draws,
		losses = losses,height = height,weight = weight,reach = reach,
		stance = stance,dob = dob,slpm = slpm,stracc = stracc,sapm = sapm,
		strdef = strdef,tdavg = tdavg,tdacc = tdacc,tddef = tddef,subavg = subavg)

	return fighterDict

def clean_data(data,*i):
	'''cleans data from '%' and '/' and converts unicode data to a float'''
	digits = [integer for integer in data if integer.isnumeric() or '.' in integer]
	if len(digits) >= 1:
		if i is 0: #handles height
			heightInFeet = (float(digits[0]) + float(digits[1]/12))
			return heightInFeet
		else: #handles everything else
			cleandigits = ''.join(digits)
			return float(cleandigits)
	else:
		return None

def clean_date(date):
	'''convers string into an sql date object'''
	stringDate = ''.join(date[1:4])
	if '--' not in stringDate:

		month = get_month(stringDate)
		day = stringDate[3:5]
		year = stringDate[6:10]

		date = '{}-{}-{}'.format(month,day,year)

		return date
	else:
		return None

def get_month(date):

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

def get_name_and_record(soup):

	container = soup.h2.text.split()

	recordIndex = [i for i,section in enumerate(container) if section == 'Record:'][0]
	recordIndexPlus1 = recordIndex +1

	nameAndRecord = dict(name='',record='')

	nameAndRecord['name'] = ' '.join(container[0:recordIndex])
	nameAndRecord['record'] = container[recordIndexPlus1:][0]

	return nameAndRecord

def clean_record(data):
	record = dict(wins=0,losses=0,draws=0)
	hyphenLocation = [i for i,letter in enumerate(data) if letter is '-']

	temp = []
	for i,item in enumerate(data):
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

	#obtain fighter links
	all_links = [line.strip("\n") for line in open("fighter_urls")]
	all_links = remove_duplicates(all_links)

	#loading fighter links into outfile
	with open('fighters.json','w') as outfile:
		for i,link in enumerate(all_links):
			fighter = get_fighter_statistics(link)
			json.dump(fighter, outfile)
			outfile.write('\n')
			print(i/len(all_links)*100, '% complete')
			
