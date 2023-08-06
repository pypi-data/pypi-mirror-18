import mpd

from twmn_mpd.MPDState import MPDState


def msg_queue(providers):
    """
    Returns a generator expression of notifications for twmn to display,
    based on a list of NotificationProvider classes.
    """

    mpd_client = get_mpd_client()

    notifiers = [provider() for provider in providers]

    prev_state = MPDState(mpd_client)
    curr_state = MPDState(mpd_client)

    while True:
        try:
            curr_state.update()
            hasChanged = False
            for notifier in notifiers:
                if notifier.state_changed(prev_state, curr_state):
                    yield notifier.get_notif(curr_state)
                    hasChanged = True
            if hasChanged:
                prev_state.update()
        except (ConnectionError, ConnectionRefusedError):
            mpd_client = get_mpd_client()
        except ConnectionRefusedError:
            mpd_client = get_mpd_client()


def get_mpd_client(ip="127.0.0.1", port=6600):
    mpd_client = mpd.MPDClient()
    mpd_client.connect("127.0.0.1", str(port))
    return mpd_client
