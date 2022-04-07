# -*- coding: utf-8 -*-
import datetime
from base import WeatherBase


class DatabaseUpdate:

    def __init__(self, weather_dict):
        self.weather_dict = weather_dict

    def save_forecast(self, year, month, day, time_range):
        # Сохранение прогноза в базу данных
        for day_counter in range(time_range):
            date_from = datetime.datetime(year=year, month=month, day=day)
            if date_from in self.weather_dict:
                temperature = self.weather_dict[date_from]['Температура']
                weather = self.weather_dict[date_from]['Погода']
                date_rus = self.weather_dict[date_from]['Дата']
                WeatherBase.create(
                    date=date_from,
                    date_rus=date_rus,
                    temperature=temperature,
                    weather=weather
                )
                day += 1
            else:
                return False
        return True

    def get_forecast(self, year, month, day, time_range):
        # Получаение прогноза из базы данных
        forecast_several_days = []
        for day_counter in range(time_range):

            for data in WeatherBase.select():
                date_from = datetime.datetime(year=year, month=month, day=day)
                if data.date == date_from:
                    data_forecast = [data.date, data.date_rus, data.temperature, data.weather]
                    forecast_several_days.append(data_forecast)
                    day += 1
        return forecast_several_days
