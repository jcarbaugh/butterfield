import sys
import json
import asyncio
from . import Bot, ALL


def main():
    """
    CLI entrypoint for testing.
    """
    config = sys.argv[1]
    with open(config, 'r') as fd:
        plugins = json.load(fd)

    bot = Bot(*sys.argv[2:])

    for plugin in plugins:
        print(plugin)
        bot.listen(*plugin)

    bot.start()
