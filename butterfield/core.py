import asyncio
import hashlib
import importlib
import itertools
import json
import os
from collections import defaultdict

import websockets
from slacker import Slacker
from .handlers import environment
from .utils import load_plugin

__all__ = ['Bot', 'Runner', 'EVENTS', 'ALL', 'run']


ALL = '*'

EVENTS = (
    'accounts_changed', 'bot_added', 'bot_changed', 'channel_archive',
    'channel_created', 'channel_deleted', 'channel_history_changed',
    'channel_joined', 'channel_left', 'channel_marked',
    'channel_rename', 'channel_unarchive', 'commands_changed',
    'email_domain_changed', 'emoji_changed', 'file_change',
    'file_comment_added', 'file_comment_deleted', 'file_comment_edited',
    'file_created', 'file_deleted', 'file_private', 'file_public',
    'file_shared', 'file_unshared', 'group_archive', 'group_close',
    'group_history_changed', 'group_joined', 'group_left',
    'group_marked', 'group_open', 'group_rename', 'group_unarchive',
    'hello', 'im_close', 'im_created', 'im_history_changed',
    'im_marked', 'im_open', 'manual_presence_change', 'message',
    'pin_added', 'pin_removed', 'pref_change', 'presence_change',
    'star_added', 'star_removed', 'team_domain_change', 'team_join',
    'team_migration_started', 'team_plan_change', 'team_pref_change',
    'team_rename', 'user_change', 'user_typing')


@asyncio.coroutine
def environment_handler(bot, message: ALL):
    func = getattr(environment, message['type'], None)
    if func:
        yield from func(bot, message)


class Runner(object):

    def __init__(self, *bots):
        self.registry = {}
        for bot in bots:
            self.add_bot(bot)

    def add_bot(self, bot):
        if bot.uuid in self.registry:
            raise ValueError(
                "Bot {} has already been registered".format(bot.uuid))
        self.registry[bot.uuid] = bot

    def gather(self):

        coros = []

        for bot in self.registry.values():
            coros.append(bot())
            coros.extend(load_plugin(x)(bot) for x in bot.daemons)

        return asyncio.gather(*coros)


class Bot(object):

    def __init__(self, token, daemons=None, **kwargs):

        self.slack = Slacker(token)
        self.uuid = hashlib.sha1(token.encode("utf-8")).hexdigest()

        self.handlers = defaultdict(list)
        self.daemons = daemons or []
        self.environment = None
        self.params = kwargs

    def __call__(self):

        self.running = False
        self._message_id = 0

        resp = self.slack.rtm.start()

        self.environment = {
            'self': resp.body['self'],
            'team': resp.body['team'],
            'users': {u['id']: u for u in resp.body['users']},
            'channels': {c['id']: c for c in resp.body['channels']},
            'groups': {g['id']: g for g in resp.body['groups']},
            'ims': {i['id']: i for i in resp.body['ims']},
            'bots': resp.body['bots'],
        }

        return self.ws_handler(resp.body['url'], self)

    def __repr__(self):
        return "<butterfield.Bot uuid:{}>".format(self.uuid)

    @property
    def id(self):
        if self.environment:
            return self.environment['self']['id']

    @property
    def name(self):
        if self.environment:
            return self.environment['self']['name']

    @asyncio.coroutine
    def ws_handler(self, url, handler):

        self.ws = yield from websockets.connect(url)
        self.running = True

        while True:
            content = yield from self.ws.recv()

            if content is None:
                break

            message = json.loads(content)

            if 'ok' in message:
                continue

            message_type = message['type']
            type_handlers = self.handlers[message_type]

            yield from environment_handler(self, message)

            for handler in itertools.chain(self.handlers[ALL], type_handlers):
                asyncio.async(handler(self, message))

    def listen(self, coro):
        if isinstance(coro, str):
            coro = load_plugin(coro)

        events = coro.__annotations__.get("message")
        if events is None:
            raise ValueError("No Annotation on plugin `%s`" % (
                coro.__code__.co_name
            ))

        if isinstance(events, str):
            events = [events]

        for event in events:
            if event not in EVENTS and event != ALL:
                raise ValueError(
                    '`{}` is not a valid event type'.format(event))
            self.handlers[event].append(coro)

    @asyncio.coroutine
    def post(self, channel_name_or_id, text):
        if self.running is False:
            return

        channel = self.channel(channel_name_or_id)
        if not channel:
            channel = self.im(channel_name_or_id)

        self._message_id += 1
        data = {'id': self._message_id,
                'type': 'message',
                'channel': channel['id'],
                'text': text}
        content = json.dumps(data)
        yield from self.ws.send(content)

    @asyncio.coroutine
    def dm(self, user_name_or_id, text):
        channel = self.im(user_name_or_id)
        yield from self.post(channel['id'], text)

    @asyncio.coroutine
    def ping(self):
        if self.running is False:
            return

        self._message_id += 1
        data = {'id': self._message_id,
                'type': 'ping'}
        content = json.dumps(data)
        yield from self.ws.send(content)

    def channel(self, name_or_id):
        return self._env_item('channels', 'name', name_or_id, prefix='#')

    def group(self, name_or_id):
        return self._env_item('groups', 'name', name_or_id, prefix='#')

    def im(self, name_or_id):
        channel = self._env_item('ims', 'user', name_or_id, prefix='@')
        if not channel:
            user = self.user(name_or_id)
            if user:
                resp = self.slack.im.open(user['id'])
                channel = resp.body['channel']
                self.environment['ims'][channel['id']] = channel
        return channel

    def user(self, name_or_id):
        return self._env_item('users', 'name', name_or_id, prefix='@')

    def _env_item(self, obj, attr, name_or_id, prefix=None):

        if obj not in ['channels', 'users', 'groups', 'ims']:
            raise ValueError('{} is not a valid type'.format(obj))

        if prefix and name_or_id.startswith(prefix):
            name_or_id = name_or_id[1:]

        if name_or_id in self.environment[obj]:
            return self.environment[obj][name_or_id]

        for item in self.environment[obj].values():
            if attr in item and item[attr] == name_or_id:
                return item


def run(*bots):

    runner = Runner(*bots)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.gather())
    loop.close()
