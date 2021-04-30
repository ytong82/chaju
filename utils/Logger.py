import os
import time
import re
import logging


class DanmuLogger:
    __logger = None
    def __init__(self, url, log):
        # init logger setting
        file_name = DanmuLogger.__get_file_name(url, log)
        format_string = DanmuLogger.__get_format_string()
        log_level = logging.DEBUG

        logger = logging.getLogger('chaju')
        logger.setLevel(log_level)
        formatter = logging.Formatter(format_string)

        # setup file handler
        file_handler = logging.FileHandler(file_name, mode='w', encoding='UTF-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # return
        self.__logger = logger

    @staticmethod
    def __get_file_name(url, path):
        # init log file log
        if path is None:
            path = "logs/"
        room_id = ""
        for website, brand in {
            'panda.tv': 'panda',
            'douyu.com': 'douyu',
            'bilibili.com': 'bilibili'}.items():
            matched_url = re.match(r'^https?://.*?%s/.*?(\w+)$' % website, url)
            if matched_url:
                room_id = matched_url.group(1)
                break

        if not os.path.exists(path):
            os.makedirs(path)

        # create log file
        file_name = path + brand + '.' + room_id + '.log.' + str(time.time())
        return file_name

    @staticmethod
    def __get_format_string():
        format_string = "%(asctime)s %(message)s"
        return format_string

    def print(self, line):
        self.__logger.info(line)
