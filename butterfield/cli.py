import sys
from . import Bot


def main():
    """
    CLI entrypoint for testing.
    """

    import sys
    bot = Bot(*sys.argv[1:])
    bot.start()
