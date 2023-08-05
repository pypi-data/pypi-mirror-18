# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Aggregate authentication tentatives
"""
import logging
import json

from .matcher_callback import MatcherRule
from ..runtime_infos import runtime

LOGGER = logging.getLogger(__name__)


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        """ Return the repr of unkown objects
        """
        return repr(obj)


class AuthMetricsCB(MatcherRule):

    def post(self, original, result, *args, **kwargs):
        # Django authentication model return either an User or None
        if result is None:
            auth_status = 'login-fail'
        else:
            auth_status = 'login-success'

        keys = []

        # Search for credentials identifier that match the whitelist
        for identifier in kwargs.keys():
            if self.match(identifier):
                keys.append([identifier.lower(), kwargs[identifier]])

        if not keys:
            # If we couldn't identify an user, don't record a metric
            return

        request = runtime.get_current_request()
        key = {'keys': keys, 'ip': request.client_ip}

        observation_key = json.dumps(key, separators=(',', ':'), sort_keys=True, cls=CustomEncoder)
        self.record_observation(auth_status, observation_key, 1)
