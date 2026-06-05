from matplotlib.collections import LineCollection

from ....style import Style


class BoxMixin:
    STYLE: Style

    collection_box_price: LineCollection
    collection_box_volume: LineCollection

    def get_collection_box_kwargs(self):
        kwargs = self.STYLE.ARTIST.BOX.__dict__
        kwargs['segments'] = []
        kwargs['animated'] = True

        return kwargs

    def set_collection_box_price(self):
        kwargs = self.get_collection_box_kwargs()

        self.collection_box_price.set(**kwargs)
        return

    def set_collection_box_volume(self):
        kwargs = self.get_collection_box_kwargs()

        self.collection_box_volume.set(**kwargs)
        return

    def set_collection_box(self):
        self.set_collection_box_price()
        self.set_collection_box_volume()

        return

