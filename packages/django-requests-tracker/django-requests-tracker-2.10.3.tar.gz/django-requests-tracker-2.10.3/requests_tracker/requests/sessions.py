"""
requests_tracker.requests
=========================
"""
from __future__ import absolute_import

from requests.models import Request
from requests.sessions import Session as _Session

from django.utils.timezone import now

from requests_tracker.signals import pre_send, response, request_failed
from requests_tracker.utils.unique import uniqid

__implements__ = ['Session']


class Session(_Session):

    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None,
                api_uid=None):
        """
        patched requests.session.Session
        """
        # Create the Request.
        req = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks
        )
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        # Send the request.
        send_kwargs = {
            'timeout': timeout,
            'allow_redirects': allow_redirects,
        }
        send_kwargs.update(settings)

        # Send pre_send signal
        uid = uniqid()
        pre_send.send(sender=self.request,
                      uid=uid,
                      prep=prep,
                      api_uid=api_uid)

        # Send the request.
        try:
            before_time = now()
            resp = self.send(prep, **send_kwargs)
            duration = now() - before_time
        except Exception, e:
            duration = now() - before_time
            request_failed.send(sender=self.request,
                                uid=uid,
                                exception=e,
                                duration=duration)
        else:
            response.send(sender=self.request,
                          uid=uid,
                          resp=resp,
                          duration=duration)

        return resp
