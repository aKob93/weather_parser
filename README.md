# Парсер погоды с занесением результатов в базу данных и рисованием открытки с погодой за выбранный диапозон дат.

Описание
----
Программа парсит погоду с сайта https://pogoda.mail.ru для города Челябинск, по умолчанию в базу данных заносится погода за прошедшую неделю, также на выбор можно заносить погоду в базу данных, вывести на консоль прогноз, либо создать открытку из прогноза.

Результат работы
-----
<h3>Добавление прогноза в бд за выбранную дату</h3>
<p>Для парсинга используется библиотека BeatifulSoup</p>
<p>Работа с базой данных через ORM Peewee</p>

![Start](https://i.ibb.co/47dqgGn/1.gif)




<h3>Вывод прогноза из бд на консоль</h3>

![weather](https://i.ibb.co/yRckMLx/2.gif)




<h3>Создание открыток с прогнозом за диапозон дат</h3>
<p>Создание картинок происходит через библиотеку OpenCV</p>

![postcard](https://i.ibb.co/VSpwmLm/3.gif)



Пример открытки:

![postcard](https://i.ibb.co/6BJZJnp/weather-image-19-January.jpg)
