class MPDState(object):
    def __init__(self, mpd_client):
        self.mpd_client = mpd_client
        self.update()

    def update(self):
        self.song = self.mpd_client.currentsong()
        self.status = self.mpd_client.status()
        self.stats = self.mpd_client.stats()
