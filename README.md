# test_HQ_API

Данный API-сервис был разаработан в качестве тестового задания с использованием Django Rest Framwork.

Версия python >= 3.8.

После того, как проект скачан, необходимо перейти в директорию проекта (Пример : C:\ ... \test_HQ_API
).


1) Перед тем, как запустить сервер, необходимо установить необходимые библиотеки с помощью команды:

    `pip install -r requirements.txt`
	или
	`pip3 install -r requirements.txt` в зависимости от ОС


2) Если необходимо загрузить тестовые экзмепляры продуктов, уроков и групп, то воспользоваться функциями:

    `python manage.py loaddata main/fixtures/groups.json`,

    `python manage.py loaddata main/fixtures/lessons.json`,

    `python manage.py loaddata main/fixtures/prod.json`, соответственно каждой таблице.


3) Создаем миграции:

    `python manage.py makemigrations`


3) Мигрируем:

    `python manage.py migrate`


4) Создаем суперюзера для доступа к админ панели (http://localhost:8000/admin или http://127.0.0.1:8000/admin):

    `python manage.py createsuperuser`


5) Запускаем сервер с помощью команды или дебагера Ctrl+F5 (создав конгфигурацию для запуска проектов на Django):

    `python manage.py runserver`


6) Авторизуемся:

    http://localhost:8000/api-auth/login/


7) Есть базовые URLs:

    https://localhost:8000/api/v1/ - Основные ссылки для получения списков по каждому классу (RESTfull)

    "all_products": "http://localhost:8000/api/v1/all_products/" - все существующие продукты,

    "lessons": "http://localhost:8000/api/v1/lessons/" - все существующие уроки,

    "all_users": "http://localhost:8000/api/v1/all_users/" - все пользователи,

    "buyed_users": "http://localhost:8000/api/v1/buyed_users/" - все пользователи, купившие продукт,

    "groups": "http://localhost:8000/api/v1/groups/" - все группы по продуктам

8) Дополнительный функционал по поставленным задачам:


    1* При получении доступа к продукту, распределение пользователя в группу происходит с помощью сигнала main\signals.py.

    http://localhost:8000/api/v1/available_products/ - 2* получение продуктов, доступных для покупки, которое бы включает в себя основную информацию о продукте и уроки, которые принадлежат продукту.

    http://localhost:8000/api/v1/login/lessons/product_id/<int:product_id>/ - 3* получение доступных пользователю уроков, где product_id это ID продукта
    (доступ только у авторизованных пользователей).

    http://localhost:8000/api/v1/users_count/ - 1** получение количество учеников занимающихся на киждом из продуктов.

    http://localhost:8000/api/v1/product_statistic/<int:pk>/ - 2** получение процента заполнения групп по проекту, где pk это ID продукта.

    http://localhost:8000/api/v1/purchase_percent/ - 3** получение процента приобретения по каждому из продуктов

    
    Примечание: * - выполнение задач по второму пункту "Написание запросов и реализация логики распределения",
    ** - выполнение дополнительных задач "Реализование API для отображения статистики по продуктам. "
