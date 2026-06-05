from .create import CreateMixin
from .update import UpdateMixin


class ArtistMixin(CreateMixin, UpdateMixin):
    def __init__(self):
        super().__init__()

        self.add_artist()

        return

