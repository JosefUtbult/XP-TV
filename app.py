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
    while True:
        logging.info(f"Trying to connect to {CHROMECAST_NAME}")
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[CHROMECAST_NAME])

        try:
            cast = chromecasts[0]
            logging.info(f"Connected to {CHROMECAST_NAME}")
            cast.wait()
            logging.debug(cast.status)
            return cast
        except IndexError:
            logging.error(f"Unable to find {CHROMECAST_NAME}")

        sleep(5)


def play(cast):
    url = URL + STREAM_NAME
    streamlink_url = None
    while True:
        logging.info(f"Connecting to {url}")
        try:
            streamlink_url = streamlink.streams(url)['best'].url
            logging.info(f"Got stream from URL {url}")
            cast.media_controller.play_media(streamlink_url, 'video/mp4')
            cast.media_controller.block_until_active()
            logging.debug(cast.media_controller.status)

            return
        except KeyError:
            logging.error(f"Unable to open stream from URL {url}")
        except OSError:
            logging.error(f"Network is unreachable")


def check_active(cast):
    logging.debug(cast.status)
    try:
        return cast.status.is_active_input
    except KeyError:
        return False


if __name__=='__main__':
    cast = setup()

    while True:
        if not check_active(cast):
            logging.info("Reconnecting")
            play(cast)

        sleep(3600)
