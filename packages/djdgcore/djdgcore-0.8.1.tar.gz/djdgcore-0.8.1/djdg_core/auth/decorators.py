#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/8/8
 """
from __future__ import unicode_literals, absolute_import
from djdg_core.auth.middleware import AuthenticationMiddleware


def permit_all_access(view):
    setattr(view, AuthenticationMiddleware.PERMIT_ALL_PARAM, True)
    return view
