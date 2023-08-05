# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Contains all callback classes
"""
import sys
import logging

from ..signature import REQUIRED_KEYS, SIGNATURE_VERSION
from ..rules import RuleCallback
from ..remote_exception import RemoteException

# Import rules callbacks
from .record_request_context import RecordRequestContext
from .record_request_context_django import RecordRequestContextDjango
from .record_request_context_flask import RecordRequestContextFlask
from .regexp_rule import RegexpRule
from .headers_insert import HeadersInsertCB
from .headers_insert_flask import HeadersInsertCBFlask
from .headers_insert_django import HeadersInsertCBDjango
from .user_agent_matches import UserAgentMatchesCB
from .user_agent_matches_framework import UserAgentMatchesCBDjango, UserAgentMatchesCBFramework
from .reflected_xss import ReflectedXSSCB
from .not_found import NotFoundCB
from .not_found_django import NotFoundCBDjango
from .not_found_flask import NotFoundCBFlask
from .count_http_codes import CountHTTPCodesCB
from .count_http_codes_flask import CountHTTPCodesCBFlask
from .count_http_codes_django import CountHTTPCodesCBDjango
from .auth_metrics import AuthMetricsCB
from .crawler_user_agent_matches_metrics import CrawlerUserAgentMatchesMetricsCB

try:
    from .js import JSCB
except ImportError:
    pass


LOGGER = logging.getLogger(__name__)


def cb_from_rule(rule, runner, rule_verifier=None):
    """ Instantiate the right cb class
    """
    # Fixme clean

    if not isinstance(rule, dict):
        LOGGER.debug("Invalid rule type %s", type(rule))
        return

    # Check rule signature
    if rule_verifier is not None:
        rule_verifier.verify_rule(rule, REQUIRED_KEYS, SIGNATURE_VERSION)

    callback_class_name = rule.get('hookpoint', {}).get('callback_class')

    if callback_class_name is None:
        err_msg = "Couldn't find a callback_class_name for rule %s, fallback on js"
        LOGGER.debug(err_msg, rule['name'])
        callback_class_name = "JSCB"

    possible_subclass = globals().get(callback_class_name, None)

    if possible_subclass and issubclass(possible_subclass, RuleCallback):
        try:
            return possible_subclass.from_rule_dict(rule, runner)
        except Exception:
            LOGGER.warning("Couldn't instantiate a callback for rule %s", rule,
                           exc_info=True)
            infos = {'rule_name': rule['name'],
                     'rulespack_id': rule['rulespack_id']}
            remote_exception = RemoteException(sys.exc_info(), infos)
            runner.queue.put(remote_exception)
            return

    LOGGER.debug("Couldn't find the class matching class_name %s", callback_class_name)
    return


__all__ = ['RecordRequestContext', 'RecordRequestContextDjango',
           'RecordRequestContextFlask', 'RegexpRule', 'HeadersInsertCB',
           'UserAgentMatchesCB', 'HeadersInsertCBFlask', 'HeadersInsertCBDjango',
           'UserAgentMatchesCBDjango',
           'UserAgentMatchesCBFramework', 'ReflectedXSSCB',
           'NotFoundCB', 'NotFoundCBDjango', 'NotFoundCBFlask', 'CountHTTPCodesCB',
           'CountHTTPCodesCBFlask', 'AuthMetricsCB',
           'CrawlerUserAgentMatchesMetricsCB', 'CountHTTPCodesCBDjango',
           'JSCB', 'cb_from_rule']
