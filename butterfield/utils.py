import importlib


def load_plugin(name):
    module, coroutine = name.rsplit(".", 1)
    module = importlib.import_module(module)
    coro = getattr(module, coroutine)
    return coro
