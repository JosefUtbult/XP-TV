import pychromecast
import streamlink
import logging
from time import sleep
import os

CHROMECAST_NAME = "XPel TV"
URL = "https://www.twitch.tv/"
STREAM_NAME = "howisitmanifested"
DEBUG = False

logging.basicConfig(filename=os.path.dirname(__file__) + '/XP_TV.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO if not DEBUG else logging.DEBUG)

def setup():
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[CHROMECAST_NAME])

    cast = None
    try:
        cast = chromecasts[0]
        logging.info("Connected to chromecast")
        cast.wait()
        logging.debug(cast.status)
        return True, cast
    except IndexError:
        logging.error(f"Unable to find {CHROMECAST_NAME}")
        return False, None

def play(cast):
    url = URL + STREAM_NAME
    streamlink_url = None
    try:
        streamlink_url = streamlink.streams(url)['best'].url
        logging.info(f"Got stream from URL {url}")
    except KeyError:
        logging.error(f"Unable to open stream from URL {url}")

    cast.media_controller.play_media(streamlink_url, 'video/mp4')
    cast.media_controller.block_until_active()
    logging.debug(cast.media_controller.status)

def check_active(cast):
    logging.debug(cast.status)
    try:
        return cast.status.is_active_input
    except KeyError:
        return False

if __name__=='__main__':
    while True:
        status, cast = setup()
        if not status:
            pass
        elif not check_active(cast):
            logging.info("Reconnecting")
            play(cast)

        sleep(3600)
