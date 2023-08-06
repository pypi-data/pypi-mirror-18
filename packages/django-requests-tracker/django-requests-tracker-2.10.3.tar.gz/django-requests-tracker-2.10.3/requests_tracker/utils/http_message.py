"""
requests_tracker.utils.http_message
===================================
"""
from urlparse import urlsplit
from django.template import Context
from django.template.loader import get_template


def render_request_message(prepared_request):
    tmpl = get_template('requests_tracker/request.tmpl')
    context = Context({
        'prep': prepared_request,
        'host': urlsplit(prepared_request.url).netloc,
    })
    return tmpl.render(context)


def render_response_message(response):
    tmpl = get_template('requests_tracker/response.tmpl')
    context = Context({'response': response})
    return tmpl.render(context)
