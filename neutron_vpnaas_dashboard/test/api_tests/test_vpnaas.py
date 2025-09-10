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

from openstack.network.v2._proxy import Proxy as networkclient
from openstack_dashboard import api
from openstack_dashboard.test import helpers

from neutron_vpnaas_dashboard.api import vpn as api_vpn
from neutron_vpnaas_dashboard.test import helpers as test


class VPNaasApiTests(test.APITestCase):

    @helpers.create_mocks({networkclient: ('create_vpn_service',)})
    def test_vpnservice_create(self):
        vpnservice1 = self.api_vpnservices[0]
        form_data = {
            'name': vpnservice1['name'],
            'description': vpnservice1['description'],
            'subnet_id': vpnservice1['subnet_id'],
            'router_id': vpnservice1['router_id'],
            'admin_state_up': vpnservice1['admin_state_up']
        }

        vpnservice = self.api_vpnservices[0]
        self.mock_create_vpn_service.return_value = vpnservice

        ret_val = api_vpn.vpnservice_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.VPNService)
        self.mock_create_vpn_service.assert_called_once_with(**form_data)

    @helpers.create_mocks({networkclient: ('vpn_services',
                                           'vpn_ipsec_site_connections'),
                           api.neutron: ('subnet_list', 'router_list')})
    def test_vpnservice_list(self):
        vpnservices = self.api_vpnservices
        subnets = self.subnets.list()
        routers = self.routers.list()

        self.mock_vpn_services.return_value = vpnservices
        self.mock_subnet_list.return_value = subnets
        self.mock_router_list.return_value = routers
        self.mock_vpn_ipsec_site_connections.return_value = (
            self.api_ipsecsiteconnections)

        ret_val = api_vpn.vpnservice_list(self.request)
        for (v, d) in zip(ret_val, self.vpnservices.list()):
            self.assertIsInstance(v, api_vpn.VPNService)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)

        self.mock_vpn_services.assert_called_once_with()
        self.mock_subnet_list.assert_called_once_with(self.request)
        self.mock_router_list.assert_called_once_with(self.request)
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('get_vpn_service',
                                           'vpn_ipsec_site_connections'),
                           api.neutron: ('subnet_get', 'router_get')})
    def test_vpnservice_get(self):
        vpnservice = self.api_vpnservices[0]
        subnet = self.subnets.first()
        router = self.routers.first()

        self.mock_get_vpn_service.return_value = vpnservice
        self.mock_subnet_get.return_value = subnet
        self.mock_router_get.return_value = router
        self.mock_vpn_ipsec_site_connections.return_value = (
            self.api_ipsecsiteconnections)

        ret_val = api_vpn.vpnservice_get(self.request, vpnservice.id)
        self.assertIsInstance(ret_val, api_vpn.VPNService)

        self.mock_get_vpn_service.assert_called_once_with(vpnservice.id)
        self.mock_subnet_get.assert_called_once_with(self.request, subnet.id)
        self.mock_router_get.assert_called_once_with(self.request, router.id)
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('create_vpn_endpoint_group',)})
    def test_endpointgroup_create(self):
        endpointgroup = self.api_endpointgroups[0].to_dict()
        form_data = {
            'name': endpointgroup['name'],
            'description': endpointgroup['description'],
            'type': endpointgroup['type'],
            'endpoints': endpointgroup['endpoints']
        }

        self.mock_create_vpn_endpoint_group.return_value = (
            self.api_endpointgroups[0])

        ret_val = api_vpn.endpointgroup_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.EndpointGroup)
        self.mock_create_vpn_endpoint_group.assert_called_once_with(
            **form_data)

    @helpers.create_mocks({networkclient: ('vpn_endpoint_groups',
                                           'vpn_ipsec_site_connections')})
    def test_endpointgroup_list(self):
        endpointgroups = self.api_endpointgroups

        self.mock_vpn_endpoint_groups.return_value = endpointgroups
        self.mock_vpn_ipsec_site_connections.return_value = \
            self.api_ipsecsiteconnections

        ret_val = api_vpn.endpointgroup_list(self.request)
        for (v, d) in zip(ret_val, self.endpointgroups.list()):
            self.assertIsInstance(v, api_vpn.EndpointGroup)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_vpn_endpoint_groups.assert_called_once_with()
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('get_vpn_endpoint_group',
                                           'vpn_ipsec_site_connections')})
    def test_endpointgroup_get(self):
        endpoint_group = self.api_endpointgroups[0]

        self.mock_get_vpn_endpoint_group.return_value = endpoint_group
        self.mock_vpn_ipsec_site_connections.return_value = \
            self.api_ipsecsiteconnections

        ret_val = api_vpn.endpointgroup_get(self.request, endpoint_group.id)
        self.assertIsInstance(ret_val, api_vpn.EndpointGroup)
        self.mock_get_vpn_endpoint_group.assert_called_once_with(
            endpoint_group.id)
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('create_vpn_ike_policy',)})
    def test_ikepolicy_create(self):
        ikepolicy1 = self.api_ikepolicies[0].to_dict()
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

        ikepolicy = self.api_ikepolicies[0]
        self.mock_create_vpn_ike_policy.return_value = ikepolicy

        ret_val = api_vpn.ikepolicy_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.IKEPolicy)
        self.mock_create_vpn_ike_policy.assert_called_once_with(**form_data)

    @helpers.create_mocks({networkclient: ('vpn_ike_policies',
                                           'vpn_ipsec_site_connections')})
    def test_ikepolicy_list(self):
        ikepolicies = self.api_ikepolicies
        ipsecsiteconnections = self.api_ipsecsiteconnections

        self.mock_vpn_ike_policies.return_value = ikepolicies
        self.mock_vpn_ipsec_site_connections.return_value = \
            ipsecsiteconnections

        ret_val = api_vpn.ikepolicy_list(self.request)
        for (v, d) in zip(ret_val, self.ikepolicies.list()):
            self.assertIsInstance(v, api_vpn.IKEPolicy)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_vpn_ike_policies.assert_called_once_with()
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('get_vpn_ike_policy',
                                           'vpn_ipsec_site_connections')})
    def test_ikepolicy_get(self):
        ikepolicy = self.api_ikepolicies[0]
        ipsecsiteconnections = self.api_ipsecsiteconnections

        self.mock_get_vpn_ike_policy.return_value = ikepolicy
        self.mock_vpn_ipsec_site_connections.return_value = \
            ipsecsiteconnections

        ret_val = api_vpn.ikepolicy_get(self.request, ikepolicy.id)
        self.assertIsInstance(ret_val, api_vpn.IKEPolicy)
        self.mock_get_vpn_ike_policy.assert_called_once_with(ikepolicy.id)
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('create_vpn_ipsec_policy',)})
    def test_ipsecpolicy_create(self):
        ipsecpolicy1 = self.ipsecpolicies.first()
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

        ipsecpolicy = self.api_ipsecpolicies[0]
        self.mock_create_vpn_ipsec_policy.return_value = ipsecpolicy

        ret_val = api_vpn.ipsecpolicy_create(self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.IPsecPolicy)
        self.mock_create_vpn_ipsec_policy.assert_called_once_with(**form_data)

    @helpers.create_mocks({networkclient: ('vpn_ipsec_policies',
                                           'vpn_ipsec_site_connections')})
    def test_ipsecpolicy_list(self):
        ipsecpolicies = self.api_ipsecpolicies

        self.mock_vpn_ipsec_policies.return_value = ipsecpolicies
        self.mock_vpn_ipsec_site_connections.return_value = \
            self.api_ipsecsiteconnections

        ret_val = api_vpn.ipsecpolicy_list(self.request)
        for (v, d) in zip(ret_val, self.ipsecpolicies.list()):
            self.assertIsInstance(v, api_vpn.IPsecPolicy)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_vpn_ipsec_policies.assert_called_once_with()
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('get_vpn_ipsec_policy',
                                           'vpn_ipsec_site_connections')})
    def test_ipsecpolicy_get(self):
        ipsecpolicy = self.api_ipsecpolicies[0]
        ipsecsiteconnections = self.api_ipsecsiteconnections

        self.mock_get_vpn_ipsec_policy.return_value = ipsecpolicy
        self.mock_vpn_ipsec_site_connections.return_value = \
            ipsecsiteconnections

        ret_val = api_vpn.ipsecpolicy_get(self.request, ipsecpolicy.id)
        self.assertIsInstance(ret_val, api_vpn.IPsecPolicy)
        self.mock_get_vpn_ipsec_policy.assert_called_once_with(ipsecpolicy.id)
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()

    @helpers.create_mocks({networkclient:
                           ('create_vpn_ipsec_site_connection',)})
    def test_ipsecsiteconnection_create(self):
        ipsecsiteconnection1 = self.ipsecsiteconnections.first()
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

        ipsecsiteconnection = self.api_ipsecsiteconnections[0]
        self.mock_create_vpn_ipsec_site_connection.return_value = \
            ipsecsiteconnection

        ret_val = api_vpn.ipsecsiteconnection_create(
            self.request, **form_data)
        self.assertIsInstance(ret_val, api_vpn.IPsecSiteConnection)
        self.mock_create_vpn_ipsec_site_connection.assert_called_once_with(
            **form_data)

    @helpers.create_mocks({networkclient: ('vpn_ipsec_site_connections',
                                           'vpn_ike_policies',
                                           'vpn_ipsec_policies',
                                           'vpn_services')})
    def test_ipsecsiteconnection_list(self):
        ipsecsiteconnections = self.api_ipsecsiteconnections
        ikepolicies = self.api_ikepolicies
        ipsecpolicies = self.api_ipsecpolicies
        vpnservices = self.api_vpnservices

        self.mock_vpn_ipsec_site_connections.return_value = \
            ipsecsiteconnections
        self.mock_vpn_ike_policies.return_value = ikepolicies
        self.mock_vpn_ipsec_policies.return_value = ipsecpolicies
        self.mock_vpn_services.return_value = vpnservices

        ret_val = api_vpn.ipsecsiteconnection_list(self.request)
        for (v, d) in zip(ret_val, self.ipsecsiteconnections.list()):
            self.assertIsInstance(v, api_vpn.IPsecSiteConnection)
            self.assertTrue(v.name, d.name)
            self.assertTrue(v.id)
        self.mock_vpn_ipsec_site_connections.assert_called_once_with()
        self.mock_vpn_ike_policies.assert_called_once_with()
        self.mock_vpn_ipsec_policies.assert_called_once_with()
        self.mock_vpn_services.assert_called_once_with()

    @helpers.create_mocks({networkclient: ('get_vpn_ipsec_site_connection',
                                           'get_vpn_ike_policy',
                                           'get_vpn_ipsec_policy',
                                           'get_vpn_service')})
    def test_ipsecsiteconnection_get(self):
        ipsecsiteconnection = self.ipsecsiteconnections.first()
        connection = self.api_ipsecsiteconnections[0]
        ikepolicy = self.api_ikepolicies[0]
        ipsecpolicy = self.api_ipsecpolicies[0]
        vpnservice = self.api_vpnservices[0]

        self.mock_get_vpn_ipsec_site_connection.return_value = connection
        self.mock_get_vpn_ike_policy.return_value = ikepolicy
        self.mock_get_vpn_ipsec_policy.return_value = ipsecpolicy
        self.mock_get_vpn_service.return_value = vpnservice

        ret_val = api_vpn.ipsecsiteconnection_get(self.request,
                                                  ipsecsiteconnection.id)
        self.assertIsInstance(ret_val, api_vpn.IPsecSiteConnection)

        self.mock_get_vpn_ipsec_site_connection.assert_called_once_with(
            ipsecsiteconnection.id)
        self.mock_get_vpn_ike_policy.assert_called_once_with(
            ipsecsiteconnection.ikepolicy_id)
        self.mock_get_vpn_ipsec_policy.assert_called_once_with(
            ipsecsiteconnection.ipsecpolicy_id)
        self.mock_get_vpn_service.assert_called_once_with(
            ipsecsiteconnection.vpnservice_id)
