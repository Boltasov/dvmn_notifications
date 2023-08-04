# Скачивание книг

Программа предназначена для отправления в telegram уведомлений о проверке ваших работ на курсах Devman.

### Как установить

Должны быть предустановлены Python 3 и pip.

Скачайте код с помощью команды в командной строке
```commandline
https://github.com/Boltasov/dvmn_notifications
```
Перейдите в папку с проектом
```commandline
cd dvmn_notifications
```
Установите необходимые библиотеки командой
```
python pip install -r requirements.txt
```
### Как запустить
1) Получите ваш ключ для сайта Devman [здесь](https://dvmn.org/api/docs/). По нему отслеживаются ваши работы.
2) Создайте телеграм-бота и получите ключ для него. Для этого: напишите [Отцу ботов](https://telegram.me/BotFather), введите в него команду `/start`, введите команду `/newbot` создайте бота. Ключ выглядит так: `95132391:wP3db3301vnrob33BZdb33KwP3db3F1I`
3) Создайте документ `.env`, в который поместите эти ключи в соответствии с примером:
```text
DVMN_KEY='Put_here_your_devman_key'
TG_BOT_KEY='Put_here_your_telegram_bot_key'
```

Для запуска будет необходимо указать ваш chat_id в Telegram, чтобы уведомления приходили именно вам. Чтобы получить свой chat_id, напишите в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot).

Теперь запустите программу с указанием вашего chat_id:
```commandline
python main.py --chat_id=ВАШ_CHAT_ID
```

Теперь, пока программа запущена, ваш бот будет публиковать сообщения при появлении новых проверок работ.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).