# -*- coding: utf-8 -*-
import datetime
from time import gmtime, strftime
from bs4 import BeautifulSoup
import requests

MONTHS = {'январ': 'january', 'феврал': 'february', 'март': 'march', 'апрел': 'april',
          'ма': 'may', 'июн': 'june', 'июл': 'july', 'август': 'august',
          'сентябр': 'september', 'октябр': 'october', 'ноябр': 'november', 'декабр': 'december'
          }
SITE = 'https://pogoda.mail.ru/prognoz/chelyabinsk/'
CURRENT_YEAR = strftime("%Y", gmtime())


class WeatherMaker:
    def __init__(self, month=None, year=CURRENT_YEAR):
        self.month = month
        self.year = year
        self.forecasts = {}

    def weather_parser(self):
        # Парсинг с сайта дней, температуры, погоды и занесение данных в словарь
        if self.month is None:
            month = strftime("%B", gmtime()).lower()
        else:
            month = MONTHS[self.month[:-1]]
        response = requests.get(f'{SITE}{month}-{self.year}')
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            days_months = html_doc.find_all('div', 'day__date')
            temperatures_days = html_doc.find_all('div', 'day__temperature')
            weathers_days = html_doc.find_all('div', 'day__description')
            for day, temperature, weather in zip(days_months, temperatures_days, weathers_days):
                day = day.text.lower()
                day_datetime, day_rus = self.date_conversion(day)
                temperature = temperature.text.split()[0][:-1]
                weather = weather.text.strip().capitalize()
                self.forecasts[day_datetime] = {'Дата': day_rus, 'Погода': weather, 'Температура': temperature}
        return self.forecasts

    def date_conversion(self, day):
        # Для удобства чтения изменяется месяц на русский язык
        if day.startswith('с'):
            day = day[8:]
        day_rus = day
        for month_rus in MONTHS.keys():
            if day.find(month_rus) != -1:
                day = day.replace(month_rus, MONTHS[month_rus])
                break
        day = day[:-6] + day[-5:]
        day_datetime = datetime.datetime.strptime(day, '%d %B %Y')
        return day_datetime, day_rus
