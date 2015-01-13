# Butterfield

A Slack bot framework using Slack's [Real Time Messaging API](https://api.slack.com/rtm), Python 3 and [asyncio](https://docs.python.org/3/library/asyncio.html).

**Butterfield is unstable and being actively developed. Breaking changes will occur.**

## Echo bot example

This simple bot will listen for *message* events and echo the message to the same channel. 

	import asyncio
	from butterfield import Bot
	
	@asyncio.coroutine
	def echo(bot, msg):
		yield from bot.post(
			msg['channel'],
			msg['text']
		)
	
	b = Bot('slack-bot-key')
	b.listen('message', echo)
	b.start()

## Usage

Bots are created by instantiating an instance with a [Slack bot user](https://api.slack.com/bot-users) key.

	mybot = Bot('this-is-not-a-real-key')
	
Message handlers are asyncio [coroutines](https://docs.python.org/3/library/asyncio-task.html#coroutine). When executed, they receive the bot instance that invoked the handler and a copy of the event message from Slack.

	@asyncio.coroutine
	def console_printer(bot, message):
		if 'text' in message:
			print(message['text'])

Handlers are registered with the bot using the *listen* method. The first argument is the event type for which the handler will be called. The full list of event types can be found in the [RTM API docs](https://api.slack.com/rtm). The handler can be called for all events by using `"*"` or `butterfield.ALL`. Multiple events can be specified by using a comma seperated string of types: `"channel_joined,channel_left"`.

	mybot.listen('message', console_printer)

The handler parameter can be either a direct reference to the coroutine or the module path as a string.

Now just start the bot and it'll run... FOREVER.

	mybot.start()

## TODO

* Add HTTP API so messages can be pushed through Butterfield to Slack.
* Listen for meta events and modify local Slack environment appropriately (list of channels, users, etc.).