import urllib.request
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

now = datetime.now()
strnow = str(now)
strnow = strnow.split(' ')[0].split('-')
yy, mm, dd = strnow

end = now + timedelta(days = 30)
strEnd = str(end)
strEnd = strEnd.split(' ')[0].split('-')
ey, em, ed = strEnd

quote_page = 'https://events.sjsu.edu/EventList.aspx?fromdate='+mm+'%2f'+dd+'%2f'+yy+'&todate='+em+'%2f'+ed+'%2f'+ey


page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

table = soup.find('table', attrs= {'id':'tblEvents'})



#for dates in table.find_all('h4', attrs={'class':'adx_wcag_header'}):
	#date = dates.text
	#print(date)
	
#Getting the links for each event
for titles in table.find_all('div', attrs={'class':'vevent'}):
	title = titles.find('a', attrs={'class':'url summary'})['href']
	#print(title)
	new_page = 'https://events.sjsu.edu/'+str(title)
	
	pg = urllib.request.urlopen(new_page)
	new_soup = BeautifulSoup(pg, 'html.parser')
	
	data = new_soup.find('table',attrs={'id':'PageTable'})
	name = data.find('td', attrs={'class':'listheadtext'}).text
	print(name)
	
	
	
	
	
		
	
	
	
