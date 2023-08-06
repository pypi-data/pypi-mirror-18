from twmn_mpd.NotificationProvider import NotificationProvider


class NowPlayingNotifier(NotificationProvider):
    def state_changed(self, old_state, new_state):
        return old_state.song != new_state.song

    def get_notif(self, mpd_state):
        header = "now playing"
        content = self.get_song_name(mpd_state)

        _title = "<title>" + header + "</title>"
        _content = "<content>" + content + "</content>"

        msg = "<root>" + _title + _content + "</root>"

        return msg
