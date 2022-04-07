# -*- coding: utf-8 -*-
import os
import cv2

WEATHERS = {
    'Ясно': {'Цвет': (0, 255, 255),
             'Путь до изображения': 'weather_icons/sun_icons.png'},
    'Дождь': {'Цвет': (255, 0, 0),
              'Путь до изображения': 'weather_icons/rain_icons.png'},
    'Снег': {'Цвет': (255, 255, 0),
             'Путь до изображения': 'weather_icons/snow_icons.png'},
    'Облачно': {'Цвет': (50, 50, 50),
                'Путь до изображения': 'weather_icons/cloud_icons.png'},
    'Дождь\гроза': {'Цвет': (0, 0, 0),
                    'Путь до изображения': 'weather_icons/thunderstorm_icons.png'},
    'Осадки': {'Цвет': (255, 255, 0),
               'Путь до изображения': 'weather_icons/precipitation_icons.png'},
    'Метель': {'Цвет': (255, 0, 0),
               'Путь до изображения': 'weather_icons/snowstorm_icons.png'}
}

BLANK_IMAGE = 'weather_icons/probe.jpg'
# Параметры изображения
FONT = cv2.FONT_HERSHEY_COMPLEX
FONT_SIZE_DATE = 1
FONT_SIZE = 0.8
FONT_COLOR_DATE = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
THICKNESS_TEXT = 2
TEXT_POSITION_DATE = (130, 40)
TEXT_POSITION_WEATHER = (230, 130)
TEXT_POSITION_TEMP = (230, 160)


class ImageMaker:
    def __init__(self, date, temp, weather):
        self.date = date
        self.temp = temp
        self.weather = weather
        self.image_postcard = None
        self.weather_icon = None

    def read_image(self):
        # Открытие нужных файлов для создания изображения
        self.image_postcard = cv2.imread(BLANK_IMAGE)
        self.weather_icon = cv2.imread(WEATHERS[self.weather]['Путь до изображения'])

    def paint_background_gradient(self):
        # Рисование градиента в засимости от погоды
        height_width = self.image_postcard.shape
        b, g, r = WEATHERS[self.weather]['Цвет']

        for i in range(height_width[0]):
            if b < 255:
                b += 1
            if g < 255:
                g += 1
            if r < 255:
                r += 1

            cv2.line(self.image_postcard, (0, i), (height_width[1], i), (b, g, r), 1)
        return self.image_postcard

    def paint_icons(self):
        # Размещение иконки погоды на изображении
        # I want to put logo on top-left corner, So I create a ROI
        rows, cols, channels = self.weather_icon.shape
        roi = self.image_postcard[100:100 + rows, 100:100 + cols]
        # Now create a mask of logo and create its inverse mask also
        img_icon = cv2.cvtColor(self.weather_icon, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img_icon, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img_background = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # Take only region of logo from logo image.
        img_frontground = cv2.bitwise_and(self.weather_icon, self.weather_icon, mask=mask)
        # Put logo in ROI and modify the main image
        dst = cv2.add(img_background, img_frontground)
        self.image_postcard[100:100 + rows, 100:100 + cols] = dst
        return self.image_postcard

    def paint_text(self):
        # Написание даты, погоды и температуры на изображении
        cv2.putText(self.image_postcard, self.date, TEXT_POSITION_DATE, FONT, FONT_SIZE_DATE, FONT_COLOR_DATE,
                    THICKNESS_TEXT)
        cv2.putText(self.image_postcard, self.weather, TEXT_POSITION_WEATHER, FONT, FONT_SIZE, FONT_COLOR,
                    THICKNESS_TEXT)
        cv2.putText(self.image_postcard, self.temp, TEXT_POSITION_TEMP, FONT, FONT_SIZE, FONT_COLOR, THICKNESS_TEXT)
        return self.image_postcard

    def save_postcard(self, name_image):
        # Сохранение открытки
        os.makedirs('weather_images', exist_ok=True)
        file_image = 'weather_image_' + str(name_image) + '.jpg'
        with open(f'weather_images/{file_image}', 'w'):
            cv2.imwrite(f'weather_images/{file_image}', self.image_postcard)

    def run(self, name_image):
        # Запуск рисования открытки
        self.read_image()
        self.paint_background_gradient()
        self.paint_icons()
        self.paint_text()
        self.save_postcard(name_image)
