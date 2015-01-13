import asyncio


@asyncio.coroutine
def joined_channel(bot, message):
    channel = message['channel']
    bot.channels[channel['id']] = channel
