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

from neutronclient.v2_0 import client

from openstack_dashboard import api
from openstack_dashboard.test import helpers

from neutron_vpnaas_dashboard.api import vpn as api_vpn
from neutron_vpnaas_dashboard.test import helpers as test

neutronclient = client.Client


class VPNaasApiTests(test.APITestCase):

    @helpers.create_mocks({neutronclient: ('create_vpnservice',)})
    def test_vpnservice_create(self):
        vpnservice1 = self.api_vpnservices.first()
        form_data = {
            'name': vpnservice1['name'],
            'description': vpnservice1['description'],
            'subnet_id': vpnservice1['subnet_id'],
            'router_id': vpnservice1['router_id'],
            'admin_state_up': vpnservice1['admin_state_up']
        }

        vpnservice = {'vpnservice': self.api_vpnservices.first()}
        self.mock_create_vpnservice.return_value = vpnservice

        ret_val = api_vpn.vpnservice_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.VPNService)
        self.mock_create_vpnservice.assert_called_once_with(
            {'vpnservice': form_data})

    @helpers.create_mocks({neutronclient: ('list_vpnservices',
                                           'list_ipsec_site_connections'),
                           api.neutron: ('subnet_list', 'router_list')})
    def test_vpnservice_list(self):
        vpnservices = {'vpnservices': self.vpnservices.list()}
        vpnservices_dict = {'vpnservices': self.api_vpnservices.list()}
        subnets = self.subnets.list()
        routers = self.routers.list()
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_list_vpnservices.return_value = vpnservices_dict
        self.mock_subnet_list.return_value = subnets
        self.mock_router_list.return_value = routers
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.vpnservice_list(self.request)
        for (v, d) in zip(ret_val, vpnservices['vpnservices']):
            self.assertIsInstance(v, api_vpn.VPNService)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)

        self.mock_list_vpnservices.assert_called_once_with()
        self.mock_subnet_list.assert_called_once_with(self.request)
        self.mock_router_list.assert_called_once_with(self.request)
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('show_vpnservice',
                                           'list_ipsec_site_connections'),
                           api.neutron: ('subnet_get', 'router_get')})
    def test_vpnservice_get(self):
        vpnservice = self.vpnservices.first()
        vpnservice_dict = {'vpnservice': self.api_vpnservices.first()}
        subnet = self.subnets.first()
        router = self.routers.first()
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_show_vpnservice.return_value = vpnservice_dict
        self.mock_subnet_get.return_value = subnet
        self.mock_router_get.return_value = router
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.vpnservice_get(self.request, vpnservice.id)
        self.assertIsInstance(ret_val, api_vpn.VPNService)

        self.mock_show_vpnservice.assert_called_once_with(vpnservice.id)
        self.mock_subnet_get.assert_called_once_with(self.request, subnet.id)
        self.mock_router_get.assert_called_once_with(self.request, router.id)
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('create_endpoint_group',)})
    def test_endpointgroup_create(self):
        endpointgroup = self.api_endpointgroups.first()
        form_data = {
            'name': endpointgroup['name'],
            'description': endpointgroup['description'],
            'type': endpointgroup['type'],
            'endpoints': endpointgroup['endpoints']
        }

        endpoint_group = {'endpoint_group': self.api_endpointgroups.first()}
        self.mock_create_endpoint_group.return_value = endpoint_group

        ret_val = api_vpn.endpointgroup_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.EndpointGroup)
        self.mock_create_endpoint_group.assert_called_once_with(
            {'endpoint_group': form_data})

    @helpers.create_mocks({neutronclient: ('list_endpoint_groups',
                                           'list_ipsec_site_connections')})
    def test_endpointgroup_list(self):
        endpointgroups = {'endpoint_groups': self.endpointgroups.list()}
        endpointgroups_dict = {
            'endpoint_groups': self.api_endpointgroups.list()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_list_endpoint_groups.return_value = endpointgroups_dict
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.endpointgroup_list(self.request)
        for (v, d) in zip(ret_val, endpointgroups['endpoint_groups']):
            self.assertIsInstance(v, api_vpn.EndpointGroup)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_list_endpoint_groups.assert_called_once_with()
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('show_endpoint_group',
                                           'list_ipsec_site_connections')})
    def test_endpointgroup_get(self):
        endpoint_group = self.endpointgroups.first()
        endpoint_group_dict = {
            'endpoint_group': self.api_endpointgroups.first()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_show_endpoint_group.return_value = endpoint_group_dict
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.endpointgroup_get(self.request, endpoint_group.id)
        self.assertIsInstance(ret_val, api_vpn.EndpointGroup)
        self.mock_show_endpoint_group.assert_called_once_with(
            endpoint_group.id)
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('create_ikepolicy',)})
    def test_ikepolicy_create(self):
        ikepolicy1 = self.api_ikepolicies.first()
        form_data = {
            'name': ikepolicy1['name'],
            'description': ikepolicy1['description'],
            'auth_algorithm': ikepolicy1['auth_algorithm'],
            'encryption_algorithm': ikepolicy1['encryption_algorithm'],
            'ike_version': ikepolicy1['ike_version'],
            'lifetime': ikepolicy1['lifetime'],
            'phase1_negotiation_mode': ikepolicy1['phase1_negotiation_mode'],
            'pfs': ikepolicy1['pfs']
        }

        ikepolicy = {'ikepolicy': self.api_ikepolicies.first()}
        self.mock_create_ikepolicy.return_value = ikepolicy

        ret_val = api_vpn.ikepolicy_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.IKEPolicy)
        self.mock_create_ikepolicy.assert_called_once_with(
            {'ikepolicy': form_data})

    @helpers.create_mocks({neutronclient: ('list_ikepolicies',
                                           'list_ipsec_site_connections')})
    def test_ikepolicy_list(self):
        ikepolicies = {'ikepolicies': self.ikepolicies.list()}
        ikepolicies_dict = {'ikepolicies': self.api_ikepolicies.list()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_list_ikepolicies.return_value = ikepolicies_dict
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.ikepolicy_list(self.request)
        for (v, d) in zip(ret_val, ikepolicies['ikepolicies']):
            self.assertIsInstance(v, api_vpn.IKEPolicy)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_list_ikepolicies.assert_called_once_with()
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('show_ikepolicy',
                                           'list_ipsec_site_connections')})
    def test_ikepolicy_get(self):
        ikepolicy = self.ikepolicies.first()
        ikepolicy_dict = {'ikepolicy': self.api_ikepolicies.first()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_show_ikepolicy.return_value = ikepolicy_dict
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.ikepolicy_get(self.request, ikepolicy.id)
        self.assertIsInstance(ret_val, api_vpn.IKEPolicy)
        self.mock_show_ikepolicy.assert_called_once_with(ikepolicy.id)
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('create_ipsecpolicy',)})
    def test_ipsecpolicy_create(self):
        ipsecpolicy1 = self.api_ipsecpolicies.first()
        form_data = {
            'name': ipsecpolicy1['name'],
            'description': ipsecpolicy1['description'],
            'auth_algorithm': ipsecpolicy1['auth_algorithm'],
            'encryption_algorithm': ipsecpolicy1['encryption_algorithm'],
            'encapsulation_mode': ipsecpolicy1['encapsulation_mode'],
            'lifetime': ipsecpolicy1['lifetime'],
            'pfs': ipsecpolicy1['pfs'],
            'transform_protocol': ipsecpolicy1['transform_protocol']
        }

        ipsecpolicy = {'ipsecpolicy': self.api_ipsecpolicies.first()}
        self.mock_create_ipsecpolicy.return_value = ipsecpolicy

        ret_val = api_vpn.ipsecpolicy_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.IPsecPolicy)
        self.mock_create_ipsecpolicy.assert_called_once_with(
            {'ipsecpolicy': form_data})

    @helpers.create_mocks({neutronclient: ('list_ipsecpolicies',
                                           'list_ipsec_site_connections')})
    def test_ipsecpolicy_list(self):
        ipsecpolicies = {'ipsecpolicies': self.ipsecpolicies.list()}
        ipsecpolicies_dict = {'ipsecpolicies': self.api_ipsecpolicies.list()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_list_ipsecpolicies.return_value = ipsecpolicies_dict
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.ipsecpolicy_list(self.request)
        for (v, d) in zip(ret_val, ipsecpolicies['ipsecpolicies']):
            self.assertIsInstance(v, api_vpn.IPsecPolicy)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_list_ipsecpolicies.assert_called_once_with()
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('show_ipsecpolicy',
                                           'list_ipsec_site_connections')})
    def test_ipsecpolicy_get(self):
        ipsecpolicy = self.ipsecpolicies.first()
        ipsecpolicy_dict = {'ipsecpolicy': self.api_ipsecpolicies.first()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}

        self.mock_show_ipsecpolicy.return_value = ipsecpolicy_dict
        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict

        ret_val = api_vpn.ipsecpolicy_get(self.request, ipsecpolicy.id)
        self.assertIsInstance(ret_val, api_vpn.IPsecPolicy)
        self.mock_show_ipsecpolicy.assert_called_once_with(ipsecpolicy.id)
        self.mock_list_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('create_ipsec_site_connection',)})
    def test_ipsecsiteconnection_create(self):
        ipsecsiteconnection1 = self.api_ipsecsiteconnections.first()
        form_data = {
            'name': ipsecsiteconnection1['name'],
            'description': ipsecsiteconnection1['description'],
            'dpd': ipsecsiteconnection1['dpd'],
            'ikepolicy_id': ipsecsiteconnection1['ikepolicy_id'],
            'initiator': ipsecsiteconnection1['initiator'],
            'ipsecpolicy_id': ipsecsiteconnection1['ipsecpolicy_id'],
            'mtu': ipsecsiteconnection1['mtu'],
            'peer_address': ipsecsiteconnection1['peer_address'],
            'peer_cidrs': ipsecsiteconnection1['peer_cidrs'],
            'peer_id': ipsecsiteconnection1['peer_id'],
            'psk': ipsecsiteconnection1['psk'],
            'vpnservice_id': ipsecsiteconnection1['vpnservice_id'],
            'admin_state_up': ipsecsiteconnection1['admin_state_up']
        }

        ipsecsiteconnection = {'ipsec_site_connection':
                               self.api_ipsecsiteconnections.first()}
        self.mock_create_ipsec_site_connection.return_value = \
            ipsecsiteconnection

        ret_val = api_vpn.ipsecsiteconnection_create(
            self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.IPsecSiteConnection)
        self.mock_create_ipsec_site_connection.assert_called_once_with(
            {'ipsec_site_connection': form_data})

    @helpers.create_mocks({neutronclient: ('list_ipsec_site_connections',
                                           'list_ikepolicies',
                                           'list_ipsecpolicies',
                                           'list_vpnservices')})
    def test_ipsecsiteconnection_list(self):
        ipsecsiteconnections = {
            'ipsec_site_connections': self.ipsecsiteconnections.list()}
        ipsecsiteconnections_dict = {
            'ipsec_site_connections': self.api_ipsecsiteconnections.list()}
        ikepolicies_dict = {'ikepolicies': self.api_ikepolicies.list()}
        ipsecpolicies_dict = {'ipsecpolicies': self.api_ipsecpolicies.list()}
        vpnservices_dict = {'vpnservices': self.api_vpnservices.list()}

        self.mock_list_ipsec_site_connections.return_value = \
            ipsecsiteconnections_dict
        self.mock_list_ikepolicies.return_value = ikepolicies_dict
        self.mock_list_ipsecpolicies.return_value = ipsecpolicies_dict
        self.mock_list_vpnservices.return_value = vpnservices_dict

        ret_val = api_vpn.ipsecsiteconnection_list(self.request)
        for (v, d) in zip(ret_val,
                          ipsecsiteconnections['ipsec_site_connections']):
            self.assertIsInstance(v, api_vpn.IPsecSiteConnection)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_list_ipsec_site_connections.assert_called_once_with()
        self.mock_list_ikepolicies.assert_called_once_with()
        self.mock_list_ipsecpolicies.assert_called_once_with()
        self.mock_list_vpnservices.assert_called_once_with()

    @helpers.create_mocks({neutronclient: ('show_ipsec_site_connection',
                                           'show_ikepolicy',
                                           'show_ipsecpolicy',
                                           'show_vpnservice')})
    def test_ipsecsiteconnection_get(self):
        ipsecsiteconnection = self.ipsecsiteconnections.first()
        connection_dict = {'ipsec_site_connection':
                           self.api_ipsecsiteconnections.first()}
        ikepolicy_dict = {'ikepolicy': self.api_ikepolicies.first()}
        ipsecpolicy_dict = {'ipsecpolicy': self.api_ipsecpolicies.first()}
        vpnservice_dict = {'vpnservice': self.api_vpnservices.first()}

        self.mock_show_ipsec_site_connection.return_value = connection_dict
        self.mock_show_ikepolicy.return_value = ikepolicy_dict
        self.mock_show_ipsecpolicy.return_value = ipsecpolicy_dict
        self.mock_show_vpnservice.return_value = vpnservice_dict

        ret_val = api_vpn.ipsecsiteconnection_get(self.request,
                                                  ipsecsiteconnection.id)
        self.assertIsInstance(ret_val, api_vpn.IPsecSiteConnection)

        self.mock_show_ipsec_site_connection.assert_called_once_with(
            ipsecsiteconnection.id)
        self.mock_show_ikepolicy.assert_called_once_with(
            ipsecsiteconnection.ikepolicy_id)
        self.mock_show_ipsecpolicy.assert_called_once_with(
            ipsecsiteconnection.ipsecpolicy_id)
        self.mock_show_vpnservice.assert_called_once_with(
            ipsecsiteconnection.vpnservice_id)
