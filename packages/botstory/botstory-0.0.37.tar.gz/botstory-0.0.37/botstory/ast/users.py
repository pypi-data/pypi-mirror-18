import logging
from .. import di
from ..integrations.mocktracker import tracker as tracker_module

logger = logging.getLogger(__name__)
_tracker = None


@di.inject()
def add_tracker(tracker):
    logger.debug('add_tracker')
    logger.debug(tracker)
    global _tracker
    _tracker = tracker


def on_new_user_comes(user):
    """
    each interface that create new user should call this method.
    as well if someone need to catch new user it is good place
    to do it

    :param user:
    :return:
    """
    _tracker.new_user(user)


def clear():
    global _tracker
    _tracker = tracker_module.MockTracker()


clear()
