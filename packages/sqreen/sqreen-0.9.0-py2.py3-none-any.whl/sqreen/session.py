# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" High-level interaction with sqreen API
"""
import logging

from .http_client import InvalidStatusCodeResponse, StatusFailedResponse

LOGGER = logging.getLogger(__name__)


class InvalidToken(Exception):
    """ Exception raise when a login fails because of the token value
    """
    pass


class Session(object):
    """ Class responsible for collection date and interacting with the sqreen API
    """

    def __init__(self, connection, api_key):
        self.connection = connection
        self.api_key = api_key
        self.session_token = None

    def login(self, runtime_infos):
        """ Login to the backend
        """
        headers = {'x-api-key': self.api_key}

        try:
            result = self.connection.post('app-login', runtime_infos,
                                          headers=headers,
                                          retries=self.connection.RETRY_LONG)
        except InvalidStatusCodeResponse as exc:
            LOGGER.error("Cannot login. Token may be invalid: %s", self.api_key)
            LOGGER.error("Invalid response: %s", exc.response_data)
            if exc.status in (401, 403):
                raise InvalidToken()
            raise
        except StatusFailedResponse as exc:
            LOGGER.error("Cannot login. Token may be invalid: %s", self.api_key)
            LOGGER.error("Invalid response: %s", exc.response)
            raise InvalidToken()

        LOGGER.debug("Received session_id %s", result['session_id'])
        self.session_token = result['session_id']

        return result

    def is_connected(self):
        """ Return a boolean indicating if a successfull login was made
        """
        return self.session_token is not None

    def _headers(self):
        """ Return authentication headers
        """
        return {'x-session-key': self.session_token}

    def _get(self, url, retries=None):
        """ Call connection.get with right headers
        """
        return self.connection.get(url, headers=self._headers(),
                                   retries=retries)

    def _post(self, url, data, retries=None):
        """ Call connection.get with right headers
        """
        return self.connection.post(url, data, headers=self._headers(),
                                    retries=retries)

    def logout(self):
        """ Logout current instance in the backend
        """
        return self._get('app-logout', retries=self.connection.RETRY_ONCE)

    def heartbeat(self):
        """ Tell the backend that the instance is still up and retrieve latest
        commands
        """
        return self._get('app-beat', retries=self.connection.RETRY)

    def post_attack(self, attack):
        """ Report an attack on the backend
        """
        LOGGER.debug("Post attack %s", attack)
        return self._post('attack', attack, retries=self.connection.RETRY_LONG)

    def post_commands_result(self, commands_result):
        """ Report commands result
        """
        return self._post('commands', commands_result, retries=self.connection.RETRY_LONG)

    def post_sqreen_exception(self, exception):
        """ Report sqreen exception
        """
        return self._post('sqreen_exception', exception, retries=self.connection.RETRY)

    def post_metrics(self, metrics):
        """ Post metrics aggregates to the backend
        """
        # Don't send empty metrics payload
        if len(metrics) < 1:
            return

        data = {'metrics': metrics}
        return self._post('metrics', data, retries=self.connection.RETRY_LONG)

    def get_rulespack(self):
        """ Retrieve rulespack from backend
        """
        return self._get('rulespack', retries=self.connection.RETRY_LONG)

    def post_batch(self, batch):
        """ Post a batch to the backend
        """
        LOGGER.debug("Post batch of size %d", len(batch))
        return self._post('batch', {'batch': batch},
                          retries=self.connection.RETRY_LONG)
