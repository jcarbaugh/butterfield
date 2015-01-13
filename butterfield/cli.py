import sys
import json
import asyncio
from . import Bot, ALL


@asyncio.coroutine
def log(bot, message):
    yield from bot.post(
        'C035687FU', # Sunlight's #testing
        "```{}```".format(json.dumps(message, sort_keys=True, indent=2))
    )


def main():
    """
    CLI entrypoint for testing.
    """

    import sys
    bot = Bot(*sys.argv[1:])
    bot.listen(ALL, log)
    bot.start()
