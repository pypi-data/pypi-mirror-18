#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/10/18
 """
from __future__ import unicode_literals, absolute_import
from django.utils.module_loading import import_string
from djdg_core import settings
from djdg_core.rest_client import RestClient
import logging
from djdg_core.cache.redis_client import cache
from djdg_core.common_api.user import get_info_by_token


user_sys_client = RestClient(
    host=settings.USER_SYSTEM_HOST,
    base_url=settings.USER_SYSTEM_BASE_URL,
    protocol=settings.USER_SYSTEM_PROTOCOL,
    logger=logging.getLogger(settings.LOGGER_NAME),
    oauth_app_id=settings.USER_SYSTEM_AUTH_APP_ID,
    oauth_app_secret=settings.USER_SYSTEM_AUTH_APP_SECRET
)


def user_fetcher(uid, token):
    """
    获取用户信息
    :param uid:
    :param token:
    :return:
    """
    res = user_sys_client.get_resource(settings.USER_SYSTEM_USER_RESOURCE, token=token)
    ret = res.get(action_to=uid)
    return ret.data


_user_proxy_ = import_string(settings.USER_PROXY)


def get_user_proxy():
    return _user_proxy_


class UserProxy(object):
    """
    用户数据代理
    """
    def __init__(self, uid=None, token=None):
        self.token = token
        self.id = self.pk = uid
        self.__data = None
        if not uid:
            self._fetch_data()

    def _fetch_data(self):
        uid = cache.get(self.token)
        if not uid:
            return None
        self.id = self.pk = int(uid)

    @property
    def data(self):
        if self.__data:
            return self.__data
        res = user_fetcher(self.id, self.token)
        self.__data = res
        return self.__data

    def __getattr__(self, item):
        return self.data.get(item)


class CommonUserProxy(UserProxy):
    """
    公共模块用户代理
    """
    def _fetch_data(self):
        self.__data = get_info_by_token(self.token)
        self.id = self.pk = self.__data['id']
