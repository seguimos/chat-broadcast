# Inspirado en el ejemplo de Gabriel Valvano:
#       https://github.com/gvalvano/telegram-notification
import requests
from logging import Handler, Formatter
import logging


class RequestsHandler(Handler):

    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': self.chat_id,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        return requests.post(url, data=payload).content


class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        # time = strftime("%d/%m/%Y, %H:%M:%S")
        # return "<b>{datetime}</b>\n{message}".format(datetime=time, message=record.msg)
        return "{message}".format(message=record.msg)


def send_message(message, token, chat_id, level=logging.INFO, logger_name='logger'):
    if not (token and chat_id):
        return
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    handler = RequestsHandler(token=token, chat_id=chat_id)
    formatter = LogstashFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(level)
    logger.info(message)
