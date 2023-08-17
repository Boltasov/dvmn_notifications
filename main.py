import os
import time
import argparse
import requests
import logging

from dotenv import load_dotenv
from telegram import Bot
from textwrap import dedent


class MyLogsHandler(logging.Handler):
    load_dotenv()

    tg_bot_key = os.getenv('LOG_BOT_KEY')
    log_bot = Bot(token=tg_bot_key)
    chat_id = ''

    def __init__(self, chat_id):
        super().__init__()
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.log_bot.send_message(text=log_entry, chat_id=self.chat_id)


def main():
    parser = argparse.ArgumentParser(
        prog='DvmnNotifier',
        description='Скрипт присылает уведомления о проверенных в devman работах в телеграм-бот.',
    )
    parser.add_argument("--chat_id", help='Ваш chat_id в telegram', type=int, required=True)
    args = parser.parse_args()

    logger = logging.getLogger("TG logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(chat_id=args.chat_id))
    logger.info('Бот запустился. Всё идёт по плану.')

    load_dotenv()

    dvmn_key = os.getenv('DVMN_KEY')
    tg_bot_key = os.getenv('TG_BOT_KEY')

    bot = Bot(token=tg_bot_key)

    header = {
        'Authorization': f'Token {dvmn_key}',
    }

    polling_url = 'https://dvmn.org/api/long_polling/'

    params = {}

    while True:
        try:
            response = requests.get(polling_url, headers=header, params=params, timeout=30)
        except requests.exceptions.ReadTimeout:
            logger.warning('ReadTimeout. Продолжаю ждать ответа.')
            continue
        except requests.ConnectionError:
            logger.warning('Ошибка соединения. Попытка восстановить связь.')
            time.sleep(10)
            continue

        response.raise_for_status()

        updates = response.json()
        status = updates['status']
        if status == 'found':
            params['timestamp'] = updates['last_attempt_timestamp']
        elif status == 'timeout':
            params['timestamp'] = updates['timestamp_to_request']
            continue
        else:
            continue

        attempts = updates['new_attempts']
        for attempt in attempts:
            lesson_title = attempt['lesson_title']
            mistakes = attempt['is_negative']
            lesson_url = attempt['lesson_url']
            if mistakes:
                message_text = f'''\
                У вас проверили работу "{lesson_title}"
                К сожалению, в работе нашли ошибки.
                Ссылка на урок: {lesson_url}'''
            else:
                message_text = f'''\
                У вас проверили работу "{lesson_title}"
                Преподавателю всё понравилось. Можно приступать к следующему уроку!'''

            bot.send_message(text=dedent(message_text), chat_id=args.chat_id)

        logger.info('Отправил обновления по проверенным задачам. Всё идёт по плану.')


if __name__ == '__main__':
    main()
