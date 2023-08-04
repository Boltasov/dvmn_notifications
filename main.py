import os
import json
import time
import argparse
import requests

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, CallbackContext, CommandHandler


def main():
    parser = argparse.ArgumentParser(
        prog='DvmnNotifier',
        description='Скрипт присылает уведомления о проверенных в devman работах в телеграм-бот.',
    )
    parser.add_argument("--chat_id", help='Ваш chat_id в telegram', type=int, required=True)
    args = parser.parse_args()

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
            continue
        except requests.ConnectionError:
            time.sleep(10)
            continue

        response.raise_for_status()

        updates = response.json()
        params['timestamp'] = updates['last_attempt_timestamp']
        attempts = updates['new_attempts']
        for attempt in attempts:
            lesson_title = attempt['lesson_title']
            mistakes = attempt['is_negative']
            lesson_url =  attempt['lesson_url']
            if mistakes:
                message_text = f'У вас проверили работу "{lesson_title}"\n\n' \
                               f'К сожалению, в работе нашли ошибки.\n\n' \
                               f'Ссылка на урок: {lesson_url}'
            else:
                message_text = f'У вас проверили работу "{lesson_title}"\n\n' \
                               f'Преподавателю всё понравилось. Можно приступать к следующему уроку!'

            bot.send_message(text=message_text, chat_id=args.chat_id)


if __name__ == '__main__':
    main()
