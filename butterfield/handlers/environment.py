import asyncio


@asyncio.coroutine
def bot_added(bot, message: "bot_added"):
    pass


@asyncio.coroutine
def bot_changed(bot, message: "bot_changed"):
    pass


@asyncio.coroutine
def channel_archive(bot, message: "channel_archive"):
    channel = bot.environment['channels'].get(message['channel'])
    if channel:
        channel['is_archived'] = True


@asyncio.coroutine
def channel_created(bot, message: "channel_created"):
    channel = message['channel']
    bot.environment['channels'][channel['id']] = channel


@asyncio.coroutine
def channel_deleted(bot, message: "channel_deleted"):
    if message['channel'] in bot.environment['channels']:
        del bot.environment['channels'][message['channel']]


@asyncio.coroutine
def channel_history_change(bot, message: "channel_history_change"):
    pass


@asyncio.coroutine
def channel_joined(bot, message: "channel_joined"):
    channel = message['channel']
    bot.environment['channels'][channel['id']] = channel


@asyncio.coroutine
def channel_left(bot, message: "channel_left"):
    if message['channel']['id'] in bot.environment['channels']:
        del bot.environment['channels'][message['channel']['id']]


@asyncio.coroutine
def channel_marked(bot, message: "channel_marked"):
    channel = bot.environment['channels'].get(message['channel'])
    if channel:
        channel['last_read'] = message['ts']


@asyncio.coroutine
def channel_rename(bot, message: "channel_rename"):
    channel = bot.environment['channels'].get(message['channel']['id'])
    if channel:
        channel['name'] = message['channel']['name']
        channel['created'] = message['channel']['created']


@asyncio.coroutine
def channel_unarchive(bot, message: "channel_unarchive"):
    channel = bot.environment['channels'].get(message['channel'])
    if channel:
        channel['is_archived'] = False


@asyncio.coroutine
def email_domain_changed(bot, message: "email_domain_changed"):
    bot.environment['team']['email_domain'] = message['email_domain']


@asyncio.coroutine
def file_change(bot, message: "file_change"):
    pass


@asyncio.coroutine
def file_comment_added(bot, message: "file_comment_added"):
    pass


@asyncio.coroutine
def file_comment_deleted(bot, message: "file_comment_deleted"):
    pass


@asyncio.coroutine
def file_comment_edited(bot, message: "file_comment_edited"):
    pass


@asyncio.coroutine
def file_created(bot, message: "file_created"):
    pass


@asyncio.coroutine
def file_deleted(bot, message: "file_deleted"):
    pass


@asyncio.coroutine
def file_private(bot, message: "file_private"):
    pass


@asyncio.coroutine
def file_public(bot, message: "file_public"):
    pass


@asyncio.coroutine
def file_shared(bot, message: "file_shared"):
    pass


@asyncio.coroutine
def file_unshared(bot, message: "file_unshared"):
    pass


@asyncio.coroutine
def group_archive(bot, message: "group_archive"):
    group = bot.environment['groups'].get(message['channel'])
    if group:
        group['is_archived'] = True


@asyncio.coroutine
def group_close(bot, message: "group_close"):
    if message['channel'] in bot.environment['groups']:
        del bot.environment['groups'][message['channel']]


@asyncio.coroutine
def group_history_changed(bot, message: "group_history_changed"):
    pass


@asyncio.coroutine
def group_joined(bot, message: "group_joined"):
    group = message['channel']
    bot.environment['groups'][group['id']] = group


@asyncio.coroutine
def group_left(bot, message: "group_left"):
    if message['channel']['id'] in bot.environment['groups']:
        del bot.environment['groups'][message['channel']['id']]


@asyncio.coroutine
def group_marked(bot, message: "group_marked"):
    group = bot.environment['group'].get(message['channel'])
    if group:
        group['last_read'] = message['ts']


@asyncio.coroutine
def group_open(bot, message: "group_open"):
    pass


@asyncio.coroutine
def group_rename(bot, message: "group_rename"):
    group = bot.environment['groups'].get(message['channel']['id'])
    if group:
        group['name'] = message['channel']['name']
        group['created'] = message['channel']['created']


@asyncio.coroutine
def group_unarchive(bot, message: "group_unarchive"):
    group = bot.environment['groups'].get(message['channel'])
    if group:
        group['is_archived'] = False


@asyncio.coroutine
def im_close(bot, message: "im_close"):
    if message['channel'] in bot.environment['ims']:
        del bot.environment['ims'][message['channel']]


@asyncio.coroutine
def im_created(bot, message: "im_created"):
    im = message['channel']
    bot.environment['ims'][im['id']] = group


@asyncio.coroutine
def im_history_changed(bot, message: "im_history_changed"):
    pass


@asyncio.coroutine
def im_marked(bot, message: "im_marked"):
    im = bot.environment['ims'].get(message['channel'])
    if im:
        im['last_read'] = message['ts']


@asyncio.coroutine
def im_open(bot, message: "im_open"):
    pass


@asyncio.coroutine
def manual_presence_change(bot, message: "manual_presence_change"):
    bot.environment['self']['manual_presence'] = message['presence']


@asyncio.coroutine
def pref_chage(bot, message: "pref_chage"):
    name = message['name']
    value = message['value']
    bot.environment['self']['prefs'][name] = value


@asyncio.coroutine
def presence_change(bot, message: "presence_change"):
    pass


@asyncio.coroutine
def star_added(bot, message: "star_added"):
    pass


@asyncio.coroutine
def star_removed(bot, message: "star_removed"):
    pass


@asyncio.coroutine
def team_domain_change(bot, message: "team_domain_change"):
    bot.environment['team']['domain'] = message['domain']


@asyncio.coroutine
def team_join(bot, message: "team_join"):
    user = message['user']
    bot.environment['users'][user['id']] = user


@asyncio.coroutine
def team_pref_change(bot, message: "team_pref_change"):
    name = message['name']
    value = message['value']
    bot.environment['team']['prefs'][name] = value


@asyncio.coroutine
def team_rename(bot, message: "team_rename"):
    bot.environment['team']['name'] = message['name']


@asyncio.coroutine
def user_change(bot, message: "user_change"):
    user = message['user']
    bot.environment['users'][user['id']] = user
