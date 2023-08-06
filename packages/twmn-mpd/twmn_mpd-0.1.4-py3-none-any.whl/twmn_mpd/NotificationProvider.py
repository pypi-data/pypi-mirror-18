class NotificationProvider(object):
    def get_state(self, mpd_client):
        """Return the state that the message queue stores."""
        return

    # @abc.abstractmethod
    # def state_changed(self, old_state, new_state):
    #     """Whether the state has changed in a way that merits showing another
    #     notification."""
    #     return

    def get_notif(self, state):
        """Return the notification text to be shown."""

        return

    def get_song_name(self, state):
        song = state.song

        date = song["date"][:4]
        artist = song["artist"]
        title = song["title"]
        content = artist + " - " + title + " " + "({})".format(date)

        print(content)
        return content
