import sys
import json
import asyncio
from . import Bot, ALL
from .utils import load_plugin


def main():
    """
    CLI entrypoint for testing.
    """
    _, config, *args = sys.argv
    with open(config, 'r') as fd:
        config = json.load(fd)

    bot = Bot(*args)
    for plugin in config.get("plugins", []):
        bot.listen(plugin)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(*[
            bot.start()
        ] + [
            load_plugin(x)(bot) for x in config.get("daemons", [])
        ])
    )
    loop.close()
