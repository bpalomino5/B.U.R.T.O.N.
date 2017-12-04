import requests

regions = {
		'california' : ', CA',
		'nevada' : ', NV',
		'florida' : ', FL',
		'italy' : ', LZ, Italy',
		'france' : ', 75, France',
		'peru' : ', LIM, Peru',
		'spain' : ', M, Spain',
	}

class Weather(object):
	def __init__(self):
		self.temp = None
		self.phrase = None
		self.description = None
		self.degree= u'\xb0'

	def getWeather(self,location):
		try:
			r = requests.get(self.getWeatherURL(location))
			
			# part1 = r.text.split('today_nowcard-location">')[1]
			# part2 = part1.split('<span')

			part1 = r.text.split('today_nowcard-phrase">')[1]
			part2 = part1.split('</div')
			self.phrase = part2[0]

			part1 = r.text.split('today_nowcard-temp"><span class="">')[1]
			part2 = part1.split('<sup>')
			self.temp = part2[0]

			self.description = self.phrase + ' with a temperature of ' + self.temp + self.degree.encode('utf8') + 'F'
		except (ValueError, IndexError) as e:
			self.description = "I'm sorry sir, I could not retrieve the forecast"

	def getWeatherURL(self,location):
		try:
			locID = self.getLocationID(location)
			CountryID = locID[0:2]
			URL = 'https://weather.com/weather/today/l/' + locID + ':1:' + CountryID
			return URL
		except ValueError as e:
			raise e

	def fixLocationStr(self,location):
		# split string into parts by whitespace
		locList = location.split()

		# default add california as region if region not provided
		if not regions.has_key(locList[-1].lower()): locList.append('california')
		
		region = locList.pop()

		if regions.has_key(region.lower()):
			location = " ".join(locList) + regions[region.lower()]
		
		return location

	def getLocationID(self,location):
		locationStr = self.fixLocationStr(location)
		locURL = 'http://wxdata.weather.com/wxdata/search/search?where=' + locationStr

		l = requests.get(locURL)
		part1 = l.text.split('<search ver="3.0">\n          ')[1]			# removes initial clutter
		part2 = part1.split('</search>')[0]									# removes ending clutter
		part3 = part2.split('</loc>')										# splits entries by delimiter
		part3.pop()															# pops last non usable clutter entry
		
		for entry in part3: 
			location = entry.split('>')
		
			if location[1] == locationStr:
				locID = location[0].split('"')[1]
				return locID
		raise ValueError

	def getDescription(self):
		return self.description

	def __str__(self):
		return self.description



"""
Previous design of weather.py using modular code
all ran on getWeather() method
Converted to Weather class on 4/13/17

def getWeatherURL(location):
	try:
		locID = getLocationID(location)
		CountryID = locID[0:2]
		URL = 'https://weather.com/weather/today/l/' + locID + ':1:' + CountryID
		return URL
	except ValueError as e:
		raise e

def getWeather(location):
	try:
		r = requests.get(getWeatherURL(location))
		#print 'status: ' , r.status_code
		part1 = r.text.split('today_nowcard-location">')[1]
		part2 = part1.split('<span')
		#print 'Location:',part2[0]

		part1 = r.text.split('today_nowcard-phrase">')[1]
		part2 = part1.split('</div')
		phrase = part2[0]
		#print 'Phrase:	',part2[0]

		part1 = r.text.split('today_nowcard-temp"><span class="">')[1]
		part2 = part1.split('<sup>')
		temp = part2[0]
		#print 'Temp:	',part2[0]
		return phrase + ' with a temperature of ' + temp + ' degrees fahrenheit'
	except ValueError as e:
		return 'Could not get weather data.'

	

#test double split
# part1 = r.text.split('today_nowcard-location">')[1]
# part2 = part1.split('<span')
# print 'Location:',part2[0]

# part1 = r.text.split('today_nowcard-phrase">')[1]
# part2 = part1.split('</div')
# print 'Phrase:	',part2[0]

# part1 = r.text.split('today_nowcard-temp"><span class="">')[1]
# part2 = part1.split('<sup>')
# print 'Temp:	',part2[0]

#get loc id
#'http://wxdata.weather.com/wxdata/search/search?where=CITY'

# method to fix input string to correct format for searching weather
def fixLocationStr(location):
	# split string into parts by whitespace
	locList = location.split()

	# default add california as region if region not provided
	if not regions.has_key(locList[-1].lower()): locList.append('california')
	
	# if len(locList)==1:
	# 	locList.append('california')

	region = locList.pop()

	if regions.has_key(region.lower()):
		location = " ".join(locList) + regions[region.lower()]
	# if region.lower() == 'california':
	# 	loc = " ".join(locList) + ', CA'
	# elif region.lower() == 'nevada':
	# 	loc = " ".join(locList) + ', NV'
	# elif region.lower() == 'florida':
	# 	loc = " ".join(locList) + ', FL'
	# elif region.lower() == 'italy':
	# 	loc = " ".join(locList) + ', LZ, Italy'
	# elif region.lower() == 'france':
	# 	loc = " ".join(locList) + ', 75, France'
	# elif region.lower() == 'peru':
	# 	loc = " ".join(locList) + ', LIM, Peru'
	# elif region.lower() == 'spain':
	# 	loc = " ".join(locList) + ', M, Spain'
	return location

def getLocationID(location):
	locationStr = fixLocationStr(location)
	locURL = 'http://wxdata.weather.com/wxdata/search/search?where=' + locationStr

	l = requests.get(locURL)
	part1 = l.text.split('<search ver="3.0">\n          ')[1]			# removes initial clutter
	part2 = part1.split('</search>')[0]									# removes ending clutter
	part3 = part2.split('</loc>')										# splits entries by delimiter
	part3.pop()															# pops last non usable clutter entry
	
	for entry in part3: 
		location = entry.split('>')
	
		if location[1] == locationStr:
			locID = location[0].split('"')[1]
			return locID
	raise ValueError
"""

# w = Weather()
# w.getWeather('Diamond Bar')
# print(w)

# weather = getWeather('Covina')
# print weather


# loc = 'Los Angeles California'
# location = 'http://wxdata.weather.com/wxdata/search/search?where=' + loc
# loc = fixLocStr(loc)

# l = requests.get(location)
# part1 = l.text.split('<search ver="3.0">\n          ')[1]			# removes initial clutter
# part2 = part1.split('</search>')[0]									# removes ending clutter
# part3 = part2.split('</loc>')										# splits entries by delimiter
# part3.pop()															# pops last non usable clutter entry


# for entry in part3: 
# 	location = entry.split('>')
# 	#print location
# 	if location[1] == loc:
# 		locID = location[0].split('"')[1]
# 	else:
# 		print('Did not find location!')
# 	return locID