import bs4
import file_manager as fm
import json
import string
import decimal
import requests

def get_children_urls(www):
	'''
	Parses the referenced hypertext within a website's tbody tag.

		string www: a website who's desired referenced hypertext
		is within the 'tbody' html-tag.

	yields: str
	'''

	wb_soup = get_website_soup(www,'tbody')
	tags = wb_soup.find_all('a')

	for tag in tags:
		yield tag.get('href')

def alphabetize_urls(baseURL, var_index):
	'''
	Generates 24 URLS by replacing the indexed variable of the baseURL with letters (A-Z).

		string URL: the full URL of ANY version of the parent website.
		int var_index: index of the varying letter in the URL.

	yields: str
	'''
	for letter in string.ascii_lowercase:
		baseURL[var_index] = letter
		yield ''.join(baseURL)

def get_fighter_urls():
	'''
	returns the list of all of the fighter links
	'''
	urls=[]
	baseURL = 'http://ufcstats.com/statistics/fighters?char=a&page=all'
	for url in alphabetize_urls(baseURL,-10):
			urls.extend(get_children_urls(url))
	return urls

def remove_duplicates(x):
	return list(dict.fromkeys(x))

def get_website_soup(URL, segment):
	"""
	Parses  a segment from a URL
		string: segment = name of the tag enclosing the desired segment to be parsed
		string: url =  url of the website
	returns: beautifulsoup4
	"""
	response = check_response(requests.get(URL))
	strainer = bs4.SoupStrainer(segment)
	soup = bs4.BeautifulSoup(response.content, 'lxml', parse_only=strainer)
	return soup

def check_response(response):
	'''checks response of a website'''
	if response.status_code == 200:
		return response
	else:
		print("Error: {}".format(response.reason))

def get_fighter_statistics(www):

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
			height = clean_height(' '.join(stat[1:4]))
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

	fighterDict = dict(url = www,name = name,wins = wins,draws = draws,
		losses = losses,height = height,weight = weight,reach = reach,
		stance = stance,dob = dob,slpm = slpm,stracc = stracc,sapm = sapm,
		strdef = strdef,tdavg = tdavg,tdacc = tdacc,tddef = tddef,subavg = subavg)

	return fighterDict

def clean_height(data):
	cleanData = [integer for integer in data if integer.isnumeric()]
	try:
		feet = cleanData[0]
		inches = ''.join(cleanData[1:])
		heightFeet = float(feet) + float(inches)/12.0
		return round(heightFeet,2)
	except:
		return None

def clean_data(data):
	'''cleans data from '%' and '/' and converts unicode data to a float'''
	digits = [integer for integer in data if integer.isnumeric() or '.' in integer]

	if len(digits) >= 1:
		cleandigits = ''.join(digits)
		return float(cleandigits)
	else:
		return None

def clean_date(date):
	'''
	cleans and reformats the date
		date string: the unformated version of the date
	'''
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

	#load the fighter URL's that have already been extracted.
	URLSfilePath = fm.get_absolute_path('data/raw/fighter_urls')
	print(URLSfilePath)

	all_links = [line.strip("\n") for line in open(URLSfilePath)]
	all_links = remove_duplicates(all_links)

	#exporting fighter statistics
	with open('fighters.json','w') as outfile:
		for i,link in enumerate(all_links):
			fighter = get_fighter_statistics(link)
			json.dump(fighter, outfile)
			outfile.write('\n')
			print(i/len(all_links)*100, '% complete')