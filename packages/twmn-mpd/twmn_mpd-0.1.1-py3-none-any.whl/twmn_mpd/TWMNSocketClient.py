import socket
from contextlib import closing

import twmn_mpd.MsgQueue as MsgQueue
from twmn_mpd.providers.NowPlayingNotifier import NowPlayingNotifier
from twmn_mpd.providers.PlayStateNotifier import PlayStateNotifier


def create_notifs(sock, notifiers):
    """
    Creates a notification for each message in the queue,
    based on a list of notifiers, by writing to the socket
    provided.
    """

    for msg in MsgQueue.msg_queue(notifiers):
        sock.send(msg.encode())


def start_notifs(ip="127.0.0.1",
                 port=9797,
                 notifiers=[PlayStateNotifier, NowPlayingNotifier]):
    """
    The main entrypoint to twmn_mpd.
    """

    with closing(socket.socket(socket.AF_INET,
                               socket.SOCK_DGRAM)) as twmn_sock:
        twmn_sock.connect((ip, port))
        create_notifs(twmn_sock, notifiers)
