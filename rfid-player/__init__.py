import asyncio
import logging
import player 
import RPi.GPIO as GPIO
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)

async def main():
    logging.info("Configuring the player")
    mapping = {
        # Card 1
        488197591059: {
            # Rock christmas
            "uri": "spotify:album:5stoW92sMwLYf0WxOgEa16",
            "type": "ALBUM"
            },
        # Card 2
        496679473376: {
            # Paw Patrol 99: Die Suche nach der Krone
            "uri": "spotify:album:31FKZ6SFUc9lFmK7DuDKqR",
            "type": "ALBUM"
            },

        # Transponder 3
        384275650724: {
            # Peter und der Wolf
            "uri": "spotify:album:76vW9dCZzixuVIwW1NZtom",
            "type": "ALBUM"
            },
        # Transponder 4
        452375222408: {
            # Leo Lausemaus 14
            # 1. Lilis Geburtstag
            # 2. Leos neues Boot
            # 3. Auf Safari
            # 4. Und das Kostümfest
            "uri": "spotify:album:6Yjp76n80lWc1krTbq7Z7m",
            "type": "ALBUM"
            }
    }
    # reader_func = player.build_reader_func()
    get_id = player.build_get_id(
            # reader_func=reader_func,
            reader_func=player.f,
            stop_playing_func=player.stop_playing)
    await player.init_player(
            mapping=mapping,
            get_id=get_id,
            play_song=player.play_song,
            play_album=player.play_album)

    GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

