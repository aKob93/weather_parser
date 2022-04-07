# -*- coding: utf-8 -*-
from pars import WeatherMaker
from paint import ImageMaker
from database import DatabaseUpdate
from data_request import get_date_last_week, get_handle_date, get_forecast_period


def main():
    forecast_last_week = WeatherMaker()
    forecast_last_week.weather_parser()
    forecast_base = DatabaseUpdate(forecast_last_week.forecasts)
    year, month, day, days_week = get_date_last_week()
    forecast_base.save_forecast(year=year, month=month, day=day, time_range=days_week)

    exit_status = False
    while not exit_status:
        choice = input(
            'Выбрать действие: \n1. Добавить прогноз за диапазон дат в базу данных(не позже текущего месяца). '
            '\n2. Получить прогноз за диапозон дат из базы данных. '
            '\nИначе - завершение программы: ')
        if choice == '1':
            print('Занесение прогноза в базу данных.')
            year, month, day, month_rus = get_handle_date()
            time_range = get_forecast_period()
            forecast_selected_date = WeatherMaker(month=month_rus, year=year)
            forecast_selected_date.weather_parser()
            forecast_base = DatabaseUpdate(forecast_selected_date.forecasts)
            if forecast_base.save_forecast(year=year, month=month, day=day, time_range=time_range):
                print(f'Прогноз с выбранной даты({day}-{month}-{year}) на {time_range} дн. занесён в базу данных')
            else:
                print('Нет прогноза на этот период')
        elif choice == '2':
            print('Получение прогноза из базы данных.')
            year, month, day, month_rus = get_handle_date()
            time_range = get_forecast_period()
            forecast_list = forecast_base.get_forecast(year, month, day, time_range)
            if forecast_list:
                output_choice = input('Выберите действие: 1. создать открытку из прогноза.'
                                      ' 2. Вывести прогноз на консоль.:')
                if output_choice == '1':
                    print()
                    for day_forecast in forecast_list:
                        name_image = f'{day_forecast[0].strftime("%d")}_{day_forecast[0].strftime("%B")}'
                        im = ImageMaker(day_forecast[1], day_forecast[2], day_forecast[3])
                        im.run(name_image)
                    print('Открытки сохранены в папке weather_images в файлах weather_img_*дата*.jpg')
                elif output_choice == '2':
                    for day_forecast in forecast_list:
                        print(
                            f'Прогноз на {day_forecast[1]}: {day_forecast[2]},  {day_forecast[3]}.')
                else:
                    print('Неверный выбор.')
            else:
                print('Прогноза на этот период нет в базе')
        else:
            exit_status = True
            print('Конец работы.')


if __name__ == '__main__':
    main()
