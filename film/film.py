from csv import DictReader
import random 
import os

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

print('Здравствуйте уважаемая Юлия!\nПожалуйста, выберите жанр.\n')

for key, value in genre_russian.items():
	print(key, value)


choice = input('\nВведиде номер жанра: ')

films_file = str(os.getcwd()) + '/film/film/films.tsv'

with open(films_file, 'r') as f:
	movies = [film for film in f if genre[choice] in film]
	
choice = 'y'
while 'y' in choice:
	print('\nСоветую этот фильм.\n')
	print(random.choice(movies))
	choice = input('Найти другую?("y/n"): ')		
	









