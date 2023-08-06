# -*- coding: utf-8 -*-
"""
Wrapper around the HipChat v2 API for sending user / room notifications.

This module contains a couple of generic functions for sending messages
to rooms and users within HipChat.

    >>> hipchat.notify_room('Customer Service', 'This is a message')
    >>> hipchat.notify_user('hugo', 'Hello, Hugo')

It includes some colour-specific helpers for room notifications:

    >>> hipchat.green('Customer service', 'This is a green message')

Requires HIPCHAT_API_TOKEN to be set.

"""
import logging
import os
import random
import requests

API_V2_ROOT = 'https://api.hipchat.com/v2/'
SEND_USER_MESSAGE_URL = lambda user: "{}user/{}/notification".format(API_V2_ROOT, user)
SEND_ROOM_MESSAGE_URL = lambda room: "{}room/{}/notification".format(API_V2_ROOT, room)
VALID_COLORS = ('yellow', 'green', 'red', 'purple', 'gray', 'random')
VALID_FORMATS = ('text', 'html')
# see https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-response-codes
BAD_RESPONSE_CODES = (400, 401, 403, 404, 405, 429, 500, 503)

logger = logging.getLogger('hipchat')


class HipChatError(Exception):

    """Custom error raised when communicating with HipChat API."""

    def __init__(self, response):
        assert response.status_code in BAD_RESPONSE_CODES, (
            u"Invalid HipChatError response.status_code:{}".format(response)
        )
        assert 'error' in response.json(), (
            u"Invalid HipChatError response.json(): {}".format(response)
        )
        self.status_code = response.status_code
        # NB this is brittle and depends on the API error response existing
        # in the correct format. This is by design - if the response format
        # changes we need to know.
        super(HipChatError, self).__init__(response.json()['error']['message'])


def _token():
    """
    Get a valid 'personal' auth token.

    The HipChat API is rate limited, and the advice from the support team
    is that we either build a proper HipChat Connect app (which will take
    time, although may the way ahead), OR we use a set of tokens, each of
    which is a valid user token. To this end, the TOKENS var read in from
    the environ _could_ be a list of comma-separated tokens. This function
    will pick on at random from the list.

    """
    try:
        token = os.getenv('HIPCHAT_API_TOKEN')
        return random.choice(token.split(',')).strip()
    except AttributeError:
        return None


def _headers(auth_token):
    """
    Return authentication headers for API requests.

    Args:
        auth_token: string, a valid v2 API token.

    Returns a dict that can be passed into requests.post as the
    'headers' dict.

    """
    return {
        'Authorization': 'Bearer {}'.format(auth_token),
        'Host': 'api.hipchat.com',
        'Content-Type': 'application/json'
    }


def _api(
    url,
    message,
    color='yellow',
    label=None,
    notify=False,
    message_format='html'
):
    """
    Send message to user or room via API.

    Args:
        url: API endpoint
        message: string, The message body, 1-10000 chars.

    Kwargs:
        color: string, the colour of the message background (must be one of
            the VALID_COLORS).
        label: string, "A label to be shown in addition to the sender's name"
        notify: bool, if True then notifies the recipient according to their
            app notification settings.
        message_format: text or html (defaults to html); html allows some
            rich formatting, text allows '@' notifications, /code and
            /quote format options.

    Returns HTTP Response object if successful, else raises HipChatError.

    """
    # asserts - message, colour and format are acceptable
    assert message is not None, u"Missing message param"
    assert len(message) >= 1, u"Message too short, must be 1-10,000 chars."
    assert color in VALID_COLORS, u"Invalid color value: %s" % color
    assert message_format in VALID_FORMATS, u"Invalid format: %s" % message_format

    message = message[:10000]
    label = label[:64] if label else None
    token = _token()
    if token is None:
        logger.debug("HipChat is disabled, logging message: %s", message)
        return
    headers = _headers(auth_token=token)
    data = {
        'message': message,
        'color': color,
        'notify': notify,
        'message_format': message_format
    }
    if label is not None:
        data['from'] = label

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp
    except requests.HTTPError as ex:
        print ex
        raise HipChatError(ex.response)


# see https://www.hipchat.com/docs/apiv2/method/send_room_notification
def notify_room(
    room,
    message,
    color='yellow',
    label=None,
    notify=False,
    message_format='html'
):
    """
    Send a room notification via 'Send room notification' API.

    Args:
        room: the id or name of the destination
        message: the message to send

    Kwargs:
        color: string, the colour of the message background (must be one of
            the VALID_COLORS).
        label: string, "A label to be shown in addition to the sender's name"
        notify: bool, if True then notifies the recipient according to their
            app notification settings.
        message_format: text or html (defaults to html); html allows some
            rich formatting, text allows '@' notifications, /code and
            /quote format options.

    Returns HTTP Response object if successful, else raises HipChatError.

    """
    assert room is not None, "HipChat room_id_or_name is missing."
    return _api(
        SEND_ROOM_MESSAGE_URL(room),
        message,
        color=color,
        label=label,
        notify=notify,
        message_format=message_format
    )


# see https://www.hipchat.com/docs/apiv2/method/private_message_user
def notify_user(
    user,
    message,
    notify=False,
    message_format='html'
):
    """
    Send a user notification via 'Send private message' API.

    Args:
        user: the id or email of the recipient
        message: the message to send

    Kwargs:
        notify: bool, if True then notifies the recipient according to their
            app notification settings.
        message_format: text or html (defaults to html); html allows some
            rich formatting, text allows '@' notifications, /code and
            /quote format options.

    Returns HTTP Response object if successful, else raises HipChatError.

    """
    assert user is not None, "HipChat user is missing."
    return _api(
        SEND_USER_MESSAGE_URL(user),
        message,
        notify=notify,
        message_format=message_format
    )


# ================================
# Colour specific helper functions - NB these can only be sent to rooms.
# ================================

def yellow(room, message, **kwargs):
    """Send a yellow message to a room."""
    kwargs['color'] = 'yellow'
    return notify_room(room, message, **kwargs)


def gray(room, message, **kwargs):
    """Send a gray message to a room."""
    kwargs['color'] = 'gray'
    return notify_room(room, message, **kwargs)


# Aliased for UK spelling.
grey = gray


def green(room, message, **kwargs):
    """Send a green message to a room."""
    kwargs['color'] = 'green'
    return notify_room(room, message, **kwargs)


def purple(room, message, **kwargs):
    """Send a purple message to a room."""
    kwargs['color'] = 'purple'
    return notify_room(room, message, **kwargs)


def red(room, message, **kwargs):
    """Send a red message to a room."""
    kwargs['color'] = 'red'
    return notify_room(room, message, **kwargs)
