# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Django specific WSGI HTTP Request / Response stuff
"""
from itertools import chain
from logging import getLogger

from .base import BaseRequest
from .ip_utils import get_real_user_ip


LOGGER = getLogger(__name__)


class DjangoRequest(BaseRequest):

    def __init__(self, request, view_func, view_args, view_kwargs):
        super(DjangoRequest, self).__init__()
        self.request = request
        self.view_func = view_func
        self.view_args = view_args
        self.view_kwargs = view_kwargs

        # Cache for params
        self._query_params = None
        self._query_params_values = None
        self._form_params = None

    @property
    def query_params(self):
        if self._query_params is None:
            # Convert django QueryDict to a normal dict with values as list
            self._query_params = dict(self.request.GET.lists())
        return self._query_params

    @property
    def query_params_values(self):
        """ Return only query values as a list
        """
        if self._query_params_values is None:
            self._query_params_values = list(chain.from_iterable(self.query_params.values()))
        return self._query_params_values

    @property
    def form_params(self):
        if self._form_params is None:
            self._form_params = dict(self.request.POST)
        return self._form_params

    @property
    def cookies_params(self):
        return self.request.COOKIES

    @property
    def client_ip(self):
        return get_real_user_ip(self.request.META.get('REMOTE_ADDR'),
                                self.request.META.get('HTTP_X_FORWARDED_FOR', ''))

    @property
    def hostname(self):
        return self.request.get_host()

    @property
    def method(self):
        return self.request.method

    @property
    def referer(self):
        return self.request.META.get('HTTP_REFERER')

    @property
    def client_user_agent(self):
        return self.request.META.get('HTTP_USER_AGENT')

    @property
    def path(self):
        return self.request.path

    @property
    def scheme(self):
        return self.request.scheme

    @property
    def server_port(self):
        return self.request.META.get('SERVER_PORT')

    @property
    def remote_port(self):
        return self.request.META.get('REMOTE_PORT')

    def get_header(self, name):
        """ Get a specific header
        """
        return self.request.META.get(name)

    @property
    def view_params(self):
        return self.view_kwargs
