GoIT, Python WEB, Homework number 10. Django. PostgreSQL. Docker. MongoDB. 

# Домашнє завдання #10

У минулій домашній роботі ви виконували скрапінг сайту http://quotes.toscrape.com.

Вам необхідно самостійно реалізувати аналог такого сайту на Django.

1. Реалізуйте можливість реєстрації на сайті та вхід на сайт.
2. Можливість додавання нового автора на сайт лише для зареєстрованого користувача.
3. Можливість додавання нової цитати на сайт із зазначенням автора тільки для зареєстрованого користувача.
4. Виконайте міграцію бази даних із MongoDB, яка у вас є, у Postgres для вашого сайту. Можна реалізувати кастомним скриптом. (За бажанням можете залишити та працювати з цитатами та авторами в MongoDB, а з користувачами у Postgres)
5. Можна зайти на сторінку кожного автора без автентифікації користувача
6. Усі цитати доступні для перегляду без автентифікації користувача

## Додаткова частина

1. Реалізуйте пошук цитат за тегами. При натисканні на тег, виводиться список цитат з цим тегом.
2. Реалізуйте блок "Top Ten tags" та виведення найпопулярніших тегів.
3. Реалізуйте пагінацію. Це кнопки next та previous
4. Замість перенесення даних з бази даних MongoDB, реалізуйте можливість скрапінгу даних прямо з вашого сайту по натисканню певної кнопки на формі та наповнення бази даних сайту.


# Частина:  Домашнє завдання #13

У цьому домашньому завданні необхідно доопрацювати застосунок Django із домашнього завдання 10.



## Завдання


- Реалізуйте механізм скидання паролю для зареєстрованого користувача;
- Усі змінні середовища повинні зберігатися у файлі .env та використовуватися у файлі settings.py

