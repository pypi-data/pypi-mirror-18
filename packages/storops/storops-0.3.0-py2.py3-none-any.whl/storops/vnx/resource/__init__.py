# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import unicode_literals

from storops.lib.common import instance_cache, clear_instance_cache
from storops.lib.resource import Resource, ResourceList
from storops.vnx.parsers import get_vnx_parser

__author__ = 'Cedric Zhuang'


class VNXResource(Resource):
    @classmethod
    def _get_parser(cls):
        return get_vnx_parser(cls.__name__)

    def _get_value_by_key(self, item):
        ret = super(VNXResource, self)._get_value_by_key(item)
        if ret is None and self._get_parser() is not None:
            prop = self._get_parser().get_property(item)
            if prop and prop.is_resource_list_clazz():
                ret = tuple()
        return ret


class _WithPoll(object):
    def __init__(self, r):
        self._resource = r
        self._orig_poll = self._resource.poll

    def __enter__(self):
        pass

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        # return None, do not handle inner exception
        self._resource.poll = self._orig_poll


class VNXCliResource(VNXResource):
    def __init__(self):
        super(VNXCliResource, self).__init__()
        self.poll = True
        self._cli = None

    def with_poll(self):
        ret = _WithPoll(self)
        self.poll = True
        return ret

    def with_no_poll(self):
        ret = _WithPoll(self)
        self.poll = False
        return ret

    def _get_property_from_raw(self, item):
        value = super(VNXCliResource, self)._get_property_from_raw(item)
        if isinstance(value, VNXCliResource):
            value = self._get_resource_property(value)
        return value

    @instance_cache
    def _get_resource_property(self, value):
        value.set_cli(self._cli)
        return value

    def set_cli(self, cli):
        if cli is not None:
            self._cli = cli

    @clear_instance_cache
    def update(self, data=None):
        return super(VNXCliResource, self).update(data)


class VNXCliResourceList(VNXCliResource, ResourceList):
    @classmethod
    def _get_parser(cls):
        return get_vnx_parser(cls.get_resource_class().__name__)

    @classmethod
    def get_resource_class(cls):
        raise NotImplementedError(
            'should return the class ref of the resource in the list.')

    def __init__(self, cli=None):
        super(VNXCliResourceList, self).__init__()
        self._cli = cli

    def update(self, data=None):
        ret = super(VNXCliResourceList, self).update(data)
        for item in self._list:
            item._cli = self._cli
        return ret

    def set_cli(self, cli):
        super(VNXCliResourceList, self).set_cli(cli)
        for item in self:
            if isinstance(item, VNXCliResource):
                item.set_cli(cli)
