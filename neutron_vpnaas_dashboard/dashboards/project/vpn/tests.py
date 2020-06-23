# Copyright 2013, Mirantis Inc
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

from django.urls import reverse

from horizon.workflows import views

from openstack_dashboard import api
from openstack_dashboard.test import helpers

from neutron_vpnaas_dashboard.api import vpn as api_vpn
from neutron_vpnaas_dashboard.dashboards.project.vpn import workflows
from neutron_vpnaas_dashboard.test import helpers as test


class VPNTests(test.TestCase):

    class AttributeDict(dict):
        def __getattr__(self, attr):
            return self[attr]

        def __setattr__(self, attr, value):
            self[attr] = value

    DASHBOARD = 'project'
    INDEX_URL = reverse('horizon:%s:vpn:index' % DASHBOARD)

    ADDIKEPOLICY_PATH = 'horizon:%s:vpn:addikepolicy' % DASHBOARD
    ADDIPSECPOLICY_PATH = 'horizon:%s:vpn:addipsecpolicy' % DASHBOARD
    ADDVPNSERVICE_PATH = 'horizon:%s:vpn:addvpnservice' % DASHBOARD
    ADDENDPOINTGROUP_PATH = 'horizon:%s:vpn:addendpointgroup' % DASHBOARD
    ADDVPNCONNECTION_PATH = 'horizon:%s:vpn:addipsecsiteconnection' % DASHBOARD

    IKEPOLICY_DETAIL_PATH = 'horizon:%s:vpn:ikepolicydetails' % DASHBOARD
    IPSECPOLICY_DETAIL_PATH = 'horizon:%s:vpn:ipsecpolicydetails' % DASHBOARD
    VPNSERVICE_DETAIL_PATH = 'horizon:%s:vpn:vpnservicedetails' % DASHBOARD
    ENDPOINTGROUP_DETAIL_PATH = 'horizon:%s:vpn:endpointgroupdetails' %\
        DASHBOARD
    VPNCONNECTION_DETAIL_PATH = 'horizon:%s:vpn:ipsecsiteconnectiondetails' %\
        DASHBOARD

    UPDATEIKEPOLICY_PATH = 'horizon:%s:vpn:update_ikepolicy' % DASHBOARD
    UPDATEIPSECPOLICY_PATH = 'horizon:%s:vpn:update_ipsecpolicy' % DASHBOARD
    UPDATEVPNSERVICE_PATH = 'horizon:%s:vpn:update_vpnservice' % DASHBOARD
    UPDATEENDPOINTGROUP_PATH = 'horizon:%s:vpn:update_endpointgroup' %\
        DASHBOARD
    UPDATEVPNCONNECTION_PATH = 'horizon:%s:vpn:update_ipsecsiteconnection' %\
        DASHBOARD

    def setup_mocks(self):
        self.mock_vpnservice_list.return_value = self.vpnservices.list()
        self.mock_endpointgroup_list.return_value = self.endpointgroups.list()
        self.mock_ikepolicy_list.return_value = self.ikepolicies.list()
        self.mock_ipsecpolicy_list.return_value = self.ipsecpolicies.list()
        self.mock_ipsecsiteconnection_list.return_value = \
            self.ipsecsiteconnections.list()

    def setup_mocks_with_exception(self):
        self.mock_vpnservice_list.side_effect = self.exceptions.neutron
        self.mock_endpointgroup_list.side_effect = self.exceptions.neutron
        self.mock_ikepolicy_list.side_effect = self.exceptions.neutron
        self.mock_ipsecpolicy_list.side_effect = self.exceptions.neutron
        self.mock_ipsecsiteconnection_list.side_effect = \
            self.exceptions.neutron

    def check_mocks(self):
        self.mock_vpnservice_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_endpointgroup_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_ikepolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_ipsecpolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_ipsecsiteconnection_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_vpnservices(self):
        self.setup_mocks()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__vpnservices')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res, 'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['vpnservicestable_table'].data),
                         len(self.vpnservices.list()))
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_endpointgroups(self):
        self.setup_mocks()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__endpointgroups')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res, 'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['endpointgroupstable_table'].data),
                         len(self.endpointgroups.list()))
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_ikepolicies(self):
        self.setup_mocks()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__ikepolicies')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res, 'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['ikepoliciestable_table'].data),
                         len(self.ikepolicies.list()))
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_ipsecpolicies(self):
        self.setup_mocks()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__ipsecpolicies')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res, 'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['ipsecpoliciestable_table'].data),
                         len(self.ipsecpolicies.list()))
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_ipsecsiteconnections(self):
        self.setup_mocks()

        res = self.client.get(
            self.INDEX_URL + '?tab=vpntabs__ipsecsiteconnections')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res, 'horizon/common/_detail_table.html')
        self.assertEqual(
            len(res.context['ipsecsiteconnectionstable_table'].data),
            len(self.ipsecsiteconnections.list()))
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_exception_vpnservices(self):
        self.setup_mocks_with_exception()

        res = self.client.get(self.INDEX_URL)

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res,
                                'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['table'].data), 0)
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_exception_endpointgroups(self):
        self.setup_mocks_with_exception()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__endpointgroups')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res,
                                'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['table'].data), 0)
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_exception_ikepolicies(self):
        self.setup_mocks_with_exception()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__ikepolicies')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res,
                                'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['table'].data), 0)
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_exception_ipsecpolicies(self):
        self.setup_mocks_with_exception()

        res = self.client.get(self.INDEX_URL + '?tab=vpntabs__ipsecpolicies')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res,
                                'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['table'].data), 0)
        self.check_mocks()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_list')})
    def test_index_exception_ipsecsiteconnections(self):
        self.setup_mocks_with_exception()

        res = self.client.get(
            self.INDEX_URL + '?tab=vpntabs__ipsecsiteconnections')

        self.assertTemplateUsed(res, '%s/vpn/index.html'
                                % self.DASHBOARD)
        self.assertTemplateUsed(res,
                                'horizon/common/_detail_table.html')
        self.assertEqual(len(res.context['table'].data), 0)
        self.check_mocks()

    @helpers.create_mocks({api.neutron: ('network_list_for_tenant',
                                         'router_list')})
    def test_add_vpnservice_get(self):
        networks = [{'subnets': [self.subnets.first(), ]}, ]
        routers = self.routers.list()

        self.mock_network_list_for_tenant.return_value = networks
        self.mock_router_list.return_value = routers

        res = self.client.get(reverse(self.ADDVPNSERVICE_PATH))

        workflow = res.context['workflow']
        self.assertTemplateUsed(res, views.WorkflowView.template_name)
        self.assertEqual(workflow.name, workflows.AddVPNService.name)

        expected_objs = ['<AddVPNServiceStep: addvpnserviceaction>', ]
        self.assertQuerysetEqual(workflow.steps, expected_objs)

        self.mock_network_list_for_tenant.assert_called_once_with(
            helpers.IsHttpRequest(), self.tenant.id)
        self.mock_router_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)

    @helpers.create_mocks({api.neutron: ('router_list',
                                         'network_list_for_tenant'),
                           api_vpn: ('vpnservice_create', )})
    def test_add_vpnservice_post(self):
        vpnservice = self.vpnservices.first()
        networks = [{'subnets': [self.subnets.first(), ]}, ]
        routers = self.routers.list()

        self.mock_network_list_for_tenant.return_value = networks
        self.mock_router_list.return_value = routers

        form_data = {'name': vpnservice['name'],
                     'description': vpnservice['description'],
                     'subnet_id': vpnservice['subnet_id'],
                     'router_id': vpnservice['router_id'],
                     'admin_state_up': vpnservice['admin_state_up']}

        self.mock_vpnservice_create.return_value = vpnservice

        res = self.client.post(reverse(self.ADDVPNSERVICE_PATH), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_network_list_for_tenant.assert_called_once_with(
            helpers.IsHttpRequest(), self.tenant.id)
        self.mock_router_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_vpnservice_create.assert_called_once_with(
            helpers.IsHttpRequest(), **form_data)

    @helpers.create_mocks({api.neutron: ('router_list',
                                         'network_list_for_tenant')})
    def test_add_vpnservice_post_error(self):
        vpnservice = self.vpnservices.first()
        networks = [{'subnets': [self.subnets.first(), ]}, ]
        routers = self.routers.list()

        self.mock_network_list_for_tenant.return_value = networks
        self.mock_router_list.return_value = routers

        form_data = {'name': vpnservice['name'],
                     'description': vpnservice['description'],
                     'subnet_id': '',
                     'router_id': '',
                     'admin_state_up': vpnservice['admin_state_up']}

        res = self.client.post(reverse(self.ADDVPNSERVICE_PATH), form_data)

        self.assertFormErrors(res, 1)

        self.mock_network_list_for_tenant.assert_called_once_with(
            helpers.IsHttpRequest(), self.tenant.id)
        self.mock_router_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)

    @helpers.create_mocks({api.neutron: ('network_list_for_tenant', )})
    def test_add_endpointgroup_get(self):
        networks = [{'subnets': [self.subnets.first(), ]}, ]

        self.mock_network_list_for_tenant.return_value = networks

        res = self.client.get(reverse(self.ADDENDPOINTGROUP_PATH))

        workflow = res.context['workflow']
        self.assertTemplateUsed(res, views.WorkflowView.template_name)
        self.assertEqual(workflow.name, workflows.AddEndpointGroup.name)

        expected_objs = ['<AddEndpointGroupStep: addendpointgroupaction>', ]
        self.assertQuerysetEqual(workflow.steps, expected_objs)
        self.mock_network_list_for_tenant.assert_called_once_with(
            helpers.IsHttpRequest(), self.tenant.id)

    @helpers.create_mocks({api.neutron: ('network_list_for_tenant', ),
                           api_vpn: ('endpointgroup_create', )})
    def test_add_endpointgroup_post(self):
        endpointgroup = self.endpointgroups.first()
        networks = [{'subnets': [self.subnets.first(), ]}, ]

        self.mock_network_list_for_tenant.return_value = networks

        form_data = {'name': endpointgroup['name'],
                     'description': endpointgroup['description'],
                     'subnets': endpointgroup['endpoints'],
                     'type': endpointgroup['type']}

        self.mock_endpointgroup_create.return_value = endpointgroup

        res = self.client.post(reverse(self.ADDENDPOINTGROUP_PATH), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_network_list_for_tenant.assert_called_once_with(
            helpers.IsHttpRequest(), self.tenant.id)
        data = form_data.copy()
        data['endpoints'] = data['subnets']
        del data['subnets']
        self.mock_endpointgroup_create.assert_called_once_with(
            helpers.IsHttpRequest(), **data)

    @helpers.create_mocks({api.neutron: ('network_list_for_tenant', )})
    def test_add_endpointgroup_post_error(self):
        endpointgroup = self.endpointgroups.first()
        networks = [{'subnets': [self.subnets.first(), ]}, ]

        self.mock_network_list_for_tenant.return_value = networks

        form_data = {'name': endpointgroup['name'],
                     'description': endpointgroup['description'],
                     'endpoints': endpointgroup['endpoints'],
                     'type': ''}

        res = self.client.post(reverse(self.ADDENDPOINTGROUP_PATH), form_data)

        self.assertFormErrors(res, 1)
        self.mock_network_list_for_tenant.assert_called_once_with(
            helpers.IsHttpRequest(), self.tenant.id)

    def test_add_ikepolicy_get(self):
        res = self.client.get(reverse(self.ADDIKEPOLICY_PATH))

        workflow = res.context['workflow']
        self.assertTemplateUsed(res, views.WorkflowView.template_name)
        self.assertEqual(workflow.name, workflows.AddIKEPolicy.name)

        expected_objs = ['<AddIKEPolicyStep: addikepolicyaction>', ]
        self.assertQuerysetEqual(workflow.steps, expected_objs)

    @helpers.create_mocks({api_vpn: ('ikepolicy_create', )})
    def test_add_ikepolicy_post(self):
        ikepolicy = self.ikepolicies.first()

        form_data = {'name': ikepolicy['name'],
                     'description': ikepolicy['description'],
                     'auth_algorithm': ikepolicy['auth_algorithm'],
                     'encryption_algorithm': ikepolicy[
                         'encryption_algorithm'],
                     'ike_version': ikepolicy['ike_version'],
                     'lifetime_units': ikepolicy['lifetime']['units'],
                     'lifetime_value': ikepolicy['lifetime']['value'],
                     'phase1_negotiation_mode': ikepolicy[
                         'phase1_negotiation_mode'],
                     'pfs': ikepolicy['pfs']}

        self.mock_ikepolicy_create.return_value = ikepolicy

        res = self.client.post(reverse(self.ADDIKEPOLICY_PATH), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))
        data = form_data.copy()
        data['lifetime'] = {'units': data['lifetime_units'],
                            'value': data['lifetime_value']}
        del data['lifetime_units']
        del data['lifetime_value']
        self.mock_ikepolicy_create.assert_called_once_with(
            helpers.IsHttpRequest(), **data)

    def test_add_ikepolicy_post_error(self):
        ikepolicy = self.ikepolicies.first()

        form_data = {'name': ikepolicy['name'],
                     'description': ikepolicy['description'],
                     'auth_algorithm': ikepolicy['auth_algorithm'],
                     'encryption_algorithm': ikepolicy[
                         'encryption_algorithm'],
                     'ike_version': ikepolicy['ike_version'],
                     'lifetime_units': ikepolicy['lifetime']['units'],
                     'lifetime_value': 10,
                     'phase1_negotiation_mode': ikepolicy[
                         'phase1_negotiation_mode'],
                     'pfs': ikepolicy['pfs']}

        res = self.client.post(reverse(self.ADDIKEPOLICY_PATH), form_data)

        self.assertFormErrors(res, 1)

    def test_add_ipsecpolicy_get(self):
        res = self.client.get(reverse(self.ADDIPSECPOLICY_PATH))

        workflow = res.context['workflow']
        self.assertTemplateUsed(res, views.WorkflowView.template_name)
        self.assertEqual(workflow.name, workflows.AddIPsecPolicy.name)

        expected_objs = ['<AddIPsecPolicyStep: addipsecpolicyaction>', ]
        self.assertQuerysetEqual(workflow.steps, expected_objs)

    @helpers.create_mocks({api_vpn: ('ipsecpolicy_create', )})
    def test_add_ipsecpolicy_post(self):
        ipsecpolicy = self.ipsecpolicies.first()

        form_data = {'name': ipsecpolicy['name'],
                     'description': ipsecpolicy['description'],
                     'auth_algorithm': ipsecpolicy['auth_algorithm'],
                     'encryption_algorithm': ipsecpolicy[
                         'encryption_algorithm'],
                     'encapsulation_mode': ipsecpolicy[
                         'encapsulation_mode'],
                     'lifetime_units': ipsecpolicy['lifetime']['units'],
                     'lifetime_value': ipsecpolicy['lifetime']['value'],
                     'pfs': ipsecpolicy['pfs'],
                     'transform_protocol': ipsecpolicy[
                         'transform_protocol']}

        self.mock_ipsecpolicy_create.return_value = ipsecpolicy

        res = self.client.post(reverse(self.ADDIPSECPOLICY_PATH), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        data = form_data.copy()
        data['lifetime'] = {'units': data['lifetime_units'],
                            'value': data['lifetime_value']}
        del data['lifetime_units']
        del data['lifetime_value']
        self.mock_ipsecpolicy_create.assert_called_once_with(
            helpers.IsHttpRequest(), **data)

    def test_add_ipsecpolicy_post_error(self):
        ipsecpolicy = self.ipsecpolicies.first()

        form_data = {'name': ipsecpolicy['name'],
                     'description': ipsecpolicy['description'],
                     'auth_algorithm': ipsecpolicy['auth_algorithm'],
                     'encryption_algorithm': ipsecpolicy[
                         'encryption_algorithm'],
                     'encapsulation_mode': ipsecpolicy[
                         'encapsulation_mode'],
                     'lifetime_units': ipsecpolicy['lifetime']['units'],
                     'lifetime_value': 10,
                     'pfs': ipsecpolicy['pfs'],
                     'transform_protocol': ipsecpolicy[
                         'transform_protocol']}

        res = self.client.post(reverse(self.ADDIPSECPOLICY_PATH), form_data)

        self.assertFormErrors(res, 1)

    @helpers.create_mocks({api_vpn: ('ikepolicy_list',
                                     'ipsecpolicy_list',
                                     'vpnservice_list',
                                     'endpointgroup_list',)})
    def test_add_ipsecsiteconnection_get(self):
        ikepolicies = self.ikepolicies.list()
        ipsecpolicies = self.ipsecpolicies.list()
        vpnservices = self.vpnservices.list()

        self.mock_ikepolicy_list.return_value = ikepolicies
        self.mock_ipsecpolicy_list.return_value = ipsecpolicies
        self.mock_vpnservice_list.return_value = vpnservices

        res = self.client.get(reverse(self.ADDVPNCONNECTION_PATH))

        workflow = res.context['workflow']
        self.assertTemplateUsed(res, views.WorkflowView.template_name)
        self.assertEqual(workflow.name, workflows.AddIPsecSiteConnection.name)

        expected_objs = ['<AddIPsecSiteConnectionStep: '
                         'addipsecsiteconnectionaction>',
                         '<AddIPsecSiteConnectionOptionalStep: '
                         'addipsecsiteconnectionoptionalaction>', ]
        self.assertQuerysetEqual(workflow.steps, expected_objs)

        self.mock_ikepolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)
        self.mock_ipsecpolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)
        self.mock_vpnservice_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_create')})
    def test_add_ipsecsiteconnection_post(self):
        self._test_add_ipsecsiteconnection_post()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_create')})
    def test_add_ipsecsiteconnection_post_single_subnet(self):
        self._test_add_ipsecsiteconnection_post(subnet_list=False)

    def _test_add_ipsecsiteconnection_post(self, subnet_list=True):
        if subnet_list:
            ipsecsiteconnection = self.ipsecsiteconnections.first()
        else:
            ipsecsiteconnection = self.ipsecsiteconnections.list()[1]
        ikepolicies = self.ikepolicies.list()
        ipsecpolicies = self.ipsecpolicies.list()
        vpnservices = self.vpnservices.list()

        form_data = {
            'name': ipsecsiteconnection['name'],
            'description': ipsecsiteconnection['description'],
            'dpd_action': ipsecsiteconnection['dpd']['action'],
            'dpd_interval': ipsecsiteconnection['dpd']['interval'],
            'dpd_timeout': ipsecsiteconnection['dpd']['timeout'],
            'ikepolicy_id': ipsecsiteconnection['ikepolicy_id'],
            'initiator': ipsecsiteconnection['initiator'],
            'ipsecpolicy_id': ipsecsiteconnection['ipsecpolicy_id'],
            'mtu': ipsecsiteconnection['mtu'],
            'peer_address': ipsecsiteconnection['peer_address'],
            'peer_cidrs': ', '.join(ipsecsiteconnection['peer_cidrs']),
            'peer_id': ipsecsiteconnection['peer_id'],
            'psk': ipsecsiteconnection['psk'],
            'vpnservice_id': ipsecsiteconnection['vpnservice_id'],
            'admin_state_up': ipsecsiteconnection['admin_state_up'],
        }

        self.mock_ikepolicy_list.return_value = ikepolicies
        self.mock_ipsecpolicy_list.return_value = ipsecpolicies
        self.mock_vpnservice_list.return_value = vpnservices
        self.mock_ipsecsiteconnection_create.return_value = ipsecsiteconnection

        res = self.client.post(reverse(self.ADDVPNCONNECTION_PATH), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_ikepolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)
        self.mock_ipsecpolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)
        self.mock_vpnservice_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)

        data = form_data.copy()
        data['peer_cidrs'] = ipsecsiteconnection['peer_cidrs']
        data['dpd'] = {'action': data['dpd_action'],
                       'interval': data['dpd_interval'],
                       'timeout': data['dpd_timeout']}
        del data['dpd_action']
        del data['dpd_interval']
        del data['dpd_timeout']
        data['local_ep_group_id'] = ''
        data['peer_ep_group_id'] = ''

        self.mock_ipsecsiteconnection_create.assert_called_once_with(
            helpers.IsHttpRequest(), **data)

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_create')})
    def test_add_ipsecsiteconnection_post_required_fields_error(self):
        self._test_add_ipsecsiteconnection_post_error()

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ipsecpolicy_list',
                                     'vpnservice_list', 'endpointgroup_list',
                                     'ipsecsiteconnection_create')})
    def test_add_ipsecsiteconnection_post_peer_cidrs_error(self):
        self._test_add_ipsecsiteconnection_post_error(subnets=True)

    def _test_add_ipsecsiteconnection_post_error(self, subnets=False):
        ipsecsiteconnection = self.ipsecsiteconnections.first()
        ikepolicies = self.ikepolicies.list()
        ipsecpolicies = self.ipsecpolicies.list()
        vpnservices = self.vpnservices.list()

        self.mock_ikepolicy_list.return_value = ikepolicies
        self.mock_ipsecpolicy_list.return_value = ipsecpolicies
        self.mock_vpnservice_list.return_value = vpnservices

        form_data = {'name': '',
                     'description': ipsecsiteconnection['description'],
                     'dpd_action': ipsecsiteconnection['dpd']['action'],
                     'dpd_interval': ipsecsiteconnection['dpd']['interval'],
                     'dpd_timeout': ipsecsiteconnection['dpd']['timeout'],
                     'ikepolicy_id': '',
                     'initiator': ipsecsiteconnection['initiator'],
                     'ipsecpolicy_id': '',
                     'mtu': ipsecsiteconnection['mtu'],
                     'peer_address': '',
                     'peer_cidrs': '',
                     'peer_id': '',
                     'psk': '',
                     'vpnservice_id': '',
                     'admin_state_up': ipsecsiteconnection[
                         'admin_state_up']}
        if subnets:
            form_data['peer_cidrs'] = '20.1.0.0/24; 21.1.0.0/24'

        res = self.client.post(reverse(self.ADDVPNCONNECTION_PATH), form_data)

        if subnets:
            self.assertFormErrors(res, 7)
        else:
            self.assertFormErrors(res, 6)

        self.mock_ikepolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)
        self.mock_ipsecpolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)
        self.mock_vpnservice_list.assert_called_once_with(
            helpers.IsHttpRequest(),
            tenant_id=self.tenant.id)

    @helpers.create_mocks({api_vpn: ('vpnservice_get', )})
    def test_update_vpnservice_get(self):
        vpnservice = self.vpnservices.first()

        self.mock_vpnservice_get.return_value = vpnservice

        res = self.client.get(
            reverse(self.UPDATEVPNSERVICE_PATH, args=(vpnservice.id,)))

        self.assertTemplateUsed(
            res, 'project/vpn/update_vpnservice.html')

        self.mock_vpnservice_get.assert_called_once_with(
            helpers.IsHttpRequest(), vpnservice.id)

    @helpers.create_mocks({api_vpn: ('vpnservice_get', 'vpnservice_update')})
    def test_update_vpnservice_post(self):
        vpnservice = self.vpnservices.first()

        self.mock_vpnservice_get.return_value = vpnservice

        data = {'name': vpnservice.name,
                'description': vpnservice.description,
                'admin_state_up': vpnservice.admin_state_up}

        self.mock_vpnservice_update.return_value = vpnservice

        form_data = data.copy()
        form_data['vpnservice_id'] = vpnservice.id

        res = self.client.post(reverse(
            self.UPDATEVPNSERVICE_PATH, args=(vpnservice.id,)), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_vpnservice_get.assert_called_once_with(
            helpers.IsHttpRequest(), vpnservice.id)
        self.mock_vpnservice_update.assert_called_once_with(
            helpers.IsHttpRequest(), vpnservice.id, vpnservice=data)

    @helpers.create_mocks({api_vpn: ('endpointgroup_get', )})
    def test_update_endpointgroup_get(self):
        endpointgroup = self.endpointgroups.first()

        self.mock_endpointgroup_get.return_value = endpointgroup

        res = self.client.get(
            reverse(self.UPDATEENDPOINTGROUP_PATH, args=(endpointgroup.id,)))

        self.assertTemplateUsed(
            res, 'project/vpn/update_endpointgroup.html')

        self.mock_endpointgroup_get.assert_called_once_with(
            helpers.IsHttpRequest(), endpointgroup.id)

    @helpers.create_mocks({api_vpn: ('endpointgroup_get',
                                     'endpointgroup_update')})
    def test_update_endpointgroup_post(self):
        endpointgroup = self.endpointgroups.first()

        data = {'name': endpointgroup.name,
                'description': endpointgroup.description}

        self.mock_endpointgroup_get.return_value = endpointgroup
        self.mock_endpointgroup_update.return_value = endpointgroup

        form_data = data.copy()
        form_data['endpoint_group_id'] = endpointgroup.id

        res = self.client.post(reverse(self.UPDATEENDPOINTGROUP_PATH,
                                       args=(endpointgroup.id, )
                                       ), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_endpointgroup_get.assert_called_once_with(
            helpers.IsHttpRequest(), endpointgroup.id)
        self.mock_endpointgroup_update.assert_called_once_with(
            helpers.IsHttpRequest(), endpointgroup.id, endpoint_group=data)

    @helpers.create_mocks({api_vpn: ('ikepolicy_get', )})
    def test_update_ikepolicy_get(self):
        ikepolicy = self.ikepolicies.first()

        self.mock_ikepolicy_get.return_value = ikepolicy

        res = self.client.get(
            reverse(self.UPDATEIKEPOLICY_PATH, args=(ikepolicy.id,)))

        self.assertTemplateUsed(
            res, 'project/vpn/update_ikepolicy.html')
        self.mock_ikepolicy_get.assert_called_once_with(
            helpers.IsHttpRequest(), ikepolicy.id)

    @helpers.create_mocks({api_vpn: ('ikepolicy_get', 'ikepolicy_update')})
    def test_update_ikepolicy_post(self):
        ikepolicy = self.ikepolicies.first()

        data = {'name': ikepolicy.name,
                'description': ikepolicy.description,
                'auth_algorithm': ikepolicy.auth_algorithm,
                'encryption_algorithm': ikepolicy.encryption_algorithm,
                'ike_version': ikepolicy.ike_version,
                'lifetime': ikepolicy.lifetime,
                'pfs': ikepolicy.pfs,
                'phase1_negotiation_mode': ikepolicy.phase1_negotiation_mode}

        self.mock_ikepolicy_get.return_value = ikepolicy
        self.mock_ikepolicy_update.return_value = ikepolicy

        form_data = data.copy()

        form_data.update({'lifetime_units': form_data['lifetime']['units'],
                          'lifetime_value': form_data['lifetime']['value'],
                          'ikepolicy_id': ikepolicy.id})
        form_data.pop('lifetime')

        res = self.client.post(reverse(
            self.UPDATEIKEPOLICY_PATH, args=(ikepolicy.id,)), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_ikepolicy_get.assert_called_once_with(
            helpers.IsHttpRequest(), ikepolicy.id)
        self.mock_ikepolicy_update.assert_called_once_with(
            helpers.IsHttpRequest(), ikepolicy.id, ikepolicy=data)

    @helpers.create_mocks({api_vpn: ('ipsecpolicy_get', )})
    def test_update_ipsecpolicy_get(self):
        ipsecpolicy = self.ipsecpolicies.first()

        self.mock_ipsecpolicy_get.return_value = ipsecpolicy

        res = self.client.get(
            reverse(self.UPDATEIPSECPOLICY_PATH, args=(ipsecpolicy.id,)))

        self.assertTemplateUsed(
            res, 'project/vpn/update_ipsecpolicy.html')

        self.mock_ipsecpolicy_get.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecpolicy.id)

    @helpers.create_mocks({api_vpn: ('ipsecpolicy_get', 'ipsecpolicy_update')})
    def test_update_ipsecpolicy_post(self):
        ipsecpolicy = self.ipsecpolicies.first()

        self.mock_ipsecpolicy_get.return_value = ipsecpolicy

        data = {'name': ipsecpolicy.name,
                'description': ipsecpolicy.description,
                'auth_algorithm': ipsecpolicy.auth_algorithm,
                'encapsulation_mode': ipsecpolicy.encapsulation_mode,
                'encryption_algorithm': ipsecpolicy.encryption_algorithm,
                'lifetime': ipsecpolicy.lifetime,
                'pfs': ipsecpolicy.pfs,
                'transform_protocol': ipsecpolicy.transform_protocol}

        self.mock_ipsecpolicy_update.return_value = ipsecpolicy

        form_data = data.copy()

        form_data.update({'lifetime_units': form_data['lifetime']['units'],
                          'lifetime_value': form_data['lifetime']['value'],
                          'ipsecpolicy_id': ipsecpolicy.id})
        form_data.pop('lifetime')

        res = self.client.post(reverse(
            self.UPDATEIPSECPOLICY_PATH, args=(ipsecpolicy.id,)), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_ipsecpolicy_get.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecpolicy.id)
        self.mock_ipsecpolicy_update.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecpolicy.id, ipsecpolicy=data)

    @helpers.create_mocks({api_vpn: ('ipsecsiteconnection_get', )})
    def test_update_ipsecsiteconnection_get(self):
        ipsecsiteconnection = self.ipsecsiteconnections.first()

        self.mock_ipsecsiteconnection_get.return_value = ipsecsiteconnection

        res = self.client.get(
            reverse(self.UPDATEVPNCONNECTION_PATH,
                    args=(ipsecsiteconnection.id,)))

        self.assertTemplateUsed(
            res, 'project/vpn/update_ipsecsiteconnection.html')
        self.mock_ipsecsiteconnection_get.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecsiteconnection.id)

    @helpers.create_mocks({api_vpn: ('ipsecsiteconnection_get',
                                     'ipsecsiteconnection_update')})
    def test_update_ipsecsiteconnection_post(self):
        ipsecsiteconnection = self.ipsecsiteconnections.first()

        self.mock_ipsecsiteconnection_get.return_value = ipsecsiteconnection

        data = {'name': ipsecsiteconnection.name,
                'description': ipsecsiteconnection.description,
                'peer_address': ipsecsiteconnection.peer_address,
                'peer_id': ipsecsiteconnection.peer_id,
                'peer_cidrs': ipsecsiteconnection.peer_cidrs,
                'psk': ipsecsiteconnection.psk,
                'mtu': ipsecsiteconnection.mtu,
                'dpd': ipsecsiteconnection.dpd,
                'initiator': ipsecsiteconnection.initiator,
                'admin_state_up': ipsecsiteconnection.admin_state_up}

        self.mock_ipsecsiteconnection_update.return_value = ipsecsiteconnection

        form_data = data.copy()

        form_data.update({
            'dpd_action': form_data['dpd']['action'],
            'dpd_interval': form_data['dpd']['interval'],
            'dpd_timeout': form_data['dpd']['timeout'],
            'peer_cidrs': ", ".join(ipsecsiteconnection['peer_cidrs']),
            'ipsecsiteconnection_id': ipsecsiteconnection.id,
        })
        form_data.pop('dpd')

        res = self.client.post(
            reverse(self.UPDATEVPNCONNECTION_PATH,
                    args=(ipsecsiteconnection.id,)), form_data)

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, str(self.INDEX_URL))

        self.mock_ipsecsiteconnection_get.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecsiteconnection.id)
        self.mock_ipsecsiteconnection_update.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecsiteconnection.id,
            ipsec_site_connection=data)

    @helpers.create_mocks({api_vpn: ('vpnservice_list', 'vpnservice_delete',)})
    def test_delete_vpnservice(self):
        vpnservice = self.vpnservices.list()[1]
        self.mock_vpnservice_list.return_value = self.vpnservices.list()
        self.mock_vpnservice_delete.return_value = None

        form_data = {"action":
                     "vpnservicestable__deletevpnservice__%s" % vpnservice.id}
        res = self.client.post(self.INDEX_URL, form_data)

        self.assertNoFormErrors(res)

        self.mock_vpnservice_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_vpnservice_delete.assert_called_once_with(
            helpers.IsHttpRequest(), vpnservice.id)

    @helpers.create_mocks({api_vpn: ('endpointgroup_list',
                                     'endpointgroup_delete',)})
    def test_delete_endpointgroup(self):
        endpointgroup = self.endpointgroups.list()[0]
        self.mock_endpointgroup_list.return_value = self.endpointgroups.list()
        self.mock_endpointgroup_delete.return_value = None

        form_data = {"action":
                     "endpointgroupstable__deleteendpointgroup__%s"
                     % endpointgroup.id}
        res = self.client.post(self.INDEX_URL, form_data)

        self.assertNoFormErrors(res)

        self.mock_endpointgroup_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_endpointgroup_delete.assert_called_once_with(
            helpers.IsHttpRequest(), endpointgroup.id)

    @helpers.create_mocks({api_vpn: ('ikepolicy_list', 'ikepolicy_delete',)})
    def test_delete_ikepolicy(self):
        ikepolicy = self.ikepolicies.list()[1]
        self.mock_ikepolicy_list.return_value = self.ikepolicies.list()
        self.mock_ikepolicy_delete.return_value = None

        form_data = {"action":
                     "ikepoliciestable__deleteikepolicy__%s" % ikepolicy.id}
        res = self.client.post(self.INDEX_URL, form_data)

        self.assertNoFormErrors(res)

        self.mock_ikepolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_ikepolicy_delete.assert_called_once_with(
            helpers.IsHttpRequest(), ikepolicy.id)

    @helpers.create_mocks({api_vpn: ('ipsecpolicy_list',
                                     'ipsecpolicy_delete',)})
    def test_delete_ipsecpolicy(self):
        ipsecpolicy = self.ipsecpolicies.list()[1]
        self.mock_ipsecpolicy_list.return_value = self.ipsecpolicies.list()
        self.mock_ipsecpolicy_delete.return_value = None

        form_data = {"action":
                     "ipsecpoliciestable__deleteipsecpolicy__%s"
                     % ipsecpolicy.id}
        res = self.client.post(self.INDEX_URL, form_data)

        self.assertNoFormErrors(res)

        self.mock_ipsecpolicy_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_ipsecpolicy_delete.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecpolicy.id)

    @helpers.create_mocks({api_vpn: ('ipsecsiteconnection_list',
                                     'ipsecsiteconnection_delete',)})
    def test_delete_ipsecsiteconnection(self):
        ipsecsiteconnection = self.ipsecsiteconnections.first()
        self.mock_ipsecsiteconnection_list.return_value = \
            self.ipsecsiteconnections.list()
        self.mock_ipsecsiteconnection_delete.return_value = None

        form_data = {"action":
                     "ipsecsiteconnectionstable__deleteipsecsiteconnection__%s"
                     % ipsecsiteconnection.id}
        res = self.client.post(self.INDEX_URL, form_data)

        self.assertNoFormErrors(res)

        self.mock_ipsecsiteconnection_list.assert_called_once_with(
            helpers.IsHttpRequest(), tenant_id=self.tenant.id)
        self.mock_ipsecsiteconnection_delete.assert_called_once_with(
            helpers.IsHttpRequest(), ipsecsiteconnection.id)
