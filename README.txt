1. Описание бота ВК:
  1.1. Пользователь - пользователь ВК, который получает информацию о кандидатах в чат.

  1.2. Принцип работы бота строится на поиске пользователей ВК, удовлетворяющих заданным условиям при запуске приложения и у которых в их профиле пользователя имеется как минимум одно фото (далее - кандидат). Пользователи ВК, неудовлетворяющие заданным критериям поиска или не имющие ни одного фото в профиле, не являются кандидатами и информация о них не отправляется в чат Пользователю, но их ID также сохраняются для истории поиска (далее - не_кандидат).

  1.3. ID пользователей ВК выбираются случайно и сравниваются с базой поиска, которая ведется в Postgres, сохраняет ID пользователей ВК, сгенерированные в ходе работы приложения, и используется для исключения повторной проверки кандидатов.

2. Результатом работы бота являются:
  2.1. Формирование и отправка сообщения в чат пользователю со сслыкой на страницу кандидата ВК, удовлетворяющего заданным условиям поиска, и от 1 до 3 фото из альбома профиля этого кандидата с наибольшим количеством лайков (в зависимости от количества фото в альбоме);
  2.2. Добавление в базу данных ID кандидатов и пользователей ВК, которые были проанализорованы приложением в ходе работы

3. Функционирование бота.
  
  3.1. Подготовительный этап.

 - 3.1.1. Для корректной работы бота необходимо предоставить разрешения на отправку сообщений. Для этого со стороны пользователя необходимо инициировать переписку с сообществом https://vk.com/club209727143, отправив произвольное сообщение в сообщество.
 - 3.1.2. Создать базу данных в Postgres SQL.
 - 3.1.3. Создать в созданной в п.3.1.2 базе данных необходимую таблицу (код для создания таблицы в функции create_table модуля SqlWork.py)

  3.2.Основной этап.
 - 3.2.1. Запустить приложение
 - 3.2.2. Ввести ID пользователя, который ранее дал права на отправку сообщений (п. 3.1.1.)
 - 3.2.3. Опционально: ввести имя пользователя (по умолчанию - не указано).
 - 3.2.4. Опционально: ввести дополнительные параметры поиска; по умолчанию параметры следующие:
	- минимальный возраст - 18 лет;
	- максимальный возраст - 65 лет;
	- пол не указан (не имеет значения для алгоритма подбора кандидата);
	- родной город не указан (не имеет значения для алгоритма подбора кандидата);
	- семейное положение не указано (не имеет значения для алгоритма подбора кандидата);
 - 3.2.5. Указать количество пользователей ВК для поиска (учитывая п. 1.2., для получения ожидаемого результата работы минимальное количество пользователей в диапазоне от 5 до 10).