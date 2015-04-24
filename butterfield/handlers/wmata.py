from aiowmata.rail import get_predictions
# pip install -e git://github.com/paultag/aiowmata#egg=aiowmata

import asyncio
import json
import re
from butterfield import handlers


@handlers.basic
def wmata(bot, message):
    text = message['text']
    channel = message['channel']

    for station in re.findall("wmata (?P<line>\w*)", text):
        data = yield from get_predictions(station)
        yield from bot.post(
            channel,
            "```{}```".format(json.dumps(data, sort_keys=True, indent=2)))
