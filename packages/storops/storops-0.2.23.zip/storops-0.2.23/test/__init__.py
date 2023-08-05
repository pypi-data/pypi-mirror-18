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

import logging
import unittest

from hamcrest import assert_that, not_none

from test.unity.rest_mock import patch_rest
from test.vnx.cli_mock import patch_cli

import storops

__author__ = 'Cedric Zhuang'

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    level=logging.DEBUG)


class StoropsTest(unittest.TestCase):
    @patch_cli
    def test_vnx_availability(self):
        vnx = storops.VNXSystem('10.244.211.30')
        assert_that(vnx, not_none())

    @patch_rest
    def test_unity_availability(self):
        unity = storops.UnitySystem('1.1.1.1', 'admin', 'password')
        assert_that(unity, not_none())

    def test_vnx_enum_availability(self):
        spa = storops.VNXSPEnum.SP_A
        assert_that(spa, not_none())

    def test_unity_enum_availability(self):
        raid5 = storops.RaidTypeEnum.RAID5
        assert_that(raid5, not_none())
