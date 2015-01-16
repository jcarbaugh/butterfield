import sys
import json
import asyncio

import butterfield
from .utils import load_plugin


def main():
    """
    CLI entrypoint for testing.
    """
    _, config, *args = sys.argv
    with open(config, 'r') as fd:
        bot_config = json.load(fd)

    for config in bot_config:

        params = config.get('params') or {}
        daemons = config.get('daemons')

        bot = butterfield.Bot(config.get("key"), daemons=daemons, **params)
        for plugin in config.get("plugins", []):
            bot.listen(plugin)

    butterfield.start()


if __name__ == '__main__':
    main()
