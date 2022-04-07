# -*- coding: utf-8 -*-
import datetime
import time

MONTHS = {'январь': '1', 'февраль': '2', 'март': '3', 'апрель': '4', 'май': '5', 'июнь': '6', 'июль': '7',
          'август': '8',
          'сентябрь': '9', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'}


def get_date_last_week():
    # Получение точной даты недельной давности
    days_week = 7
    date_week_ago = datetime.date.today() - datetime.timedelta(weeks=1, days=0)
    year = date_week_ago.year
    month = date_week_ago.month
    day = date_week_ago.day
    return year, month, day, days_week


def get_handle_date():
    # Запрос даты у пользователя
    while True:
        input_year = input('Введите желаемый год числом:')
        input_month = input('Введите желаемый месяц словом:').lower()
        input_day = input('Введите желаемый день числом:')
        if input_month in MONTHS:
            input_date = f'{input_year} {MONTHS[input_month]} {input_day}'
            try:
                time.strptime(input_date, '%Y %m %d')
                return int(input_year), int(MONTHS[input_month]), int(input_day), input_month
            except ValueError:
                print('Не верно введены год или день')
        else:
            print('Не верно введен месяц')


def get_forecast_period():
    # Запрос периода дней
    while True:
        range_choice = input('Введите числом количество дней для прогноза погоды(до 5 дней):')
        try:
            if 0 < int(range_choice) <= 5:
                return int(range_choice)
            else:
                print('Количество дней не попадает в обозначенный период')
        except ValueError:
            print('Не верный формат дней')
