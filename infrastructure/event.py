from typing import Callable, List


class Event:
    def __init__(self):
        self.handlers: List[Callable] = []

    def add_handler(self, handler: Callable):
        self.handlers.append(handler)

    def remove_handler(self, handler: Callable):
        if handler in self.handlers:
            self.handlers.remove(handler)

    def remove_all_handlers(self):
        self.handlers = []

    def invoke(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)
