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

from storops import exception as ex
from storops.lib.common import instance_cache
from storops.unity.client import UnityClient
from storops.unity.enums import UnityEnum, DNSServerOriginEnum
from storops.unity.resource import UnityResource, UnityResourceList, \
    UnitySingletonResource
from storops.unity.resource.cifs_server import UnityCifsServerList
from storops.unity.resource.cifs_share import UnityCifsShareList
from storops.unity.resource.dns_server import UnityFileDnsServerList
from storops.unity.resource.filesystem import UnityFileSystemList
from storops.unity.resource.interface import UnityFileInterfaceList
from storops.unity.resource.host import UnityHost, UnityHostList, \
    UnityHostIpPortList, UnityHostInitiatorList
from storops.unity.resource.lun import UnityLunList
from storops.unity.resource.nas_server import UnityNasServerList
from storops.unity.resource.nfs_server import UnityNfsServerList
from storops.unity.resource.nfs_share import UnityNfsShareList
from storops.unity.resource.pool import UnityPoolList
from storops.unity.resource.port import UnityIpPortList, UnityIoLimitPolicy, \
    UnityIoLimitPolicyList
from storops.unity.resource.snap import UnitySnapList
from storops.unity.resource.sp import UnityStorageProcessorList
from storops.unity.resource.port import UnityEthernetPortList, \
    UnityIscsiPortalList, UnityFcPortList
from storops.unity.resource.storage_resource import UnityConsistencyGroup, \
    UnityConsistencyGroupList
from storops.unity.resource.vmware import UnityCapabilityProfileList

__author__ = 'Jay Xu'

LOG = logging.getLogger(__name__)


class UnitySystem(UnitySingletonResource):
    def __init__(self, host=None, username=None, password=None,
                 port=443, cli=None, verify=False):
        super(UnitySystem, self).__init__(cli=cli)
        if cli is None:
            self._cli = UnityClient(host, username, password, port,
                                    verify=verify)
        else:
            self._cli = cli

    def get_capability_profile(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityCapabilityProfileList,
                                   _id=_id, name=name, **filters)

    def get_sp(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityStorageProcessorList, _id=_id,
                                   name=name, **filters)

    def get_iscsi_portal(self, _id=None, **filters):
        return self._get_unity_rsc(UnityIscsiPortalList, _id=_id, **filters)

    def get_fc_port(self, _id=None, **filters):
        return self._get_unity_rsc(UnityFcPortList, _id=_id, **filters)

    def get_ethernet_port(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityEthernetPortList, _id=_id,
                                   name=name, **filters)

    def create_host(self, name, host_type=None, desc=None, os=None):
        host = UnityHostList.get(self._cli, name=name)
        if host:
            raise ex.UnityHostNameInUseError()
        else:
            host = UnityHost.create(self._cli, name, host_type=host_type,
                                    desc=desc, os=os)

        return host

    def get_initiator(self, _id=None, **filters):
        return self._get_unity_rsc(UnityHostInitiatorList, _id=_id, **filters)

    def get_lun(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityLunList, _id=_id, name=name, **filters)

    def get_pool(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityPoolList, _id=_id, name=name,
                                   **filters)

    def get_nas_server(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityNasServerList, _id=_id, name=name,
                                   **filters)

    def get_cifs_server(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityCifsServerList, _id=_id, name=name,
                                   **filters)

    def get_nfs_server(self, _id=None, **filters):
        return self._get_unity_rsc(UnityNfsServerList, _id=_id, **filters)

    def get_snap(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnitySnapList, _id=_id, name=name,
                                   **filters)

    def create_nas_server(self, name, sp=None, pool=None, is_repl_dst=None,
                          multi_proto=None):
        if sp is None:
            sp = self.get_sp().first_item

        return sp.create_nas_server(name, pool,
                                    is_repl_dst=is_repl_dst,
                                    multi_proto=multi_proto)

    def get_ip_port(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityIpPortList, _id=_id, name=name,
                                   **filters)

    def get_file_interface(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityFileInterfaceList, _id=_id, name=name,
                                   **filters)

    def get_dns_server(self, _id=None, **filters):
        return self._get_unity_rsc(UnityFileDnsServerList, _id=_id, **filters)

    def get_filesystem(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityFileSystemList, _id=_id, name=name,
                                   **filters)

    def get_cifs_share(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityCifsShareList, _id=_id, name=name,
                                   **filters)

    def get_nfs_share(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityNfsShareList, _id=_id, name=name,
                                   **filters)

    def get_host(self, _id=None, name=None, address=None, **filters):
        ret = UnityHostList.get(self._cli, name='not found')
        if address:
            host_ip_ports = UnityHostIpPortList.get(self._cli, address=address)
            if host_ip_ports:
                ret = host_ip_ports[0].host
        else:
            ret = self._get_unity_rsc(UnityHostList, _id=_id, name=name,
                                      **filters)
        return ret

    def get_io_limit_policy(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityIoLimitPolicyList, _id=_id, name=name,
                                   **filters)

    def create_io_limit_policy(self, name, max_iops=None, max_kbps=None,
                               policy_type=None, is_shared=None,
                               description=None):
        return UnityIoLimitPolicy.create(
            self._cli, name, max_iops=max_iops, max_kbps=max_kbps,
            policy_type=policy_type, is_shared=is_shared,
            description=description)

    def get_cg(self, _id=None, name=None, **filters):
        return self._get_unity_rsc(UnityConsistencyGroupList, _id=_id,
                                   name=name, **filters)

    def create_cg(self, name, description=None, lun_list=None, hosts=None):
        return UnityConsistencyGroup.create(
            self._cli, name, description=description, lun_list=lun_list,
            hosts=hosts)

    def get_doc(self, resource):
        if isinstance(resource, (UnityResource, UnityEnum)):
            clz = resource.__class__
        else:
            clz = resource
        return self._cli.get_doc(clz)

    @property
    @instance_cache
    def _system_time(self):
        return UnitySystemTime(self._cli)

    @property
    def system_time(self):
        return self._system_time.time

    def set_system_time(self, new_time=None):
        return self._system_time.set(new_time)

    @property
    @instance_cache
    def _ntp_server(self):
        return UnityNtpServer(self._cli)

    @property
    def ntp_server(self):
        return self._ntp_server.addresses

    def add_ntp_server(self, *addresses):
        return self._ntp_server.add(*addresses)

    def remove_ntp_server(self, *addresses):
        return self._ntp_server.remove(*addresses)

    def clear_ntp_server(self):
        return self._ntp_server.clear()

    @property
    @instance_cache
    def dns_server(self):
        return UnityDnsServer(self._cli)

    def add_dns_server(self, *addresses):
        return self.dns_server.add(*addresses)

    def remove_dns_server(self, *addresses):
        return self.dns_server.remove(*addresses)

    def clear_dns_server(self, use_dhcp=None):
        """ Clear the DNS server settings.

        :param use_dhcp: default to True, clear all settings and fallback to
                         use DHCP settings.
        :return: last settings
        """
        return self.dns_server.clear(use_dhcp)

    @property
    @instance_cache
    def info(self):
        return UnityBasicSystemInfo.get(cli=self._cli)


class UnitySystemList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnitySystem


class UnityDpe(UnityResource):
    pass


class UnityDpeList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityDpe


class UnityVirusChecker(UnityResource):
    pass


class UnityVirusCheckerList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVirusChecker


class UnityBasicSystemInfo(UnitySingletonResource):
    pass


class UnityBasicSystemInfoList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityBasicSystemInfo


class UnitySystemTime(UnitySingletonResource):
    def set(self, new_time, reboot=None):
        old_time = self.time

        if reboot:
            reboot = 1
        else:
            reboot = 0

        time_str = new_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        resp = self.modify(time=time_str, rebootPrivilege=reboot)
        resp.raise_if_err()
        self.update()
        return old_time


class _UnityNtpDnsServerCommonBase(UnitySingletonResource):
    def _do_modify(self, *addresses):
        raise NotImplementedError('Should be implemented by child classes.')

    def set(self, *addresses):
        exists = self.addresses
        resp = self._do_modify(*addresses)
        resp.raise_if_err()
        self.update()
        return exists

    def add(self, *addresses):
        new_addresses = set(self.addresses).union(set(addresses))
        return self.set(*new_addresses)

    def remove(self, *addresses):
        new_addresses = set(self.addresses) - set(addresses)
        return self.set(*new_addresses)

    def clear(self):
        return self.set()


class UnityNtpServer(_UnityNtpDnsServerCommonBase):
    def _do_modify(self, *addresses):
        return self.modify(addresses=sorted(addresses), rebootPrivilege=0)


class UnityDnsServer(_UnityNtpDnsServerCommonBase):
    def _do_modify(self, *addresses):
        return self.modify(addresses=sorted(addresses))

    def clear(self, use_dhcp=None):
        if use_dhcp is None:
            use_dhcp = True

        if use_dhcp:
            origin = DNSServerOriginEnum.DHCP
        else:
            origin = None

        exists = self.addresses
        resp = self.modify(addresses=[], origin=origin)
        resp.raise_if_err()
        self.update()
        return exists
