from matplotlib.collections import LineCollection

from ....style import Style


class CrossLineMixin:
    STYLE: Style

    collection_crossline_price: LineCollection
    collection_crossline_volume: LineCollection
    collection_slider_top_vline: LineCollection
    collection_slider_bottom_vline: LineCollection

    def get_collection_crossline_kwargs(self):
        kwargs = self.STYLE.ARTIST.CROSSLINE.__dict__
        kwargs['segments'] = []
        kwargs['animated'] = True

        return kwargs

    def set_collection_crossline(self):
        kwargs = self.get_collection_crossline_kwargs()

        self.collection_crossline_price.set(**kwargs)
        self.collection_crossline_volume.set(**kwargs)

        self.collection_slider_top_vline.set(**kwargs)
        self.collection_slider_bottom_vline.set(**kwargs)

        return

