from sys import stderr
from time import sleep
import logging
import asyncio


def init_player(mapping, get_id, play_song, play_album):
    current_id = -1
    while True:
        logging.info("Waiting for id")
        id = asyncio.run(get_id())

        if id == 2:
            logging.info("Stopping player")
            break

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
        sleep(1)
