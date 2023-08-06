"""
requests_tracker.signals.handlers
=================================
"""
import logging
from urlparse import urlsplit, urlunsplit

from requests_tracker import states
from requests_tracker.models import Record
from requests_tracker.utils import http_message
from requests_tracker.filtering import filters

logger = logging.getLogger(__name__)


def pre_send_handler(sender, uid, prep, api_uid, **kwargs):
    """handle `requests_tracker.signals.pre_send` signal"""

    setattr(prep, 'api_uid', api_uid)

    if filters.rt_filter(prep):
        rt_kwargs = {
            'uid': uid,
            'api_uid': api_uid or '',
            'method': prep.method,
            'request_message': http_message.render_request_message(prep),
        }

        _ = urlsplit(prep.url)
        rt_kwargs.update({
            'url': urlunsplit((_.scheme, _.netloc, _.path, '', '')),
        })

        record = Record(**rt_kwargs)
        record.save()

        record.transit(states.IN_PROGRESS)


def response_handler(sender, uid, resp, duration, **kwargs):
    """handle `requests_tracker.signals.response` signal"""

    try:
        record = Record.objects.get(uid=uid)
    except Record.DoesNotExist:
        logger.info("uid does not exist: %r" % uid)
    else:
        rt_kwargs = {
            'status_code': resp.status_code,
            'response_message': http_message.render_response_message(resp),
            'remark': resp.reason,
            'duration': duration,
        }
        record.transit(states.SUCCESS, **rt_kwargs)


def request_failed_handler(sender, uid, exception, duration, **kwargs):
    """handle `requests_tracker.signals.request_failed` signal"""

    try:
        record = Record.objects.get(uid=uid)
    except Record.DoesNotExist:
        logger.info("uid does not exist: %r" % uid)
    else:
        rt_kwargs = {
            'duration': duration,
            'remark': exception.__class__.__name__,
            'response_message': exception.message,
        }
        record.transit(states.FAILURE, **rt_kwargs)

    raise exception
