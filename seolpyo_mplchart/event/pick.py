from matplotlib.backend_bases import PickEvent


class PickMixin:
    acting_pick = False

    def on_pick(self, e: PickEvent):
        artist = e.artist

        pick_action = getattr(artist, 'pick_action', None)
        if pick_action:
            pick_action(e)

        return

    def _on_pick(self, e: PickEvent):
        if not self.acting_pick:
            self.acting_pick = True
            self.on_pick(e)
            self.acting_pick = False
        return

