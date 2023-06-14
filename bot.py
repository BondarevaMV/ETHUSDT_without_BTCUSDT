import requests
import time

# Ключ АПИ, который должен добавить пользователь
api_key = ''


def find_percent(last_num, new_num):
	"""Функция, возращающая результат вычисления процента изменений"""
	return (new_num / last_num - 1) * 100


def get_request(params, url='/api/v3/ticker/price'):
	"""Функция возращающая результат GET-запроса"""

	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": "https://api4.binance.com"
	}

	try:
		response = requests.get(
			url,
			headers=headers,
			params=params,
			timeout=15
			)
		if response.status_code == requests.codes.ok:
			return response.text

	except Exception:
		print("Ошибка!")


# Переменные, которые сохраняют предыдущую цену
last_price_ETHUSDT = last_price_BTCUSDT = 0

while True:
	percent_hour_ETHUSDT = 0

	for _ in range(60):
		# Запрос к базе
		response_BTCUSDT = get_request(params='BTCUSDT')
		response_ETHUSDT = get_request(params='ETHUSDT')

		# Переменные, которые сохраняют новую цену(только что полученную)
		new_price_BTCUSDT = float(response_BTCUSDT['price'])
		new_price_ETHUSDT = float(response_ETHUSDT['price'])

		if last_price_BTCUSDT == 0:
			last_price_ETHUSDT = new_price_ETHUSDT
			last_price_BTCUSDT = new_price_BTCUSDT
		else:
			percent_hour_ETHUSDT += (find_percent(last_price_ETHUSDT, new_price_ETHUSDT) - find_percent(last_price_BTCUSDT, new_price_BTCUSDT))
			last_price_ETHUSDT = new_price_ETHUSDT
			last_price_BTCUSDT = new_price_BTCUSDT

		time.sleep(60)

	if percent_hour_ETHUSDT > 1:
		print(f'За последний час изменения составили больше 1%, а именно {percent_hour_ETHUSDT}')
