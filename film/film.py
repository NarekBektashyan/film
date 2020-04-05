from csv import DictReader
import random 
import os
import requests
import wikipedia
from colorama import Fore, Style

kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')	
movie = wikipedia.set_lang('ru')

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
		res = requests.get(f'https://ru.wikipedia.org/w/index.php?search={title}%2C{year}')

		res = res.text.split('<')

		new = [x for x in res if 'data-serp-pos' in x ]

		link = new[0].split('"')[1]
		res = requests.get('https://ru.wikipedia.org' + link)
		title = [x for x in res.text.split('<') if 'title' in x]
		title = title[0].split('>')[1].split('—')[0]
		find_kirill = [x for x in kirill if x in title.lower()]
		if not find_kirill:
			continue
		description = wikipedia.summary(f"{title}(фильм)")
		print('\nСоветую этот фильм.\n')
		print(Fore.GREEN + title + ', ' + year)
		print()
		print(Style.RESET_ALL)
		print(description)
		choice = input('\nНайти другую?("y/n")Менять жанр("g"): ')		
		
