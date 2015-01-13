import itertools
import os
import json
import asyncio
import websockets
import importlib
from collections import defaultdict
from slacker import Slacker

__all__ = ['Bot', 'EVENTS', 'ALL']


ALL = '*'

EVENTS = ('hello', 'message', 'channel_marked', 'channel_created',
          'channel_joined', 'channel_left', 'channel_deleted', 'channel_rename',
          'channel_archive', 'channel_unarchive', 'channel_history_change',
          'im_created', 'im_open', 'im_close', 'im_marked', 'im_history_changed',
          'group_joined', 'group_left', 'group_open', 'group_close', 'group_archive',
          'group_unarchive', 'group_rename', 'group_marked', 'group_history_changed',
          'file_created', 'file_shared', 'file_unshared', 'file_public', 'file_private',
          'file_change', 'file_deleted', 'file_comment_added', 'file_comment_edited',
          'file_comment_deleted', 'presence_change', 'manual_presence_change',
          'pref_chage', 'user_change', 'team_join', 'star_added', 'star_removed',
          'emoji_changed', 'commands_changed', 'team_pref_change', 'team_rename',
          'team_domain_change', 'email_domain_changed', 'bot_added',
          'bot_changed', 'accounts_changed')


class Bot(object):

    def __init__(self, token):
        self.slack = Slacker(token)
        self.handlers = defaultdict(list)
        self.environment = None

    def start(self):
        self._message_id = 0
        resp = self.slack.rtm.start()
        self.id = resp.body['self']['id']
        self.name = resp.body['self']['name']
        self.environment = {
            'team': resp.body['team'],
            'users': {u['id']: u for u in resp.body['users']},
            'channels': {c['id']: c for c in resp.body['channels']},
            'groups': {g['id']: g for g in resp.body['groups']},
            'ims': {i['id']: i for i in resp.body['ims']},
            'bots': resp.body['bots'],
        }

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ws_handler(resp.body['url'], self))
        loop.close()

    @asyncio.coroutine
    def ws_handler(self, url, handler):
        self.ws = yield from websockets.connect(url)
        while True:
            content = yield from self.ws.recv()

            if content is None:
                break

            message = json.loads(content)

            if 'ok' in message:
                continue

            message_type = message['type']
            type_handlers = self.handlers[message_type]

            for handler in itertools.chain(self.handlers[ALL], type_handlers):
                asyncio.async(handler(self, message))

    def listen(self, events, coro):
        if isinstance(events, str):
            events = events.split(',')

        if isinstance(coro, str):
            # Preform an import by name
            module, coroutine = coro.rsplit(".", 1)
            module = importlib.import_module(module)
            coro = getattr(module, coroutine)

        for event in events:
            if event not in EVENTS and event != ALL:
                raise ValueError('`{}` is not a valid event type'.format(event))
            self.handlers[event].append(coro)

    @asyncio.coroutine
    def post(self, channel, text):
        self._message_id += 1
        data = {'id': self._message_id,
                'type': 'message',
                'channel': channel,
                'text': text}
        content = json.dumps(data)
        yield from self.ws.send(content)

    @asyncio.coroutine
    def ping(self):
        self._message_id += 1
        data = {'id': self._message_id,
                'type': 'ping'}
        content = json.dumps(data)
        yield from self.ws.send(content)
