"""
requests_tracker.signals
========================
"""
from django.dispatch import Signal

pre_send = Signal(providing_args=["uid", "prep", "api_uid"])
response = Signal(providing_args=["uid", "resp", "duration"])
request_failed = Signal(providing_args=["uid", "exception", "duration"])
