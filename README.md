# Weather Bot
Weather Bot stands as an advanced Telegram bot meticulously crafted in Python,
leveraging the powerful capabilities of the aiogram framework. At its core,
the project seamlessly integrates a robust SQLite database and the versatility
of the SQLAlchemy ORM framework to ensure optimal data management and storage efficiency.
Through its dynamic interaction with the weatherapi.com API,
the bot emerges as a reliable source, delivering precise 
and real-time weather forecasts for a diverse array of cities across Ukraine.

## Содержание
- [Technologies](#Technologies)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-ci/cd)
- [Contributing](#contributing)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Technologies
- [Aiogram](https://docs.aiogram.dev/)
- [SQLite](https://www.sqlite.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Использование
Расскажите как установить и использовать ваш проект, покажите пример кода:

Установите npm-пакет с помощью команды:
```sh
$ npm i your-awesome-plugin-name
```

И добавьте в свой проект:
```typescript
import { hi } from "your-awesome-plugin-name";

hi(); // Выведет в консоль "Привет!"
```

## Разработка

### Требования
Для установки и запуска проекта, необходим [NodeJS](https://nodejs.org/) v8+.

### Установка зависимостей
Для установки зависимостей, выполните команду:
```sh
$ npm i
```


### Создание билда
Чтобы выполнить production сборку, выполните команду: 
```sh
npm run build
```

## Тестирование
Какие инструменты тестирования использованы в проекте и как их запускать. Например:

Наш проект покрыт юнит-тестами Jest. Для их запуска выполните команду:
```sh
npm run test
```. 