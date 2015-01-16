import asyncio
import json
from .. import ALL


@asyncio.coroutine
def log(bot, message: ALL):
    print(message)
    yield from bot.post(
        '#testing',
        "```{}```".format(json.dumps(message, sort_keys=True, indent=2))
    )


@asyncio.coroutine
def emoji(bot, message: "message"):
    if ':shipit:' not in message['text']:
        return

    yield from bot.post(message['channel'], ':shipit:')


@asyncio.coroutine
def big_ben(bot):
    while True:
        yield from bot.post(
            'C035687FU', # Sunlight's #testing
            "DONG",
        )
        yield from asyncio.sleep(5)
