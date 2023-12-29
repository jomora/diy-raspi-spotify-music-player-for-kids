from sys import stderr
from time import sleep
import logging
import asyncio
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth

DEVICE_ID = "98bb0735e28656bac098d927d410c3138a4b5bca"
scope = 'user-read-private user-read-email playlist-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
reader = SimpleMFRC522()
# def build_reader_func():
#     reader = SimpleMFRC522()
#     async def f():
#         try:
#             print("Waiting for you to scan an RFID sticker/card")
#             id = reader.read()[0]
#             print("The ID for this card is:",id)
#             return id
#         finally:
#             GPIO.cleanup()
#     return f

def f():
    print("Waiting for you to scan an RFID sticker/card")
    id = reader.read()[0]
    print("The ID for this card is:",id)
    return id

def build_get_id(reader_func, stop_playing_func):
#     def get_id():
#         return reader_func()
    async def get_id():
        # read_task = asyncio.create_task(reader_func())
        read_task = asyncio.get_event_loop().run_in_executor(None,reader_func)
        await read_task
        return read_task.result()
    return get_id
       
def play_song(uri):
    logging.info(f"Playing song {uri}")
    sp.start_playback(DEVICE_ID, uris=[uri])

def play_album(uri):
    logging.info(f"Playing album {uri}")
    sp.start_playback(DEVICE_ID, context_uri=uri)

def stop_playing():
    logging.info("Stop playing")
    sp.pause_playback(DEVICE_ID)

async def init_player(mapping, get_id, play_song, play_album):
    current_id = -1
    while True:
        logging.info("Waiting for id")
        # id_task = asyncio.get_event_loop().run_in_executor(None,get_id)
        id_task = asyncio.create_task(get_id())
        logging.info("id_task: waiting for 1s")
        await asyncio.sleep(1.5)
        logging.info("id_task: waiting completed")
        if not id_task.done():
            logging.info("Calling: stop_playing_func()")
            stop_playing()
            current_id = -1
            logging.info("Set current_id = -1")
        await id_task
        id = id_task.result()

        if current_id == id:
            logging.info(f"Continuing current item {id}",)
            continue

        item = mapping.get(id)

        if item == None:
            logging.info(f"No mapping for {id}")
            continue

        current_id = id
        if item.get("type") == "TRACK":
            play_song(item.get("uri"))
        elif item.get("type") == "ALBUM":
            play_album(item.get("uri"))
        elif item.get("type") == "EXIT":
            logging.info("Stopping player")
            break
        sleep(1)
