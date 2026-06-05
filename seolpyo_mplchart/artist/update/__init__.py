from .collection import CollectionMixin
from .text import TextMixin


class UpdateMixin(CollectionMixin, TextMixin):
    def set_artist(self):
        self.set_collection()
        self.set_text()

        return

