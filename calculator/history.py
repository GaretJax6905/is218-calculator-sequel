"""History owns a private entry list of (calculation, result) pairs."""


class History:
    def __init__(self):
        self._entries = []

    def add(self, calculation, result):
        self._entries.append((calculation, result))

    def get_history(self):
        return list(self._entries)      # shallow copy

    def clear(self):
        self._entries.clear()