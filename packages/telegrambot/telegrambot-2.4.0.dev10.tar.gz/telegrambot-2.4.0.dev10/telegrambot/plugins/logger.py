""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import logging
import hashlib

from telegrambot.plugins.base import BasePlugin


class Logger(BasePlugin):
    def __init__(self, *args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)
        self.loggers = {}

    def handle_msg(self, msg):
        if msg.text is None:
            self.logger.debug('handle_update(%s)', payload)
        chat_id = hashlib.md5(str(msg.chat.id)).hexdigest()
        if chat_id not in self.loggers:
            logger = logging.getLogger('telegrambot.chats.{}'.format(chat_id))
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter('[LOG:%(levelname)s] %(message)s'))
            logger.addHandler(handler)
            self.loggers[chat_id] = logger
        log_message = "{timestamp}\t({subject})\t<{user}> {msg_text}".format(**{
            'timestamp': msg.date.strftime("%Y-%m-%d-%H-%M-%S"),
            'subject': msg.chat.title,
            'user': msg.froom.username or '{} {}'.format(msg.froom.first_name, msg.froom.last_name).strip().replace(' ', '_'),
            'msg_text': msg.text
        })
        self.loggers[chat_id].info(log_message)

    def handle_update(self, payload):
        self.logger.debug('handle_update(%s)', payload)
