import sys
import asyncio
from . import Bot, ALL


@asyncio.coroutine
def log(bot, message):
    print(bot, message)


def main():
    """
    CLI entrypoint for testing.
    """

    import sys
    bot = Bot(*sys.argv[1:])
    bot.listen(ALL, log)
    bot.start()
