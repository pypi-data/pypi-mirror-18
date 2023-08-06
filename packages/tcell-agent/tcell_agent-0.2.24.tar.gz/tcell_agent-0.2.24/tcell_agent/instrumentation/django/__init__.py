# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals
from __future__ import print_function

import os
import uuid

import tcell_agent

from tcell_agent.agent import TCellAgent, PolicyTypes
from tcell_agent.sensor_events import HttpTxSensorEvent, FingerprintSensorEvent, LoginSuccessfulSensorEvent, LoginFailureSensorEvent
from tcell_agent.sensor_events import RedirectSensorEvent
from tcell_agent.sensor_events import ServerAgentDetailsEvent
from .settings import send_django_setting_events

from tcell_agent.sanitize import SanitizeUtils

from future.backports.urllib.parse import urlsplit
from future.backports.urllib.parse import urlunsplit
from future.backports.urllib.parse import parse_qs
_started = False
_route_table_sent = False

from .routes import make_route_table

from tcell_agent.instrumentation.django.middleware.globalrequestmiddleware import GlobalRequestMiddleware
from tcell_agent.instrumentation.django.middleware import globalrequestmiddleware
from tcell_agent.instrumentation.django.middleware.csrf_exception_middleware import instrument_csrf_view_middleware
from tcell_agent.instrumentation.django.database_error_wrapper import instrument_database_error_wrapper

import logging
import tcell_agent.tcell_logger
from tcell_agent.instrumentation.django.utils import django15or16

LOGGER = logging.getLogger('tcell_agent').getChild(__name__)

try:
    if django15or16:
        dlp_success = False
    else:
        from tcell_agent.instrumentation.django.dlp import dlp_instrumentation
        dlp_success = True
except Exception as e:
    LOGGER.error("Problem importing DLP: {e}".format(e=e))
    LOGGER.debug(e, exc_info=True)
    dlp_success = False



def _instrument():
    from django.core.handlers.base import BaseHandler
    old_load_middleware = BaseHandler.load_middleware
    def load_middleware(*args, **kwargs):
        LOGGER.info("Adding middleware")
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.body_filter_middleware.BodyFilterMiddleware')
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.afterauthmiddleware.AfterAuthMiddleware')
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.tcelllastmiddleware.TCellLastMiddleware')
        _insertMiddleware(
          'tcell_agent.instrumentation.django.middleware.tcell_data_exposure_middleware.TCellDataExposureMiddleware',
          atIdx=0)
        _insertMiddleware(
          'tcell_agent.instrumentation.django.middleware.globalrequestmiddleware.GlobalRequestMiddleware',
          atIdx=0)
        _insertMiddleware(
             'tcell_agent.instrumentation.django.middleware.timermiddleware.TimerMiddleware')

        if dlp_success == True:
            dlp_instrumentation()

        if _is_csrf_middleware_enabled():
            instrument_csrf_view_middleware()

        instrument_database_error_wrapper()

        import tcell_agent.instrumentation.django.contrib_auth
        return old_load_middleware(*args, **kwargs)
    BaseHandler.load_middleware =  load_middleware

def _insertMiddleware(middlewareClassString, after=None, before=None, atIdx=None):
    from django.conf import settings
    middleware_list = list(settings.MIDDLEWARE_CLASSES)
    if after:
        idx = middleware_list.index(after)+1 if after in middleware_list else len(middleware_list)
    elif before:
        idx = middleware_list.index(before) if before in middleware_list else 0
    elif atIdx is not None:
        idx = atIdx
    else:
        idx = len(middleware_list)
    middleware_list.insert(idx, middlewareClassString)
    settings.MIDDLEWARE_CLASSES = tuple(middleware_list)

def _is_csrf_middleware_enabled():
    from django.conf import settings
    return "django.middleware.csrf.CsrfViewMiddleware" in list(settings.MIDDLEWARE_CLASSES)

try:
    import django
    if TCellAgent.get_agent():
        _instrument()

except Exception as e:
    LOGGER.error("Could not instrument django: {e}".format(e=e))
    LOGGER.debug(e, exc_info=True)
