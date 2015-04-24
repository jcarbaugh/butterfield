import importlib
import re


def load_plugin(name):
    module, coroutine = name.rsplit(".", 1)
    module = importlib.import_module(module)
    coro = getattr(module, coroutine)
    return coro


def at_bot(func):
    def inner(bot, message: "message"):
        match = re.match(r"<@{}>(?::)? (.*)".format(bot.id),
                         message.get('text'))
        if match:
            message['text'] = match.group(1)
            yield from func(bot, message)
    return inner
