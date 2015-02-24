import asyncio
import re


# utility methods

def is_direct(bot, message):
    return message['channel'].startswith('D')


def is_mention(bot, message):
    return message.get('text', '').startswith('<@{}>'.format(bot.id))


def parse_command(bot, message, command):
    pattern = r"(<@{}>(?::)? )?{}(?: (.*))?".format(bot.id, command)
    match = re.match(pattern, message.get('text', ''))
    if match:
        return match.group(1) or ''
    return None


# handler decorators

def basic(func):
    return asyncio.coroutine(func)


def direct(func):
    @asyncio.coroutine
    def inner(bot, message: "message"):
        if is_direct(bot, message):
            yield from func(bot, message)
    return inner


def mention(func):
    @asyncio.coroutine
    def inner(bot, message: "message"):
        print(is_mention(bot, message))
        if is_mention(bot, message):
            yield from func(bot, message)
    return inner


def at(func):
    @asyncio.coroutine
    def inner(bot, message: "message"):
        if is_direct(bot, message) or is_mention(bot, message):
            yield from func(bot, message)
    return inner


def command(cmd):
    def outer(func):
        @asyncio.coroutine
        def inner(bot, message: "message"):
            if is_direct(bot, message) or is_mention(bot, message):
                arguments = parse_command(bot, message, cmd)
                if arguments is not None:
                    yield from func(bot, message, arguments)
        return inner
    return outer
