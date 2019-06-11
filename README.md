# Support-Bot
Бот моментально отвечает на вопросы пользователей, задаваемые в чатах Telegram и VK.

![](bot_sample.gif)
### Как установить 
Должен быть установлен `python3`. Затем используйте `pip`(или `pip3`, 
 если есть конфликт с `Python2`) для установки зависимостей: 
 ```bash
 pip install -r requirements.txt
 ```
 
 
 ### Как настроить
 1. Создайте Telegram-бота и получите API-ключ. [Как обойти блокировку Telegram](https://bigpicture.ru/?p=913797),
[Как создать бота и получить токен](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)

    Создайте чат со своим ботом. 
    
    Узнайте свой id у бота в telegram `@userinfobot`

2. Создайте группу в VK. В настройках группы получите токен `Настройки > Работа с API` и 
разрешить боту отправлять сообщения `Настройки > Сообщения > Сообщения сообщества -> Включить`

3. Зарегистрируйте аккаунт [DialogFlow](https://dialogflow.com/)

    Создайте новый [Agent](https://dialogflow.com/docs/getting-started/first-agent#create_your_first_dialogflow_agent)

    Скачайте `GOOGLE_APPLICATION_CREDENTIALS.json`, используя [инструкцию](https://dialogflow.com/docs/reference/v2-auth-setup#getting_the_service_account_key)
    
    В настройках Agent узнайте id своего проекта

    Создайте файл в формате `json`, где будут вопросы, на которых будет обучаться бот, и ответы к ним.
Желательно на каждую тему задать минимум 10 вопросов. Расположите его в одной директории со скриптом `training_phrases.py`.
  
      Структура файла будет выглядить так:
```json
{
    "<Your intent name>": {
        "questions": [
            "...",
            "...",
            "..."
        ],
        "answer": "..."
    },
    "<Your intent name>": {
        "questions": [
            "...",
            "...",
            "..."
        ],
        "answer": "..."
    }
}
```

Создайте файл .env в корне проекта и запишите в него полученные токены:
```text
TELEGRAM_TOKEN=<your telegram-bot token>
VK_TOKEN=<your vk token>
DEVELOPER_ID=<your telegram id>
PROJECT_ID=<your dialogflow project id>
TRAINING_FILE_NAME=<training filename>
```

### Как запустить

Авторизоваться в Google
```bash
export GOOGLE_APPLICATION_CREDENTIALS='path_to_google_credentials_file.json'
```

Запустите тренировку бота, если он еще не обучен
```bash
python3 training_phrases.py
```  

Запустить Telegram-бота
```bash
python3 telegram_bot.py
```

Запустить VK-бота
```bash
python3 vk_bot.py
```

### Развертывание на Heroku
 Создайте приложение
 
 Установите переменные окружения, как в файле `.env`
 
 Создайте переменные окружения: `GOOGLE_CREDENTIALS` и скопируйте в неё всё, что находится в 
 вашем файле `GOOGLE_APLICATION_CREDENTIALS.json`; `GOOGLE_APPLICATION_CREDENTIALS` и запишите в неё `google-credentials.json`
 
 Прикрепите buildpack `https://github.com/elishaterada/heroku-google-application-credentials-buildpack.git`
 
 
 


