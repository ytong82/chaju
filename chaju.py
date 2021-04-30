import sys
import click
import logging

from danmu import DanMuClient
from utils.Logger import DanmuLogger

APP_DESC = """
          _               _
         | |             (_)
      ___| |__   __ _     _ _   _
     / __| '_ \ / _` |   | | | | |
    | (__| | | | (_| |   | | |_| |
     \___|_| |_|\__,_|   | |\__,_|
                        _/ |
                       |__/

                        ---- A Terminal Tools For Crawling DanMu

    @Author David Tong (ytong82@towing.top)
                                    Last update on 2017-10-23
"""


@click.command()
@click.argument('url', required=True)
@click.option('--log')
def main(url, log):
    dmc = DanMuClient(url)
    if not dmc.isValid():
        print('Url not valid')
    else:
        logger = DanmuLogger(url, log)
        logger.print("Start to crawler %s ..." % url)

    @dmc.danmu
    def danmu_fn(msg):
        message = make_message('[%s] %s' % (msg['NickName'], msg['Content']))
        logger.print(message)

    @dmc.gift
    def gift_fn(msg):
        message = make_message('[%s] sent a gift!' % msg['NickName'])
        logger.print(message)

    @dmc.other
    def other_fn(msg):
        message = make_message('Other message received')
        logger.print(message)

    dmc.start(blockThread=True)


def make_message(msg):
    return msg.encode(sys.stdin.encoding, 'ignore').decode(sys.stdin.encoding)

if __name__ == '__main__':
    print(APP_DESC)
    main()


