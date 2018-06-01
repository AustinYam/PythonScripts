import urllib.request
import requests
import json
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

print('starting script')

now = datetime.now()
strnow = str(now)
strnow = strnow.split(' ')[0].split('-')
yy, mm, dd = strnow

end = now + timedelta(days = 30)
strEnd = str(end)
strEnd = strEnd.split(' ')[0].split('-')
ey, em, ed = strEnd

print('getting quote page')
quote_page = 'https://events.sjsu.edu/EventList.aspx?fromdate='+mm+'%2f'+dd+'%2f'+yy+'&todate='+em+'%2f'+ed+'%2f'+ey


page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

table = soup.find('table', attrs= {'id':'tblEvents'})


#for dates in table.find_all('h4', attrs={'class':'adx_wcag_header'}):
	#date = dates.text
	#print(date)

database = {
	'events': {},
}

event_id = 0

print('populating database')

#Getting the links for each event
for titles in table.find_all('div', attrs={'class':'vevent'}):
	event = {}

	event_id += 1
	event['id'] = event_id

	title = titles.find('a', attrs={'class':'url summary'})['href']
	
	new_page = 'https://events.sjsu.edu/'+str(title)
	
	
	pg = urllib.request.urlopen(new_page)
	new_soup = BeautifulSoup(pg, 'html.parser')
	
	data = new_soup.find('table',attrs={'id':'PageTable'})

	#eventName
	name = data.find('td', attrs={'class':'listheadtext'}).text
	event['title'] = name
	print(name)
	
	desc = data.find_all('td',attrs={'class':'detailsview'})

	response = requests.get(new_page)
	text = response.content
	newSoup = BeautifulSoup(response.content, 'html.parser')
	text = ''.join(newSoup.findAll(text=True))
	
	try:
	#eventDesc
		event_text = text[text.index("Event Description:") + len("Event Description:"): text.index("Location Information:")]
		event_text = event_text.strip()
	except Exception as e:
		event_text = None

	event['description'] = event_text
	

	try:
	#eventDate
		date_text = text[text.index("Start Date:") + len("Start Date:"): text.index("Start Time:")]
		date_text = date_text.strip()
	except Exception as e:
		date_text = None

	event['date'] = date_text
	
	try:
	#eventStartTime
		start_time = text[text.index("Start Time:") + len("Start Time:"): text.index("End Date:")]
		start_time = start_time.strip()
	except Exception as e:
		start_time = None

	event['start_time'] = start_time
	
	try:
	#eventEndTime
		end_time = text[text.index("End Time") + len("End Time:"): text.index("Event Description")]
		end_time = end_time.strip()
	except Exception as e:
		end_time = None

	event['end_time'] = end_time
	
	try:
	#eventLocation
		event_location = text[text.index("Location Information:") + len("Location Information:"): text.index("Contact Information:")]
		event_location = event_location.strip()
	except Exception as e:
		event_location = None

	event['location'] = event_location
	
	try:
	#eventContact
		event_contact = text[text.index("Contact Information:") + len("Contact Information:"): text.index("Event Type")]
		event_contact = event_contact.strip()
	except Exception as e:
		event_contact = None

	event['contact'] = event_contact
		
	try:
	#eventType
		event_type = text[text.index("Event Type") + len("Event Type"): text.index("Select item(s)")]
		event_type = event_type.strip()
	except Exception as e:
		event_type = None

	event['type'] = event_type
	
	database['events'][event_id] = event

	#print(event_type)

import json
with open('events.json', 'w') as outfile:
    json.dump(database, outfile)