from .collection import CollectionMixin
from .text import TextMixin


class CreateMixin(CollectionMixin, TextMixin):
    def add_artist(self):
        self._add_collection()
        self._add_text()

        return

