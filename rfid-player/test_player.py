# pytest  --log-cli-level info --log-format="%(asctime)s %(levelname)s %(message)s" --log-date-format="%Y-%m-%d %H:%M:%S" .

import signal
import asyncio
import pytest
import player
from sys import stderr
from time import sleep
import logging
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)

def test_play():
    mapping = {
        30: {
            "uri": "spotify:album:31FKZ6SFUc9lFmK7DuDKqR",
            "type": "ALBUM"
        },
        31: {
            "uri": "spotify:track:03aXtrt0TBNYqz5xe8qunM",
            "type": "TRACK"
        }
    }

    cards = [
            {"id": 30,"sleep": 0.5},
            {"id": 30, "sleep": 0.5},
            {"id": 3821, "sleep": 2},
            {"id": 1111, "sleep": 2},
            {"id": 2, "sleep": 2}
           ]
    async def rfid_chip():
        card = cards.pop(0) 
        logging.info(f"rfid_chip: blocking for {card['sleep']}s")
        await asyncio.sleep(card["sleep"])
        return card["id"] 

    async def signal_input():
        result = -1 
        result = signal.sigwait({
            signal.SIGUSR1,
            signal.SIGUSR2,
            signal.SIGINT
        })
        logging.info(f"SIGNAL {result} (type {type(result)})")
        return result 


    async def get_id():
        read_task = asyncio.create_task(rfid_chip())
        logging.info("get_id: waiting for 1s")
        await asyncio.sleep(1)
        if not read_task.done():
            stop_playing()
        await read_task
        return read_task.result()
       
    def play_song(uri):
        logging.info(f"Playing song {uri}")

    def play_album(uri):
        logging.info(f"Playing album {uri}")

    def stop_playing():
        logging.info("Stop playing")

    player.init_player(mapping, get_id, play_song, play_album)
