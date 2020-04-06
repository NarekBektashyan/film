from csv import DictReader
import random 
import os
import requests
from colorama import Fore, Style



kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')	
header = {
	'x-fx-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImp0aSI6ImZ4LTVlOGFkNmVmMDY4OGMifQ.eyJpc3MiOiJodHRwczpcL1wvZmlsbWl4Lm1lIiwiYXVkIjoiaHR0cHM6XC9cL2ZpbG1peC5tZSIsImp0aSI6ImZ4LTVlOGFkNmVmMDY4OGMiLCJpYXQiOjE1ODYxNTcyOTUsIm5iZiI6MTU4NjE0NjQ5NSwiZXhwIjoxNTg4NzQ5Mjk1LCJwYXJ0bmVyX2lkIjoiMiIsImhhc2giOiIyMWZiYjI1NTM5ZTg2OTQzMDg1M2M4YjExZGY0MTZhOTkxODZlZjhjIiwidXNlcl9pZCI6bnVsbCwiaXNfcHJvIjpmYWxzZSwiaXNfcHJvX3BsdXMiOmZhbHNlLCJzZXJ2ZXIiOiIifQ.gCUVS0Mj4i63wAzfeDq-Vnap5pUTFFDRCE9pCz0VY6U'
	
}

genre = {
	 '1':'Drama','2': 'Comedy','3': 'Thriller', '4': 'Action', '5': 'Crime',
	 '6': 'Adventure', '7': 'Mystery', '8': 'Fantasy', '9': 'Sci-Fi', '10': 'History',
	 '11': 'Biography','12': 'War', '13': 'Documentary', 
}

genre_russian = {
	'1': 'Драма', '2': 'Комедия', '3': 'Триллер', '4': 'Боевик','5': 'Криминалная',
	'6': 'Приключения', '7': 'Мистика', '8': 'Фантастика','9': 'Научная фантастика',
	'10': 'Историческая', '11': 'Биография', '12': 'Военная', '13': 'Документальная'
}

def translate_title(title, year):
	title = '+'.join(title.split())
	year = str(year)
	res = requests.get(f'https://ru.wikipedia.org/w/index.php?search={title}+фильм%2C{year}')
	res = res.text.split('<')
	new = [x for x in res if 'data-serp-pos' in x ]
	link = new[0].split('"')[1]
	res = requests.get('https://ru.wikipedia.org' + link)
	title = [x for x in res.text.split('\n') if 'title' in x]
	title_html = title[0]
	while '<' in title_html:
		start = title_html.find('<')
		stop = title_html.find('>')
		if start != -1:
			title_html = title_html[:start] + title_html[stop+1:]
	cleantext = title_html
	start = cleantext.find( '(' )
	if start != -1:
 		cleantext = cleantext[:start]
	if cleantext.find('—') > 0:
		cleantext = cleantext.replace('—', '')
	if cleantext.find('Википедия') > 0:
		cleantext = cleantext.replace('Википедия', '')	
	title = cleantext.strip()
	return title

def get_description(title):
	res = requests.get(f'http://85.239.42.191/partner_api/suggests?query={title}', headers=header)
	res = res.json()
	movie_id = str([x for  x in res['items'] if x['title'] == title][0]['id'])
	details = requests.get(f'http://85.239.42.191/partner_api/film/{movie_id}/details', headers=header)
	description = details.json()['short_story']
	while '<' in description:
		start = description.find('<')
		stop = description.find('>')
		if start != -1:
			description = description[:start] + description[stop+1:]
	return description

choice = '1'

films_file = str(os.getcwd()) + '/film/film/films.tsv'

with open(films_file, 'r') as f:
	movies = [film for film in f if genre[choice] in film]
	
choice = 'y'

while choice != 'q':
	print('Пожалуйста, выберите жанр.\n')
	for key, value in genre_russian.items():
		print(key, value)
	choice = input('\nВведиде номер жанра: ')	
	while not 'n' in choice and not 'g' in choice:
		movie = random.choice(movies)
		title, year = movie.split(',')[:2]
		title = '+'.join(title.split())
		year = str(year)
		title = translate_title(title, year)
		find_kirill = [x for x in kirill if x in title.lower()]
		if not find_kirill:
			continue
		try:
			description = get_description(title)
			print('\nСоветую этот фильм.\n')
			print(Fore.GREEN + title + ', ' + year)
			print()
			print(Style.RESET_ALL)
			print(description)
		except Exception:
			continue
		choice = input('\nНайти другую?("y/n")Менять жанр("g"): ')		
	
