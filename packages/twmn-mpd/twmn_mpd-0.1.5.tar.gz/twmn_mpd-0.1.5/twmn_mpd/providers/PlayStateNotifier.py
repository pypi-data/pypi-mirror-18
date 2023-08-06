import twmn_mpd.utils as utils
from twmn_mpd.NotificationProvider import NotificationProvider


class PlayStateNotifier(NotificationProvider):
    def state_changed(self, old_state, new_state):
        return old_state.status["state"] != new_state.status["state"]

    def get_notif(self, mpd_state):
        status = mpd_state.status
        header = utils.to_human_state_name(status["state"])
        content = self.get_song_name(mpd_state)

        _title = "<title>" + header + "</title>"
        _content = "<content>" + content + "</content>"

        msg = "<root>" + _title + _content + "</root>"

        return msg
