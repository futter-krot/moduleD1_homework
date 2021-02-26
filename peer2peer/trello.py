# ПРИЛОЖЕНИЕ РАБОТАЕТ ЧЕРЕЗ ЛЮБОЙ ТЕРМИНАЛ(VS CODE, CMD...)
# РАБОТА С ЗАДАЧЕЙ СОВЕРШАЕТСЯ ЛИШЬ В ФУНЦИИ move(), ВСЕ ОСТАЛЬНЫЕ ФУНКЦИИ НЕ ИМЕЮТ РАБОТЫ С ЗАДАЧАМИ, ДЛЯ ПРОВЕРКИ 3 ПУНКТА УСЛОВИЯ НЕОБХОДИМО ИСПОЛЬЗОВАТЬ move() см. строку 60.
import requests, sys
login = str(input("ВВЕДИТЕ В ПОЛЕ: 'КЛЮЧ, ТОКЕН, BOARD_ID' - С ПРОБЕЛАМИ; БЕЗ ЗНАКОВ ПРЕПИНАНИЯ И КАВЫЧЕК")).split() #ПРИМЕР ЛОГИНА: 769392e0cb908d32412f786735929 c5593eff41f41eb5f03e0d6717f89b69135638900821270b6d7d5e2cea8f4 Ba34eJh1
auth_params = {    
    'key': "{}".format(login[0]), # ГЕНЕРИРУЕМ СЛОВАРЬ НА ЛОГИНЕ
    'token': "{}".format(login[1]), 
    }  
base_url = "https://api.trello.com/1/{}" 
board_id = "{}".format(login[2]) # ГЕНЕРИРУЕМ BOARD_ID НА ЛОГИНЕ
def read():
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
		column_name = column['name'] + ': ' + str(len(task_data)) # СЧЁТЧИК ЗАДАЧ
		print(column_name)
		if not task_data:
			print('\t' + 'Нет задач!')
			continue
		for task in task_data:
			print('\t' + task['name'])
def create(name, column_name):
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		if column['name'] == column_name:
			requests.post(base_url.format("cards"), data={'name': name, 'idList': column['id'], **auth_params})
			break
def colreate(column_name): # ФУНКЦИЯ СОЗДАЕТ НОВУЮ КОЛОНКУ, ПРИНИМАЕТ НАЗВАНИЕ КОЛОНКИ (COLUMN + CREATE = COLREATE)
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		if column['name'] != column_name:
			requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': column['idBoard'], **auth_params})
			break
		else:
			print("A column with the same name already exists. Column was not created.")
			break
def move(name, column_name):
	tasklist = [] # СПИСОК, В КОТОРЫЙ БУДЕМ КЛАСТЬ ID ТАСКОВ
	collist = [] # СПИСОК, В КОТОРЫЙ БУДЕМ КЛАСТЬ ID КОЛОНОК
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
		for task in column_tasks:
			if task['name'] == name:
				tasklist.append(task["id"])
				collist.append(column["name"])
	for column in column_data:
		if column['name'] == column_name:
			print("Задача 1 находится в колонке '{0}', её id={1}; Задача 2 находится в колонке '{2}', её id={3}".format(collist[0], tasklist[0], collist[1], tasklist[1]))
			a = int(input("Какое значение вам необходимо переместить? (1 или 2)")) # ФУНКЦИЯ НЕ РАБОТАЕТ НА 3 И БОЛЕЕ ЭЛЕМЕНТАХ (ПО УСЛОВИЮ ЗАДАНИЯ)
			if a == 1:
				requests.put(base_url.format('cards') + '/' + tasklist[0] + '/idList', data={'value': column['id'], **auth_params})
				break
			elif a == 2:
				requests.put(base_url.format('cards') + '/' + tasklist[1] + '/idList', data={'value': column['id'], **auth_params})
				break
			else:
				break
if __name__ == "__main__":
	# <-- СЮДА МОЖНО ВСТАВЛЯТЬ ФУНКЦИИ ДЛЯ ТЕСТОВ. ПРИМЕРЫ ТЕСТОВ: colreate("На будущее"), move("Изучить Python", "В процессе")
	if len(sys.argv) <= 2:
		read()
	elif sys.argv[1] == 'colreate':
		colreate(sys.argv[2])
	elif sys.argv[1] == 'create':
		create(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == 'move':
		move(sys.argv[2], sys.argv[3])
# СПАСИБО ЗА ПРОВЕРКУ
