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

from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import tables as htables
from horizon import tabs

from openstack_dashboard import api

from neutron_vpnaas_dashboard.api import vpn as api_vpn
from neutron_vpnaas_dashboard.dashboards.project.vpn import tables


class IPsecSiteConnectionsTab(tabs.TableTab, htables.DataTableView):
    table_classes = (tables.IPsecSiteConnectionsTable,)
    name = _("IPsec Site Connections")
    slug = "ipsecsiteconnections"
    template_name = ("horizon/common/_detail_table.html")
    FILTERS_MAPPING = {'admin_state_up': {_("up"): True, _("down"): False}}

    def get_ipsecsiteconnectionstable_data(self):
        try:
            filters = self.get_filters()
            tenant_id = self.request.user.tenant_id
            if 'vpnservice' in filters:
                filters['vpnservice_id'] = \
                    [v.id for v in api_vpn.vpnservice_list(
                     self.tab_group.request, tenant_id=tenant_id,
                     name=filters['vpnservice'])]
                del filters['vpnservice']
            if 'ikepolicy' in filters:
                filters['ikepolicy_id'] = \
                    [i.id for i in api_vpn.ikepolicy_list(
                     self.tab_group.request, tenant_id=tenant_id,
                     name=filters['ikepolicy'])]
                del filters['ikepolicy']
            if 'ipsecpolicy' in filters:
                filters['ipsecpolicy_id'] = \
                    [i.id for i in api_vpn.ipsecpolicy_list(
                     self.tab_group.request, tenant_id=tenant_id,
                     name=filters['ipsecpolicy'])]
                del filters['ipsecpolicy']
            ipsecsiteconnections = api_vpn.ipsecsiteconnection_list(
                self.tab_group.request, tenant_id=tenant_id, **filters)
        except Exception:
            ipsecsiteconnections = []
            exceptions.handle(
                self.tab_group.request,
                _('Unable to retrieve IPsec site connections list.'))
        return ipsecsiteconnections

    def get_filters(self):
        self.table = self._tables['ipsecsiteconnectionstable']
        self.handle_server_filter(self.request, table=self.table)
        self.update_server_filter_action(self.request, table=self.table)

        return super(IPsecSiteConnectionsTab,
                     self).get_filters(filters_map=self.FILTERS_MAPPING)


class VPNServicesTab(tabs.TableTab, htables.DataTableView):
    table_classes = (tables.VPNServicesTable,)
    name = _("VPN Services")
    slug = "vpnservices"
    template_name = ("horizon/common/_detail_table.html")

    def get_vpnservicestable_data(self):
        try:
            filters = self.get_filters()
            tenant_id = self.request.user.tenant_id
            if 'subnet_name' in filters:
                subnets = api.neutron.subnet_list(self.tab_group.request,
                                                  tenant_id=tenant_id,
                                                  cidr=filters['subnet_name'])
                subnets_ids = [n.id for n in subnets]
                del filters['subnet_name']
                if not subnets_ids:
                    return []
                filters['subnet_id'] = subnets_ids
            if 'router_name' in filters:
                routers = api.neutron.router_list(self.tab_group.request,
                                                  tenant_id=tenant_id,
                                                  name=filters['router_name'])
                routers_ids = [r.id for r in routers]
                if not routers:
                    return []
                filters['router_id'] = routers_ids
            vpnservices = api_vpn.vpnservice_list(
                self.tab_group.request, tenant_id=tenant_id, **filters)
        except Exception:
            vpnservices = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve VPN services list.'))
        return vpnservices

    def get_filters(self):
        self.table = self._tables['vpnservicestable']
        self.handle_server_filter(self.request, table=self.table)
        self.update_server_filter_action(self.request, table=self.table)

        return super(VPNServicesTab, self).get_filters()


class EndpointGroupTab(tabs.TableTab, htables.DataTableView):
    table_classes = (tables.EndpointGroupTable,)
    name = _("Endpoint Groups")
    slug = "endpointgroups"
    template_name = ("horizon/common/_detail_table.html")

    def get_endpointgroupstable_data(self):
        try:
            filters = self.get_filters()
            tenant_id = self.request.user.tenant_id
            endpointgroups = api_vpn.endpointgroup_list(
                self.tab_group.request, tenant_id=tenant_id, **filters)
        except Exception:
            endpointgroups = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve endpoint group list.'))
        return endpointgroups

    def get_filters(self):
        self.table = self._tables['endpointgroupstable']
        self.handle_server_filter(self.request, table=self.table)
        self.update_server_filter_action(self.request, table=self.table)

        return super(EndpointGroupTab, self).get_filters()


class IKEPoliciesTab(tabs.TableTab, htables.DataTableView):
    table_classes = (tables.IKEPoliciesTable,)
    name = _("IKE Policies")
    slug = "ikepolicies"
    template_name = ("horizon/common/_detail_table.html")

    def get_ikepoliciestable_data(self):
        try:
            filters = self.get_filters()
            tenant_id = self.request.user.tenant_id
            ikepolicies = api_vpn.ikepolicy_list(
                self.tab_group.request, tenant_id=tenant_id, **filters)
        except Exception:
            ikepolicies = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve IKE policies list.'))
        return ikepolicies

    def get_filters(self):
        self.table = self._tables['ikepoliciestable']
        self.handle_server_filter(self.request, table=self.table)
        self.update_server_filter_action(self.request, table=self.table)

        return super(IKEPoliciesTab, self).get_filters()


class IPsecPoliciesTab(tabs.TableTab, htables.DataTableView):
    table_classes = (tables.IPsecPoliciesTable,)
    name = _("IPsec Policies")
    slug = "ipsecpolicies"
    template_name = ("horizon/common/_detail_table.html")

    def get_ipsecpoliciestable_data(self):
        try:
            filters = self.get_filters()
            tenant_id = self.request.user.tenant_id
            ipsecpolicies = api_vpn.ipsecpolicy_list(
                self.tab_group.request, tenant_id=tenant_id, **filters)
        except Exception:
            ipsecpolicies = []
            exceptions.handle(self.tab_group.request,
                              _('Unable to retrieve IPsec policy list.'))
        return ipsecpolicies

    def get_filters(self):
        self.table = self._tables['ipsecpoliciestable']
        self.handle_server_filter(self.request, table=self.table)
        self.update_server_filter_action(self.request, table=self.table)

        return super(IPsecPoliciesTab, self).get_filters()


class VPNTabs(tabs.TabGroup):
    slug = "vpntabs"
    tabs = (IKEPoliciesTab, IPsecPoliciesTab,
            VPNServicesTab, EndpointGroupTab,
            IPsecSiteConnectionsTab,)
    sticky = True


class IKEPolicyDetailsTab(tabs.Tab):
    name = _("IKE Policy Details")
    slug = "ikepolicydetails"
    template_name = "project/vpn/_ikepolicy_details.html"

    def get_context_data(self, request):
        ikepolicy = self.tab_group.kwargs['ikepolicy']
        return {'ikepolicy': ikepolicy}


class IKEPolicyDetailsTabs(tabs.TabGroup):
    slug = "ikepolicytabs"
    tabs = (IKEPolicyDetailsTab,)


class IPsecPolicyDetailsTab(tabs.Tab):
    name = _("IPsec Policy Details")
    slug = "ipsecpolicydetails"
    template_name = "project/vpn/_ipsecpolicy_details.html"

    def get_context_data(self, request):
        ipsecpolicy = self.tab_group.kwargs['ipsecpolicy']
        return {'ipsecpolicy': ipsecpolicy}


class IPsecPolicyDetailsTabs(tabs.TabGroup):
    slug = "ipsecpolicytabs"
    tabs = (IPsecPolicyDetailsTab,)


class VPNServiceDetailsTab(tabs.Tab):
    name = _("VPN Service Details")
    slug = "vpnservicedetails"
    template_name = "project/vpn/_vpnservice_details.html"

    def get_context_data(self, request):
        vpnservice = self.tab_group.kwargs['vpnservice']
        return {'vpnservice': vpnservice}


class VPNServiceDetailsTabs(tabs.TabGroup):
    slug = "vpnservicetabs"
    tabs = (VPNServiceDetailsTab,)


class EndpointGroupDetailsTab(tabs.Tab):
    name = _("Endpoint Groups Details")
    slug = "endpointgroupdetails"
    template_name = "project/vpn/_endpointgroup_details.html"

    def get_context_data(self, request):
        endpointgroup = self.tab_group.kwargs['endpointgroup']
        return {'endpointgroup': endpointgroup}


class EndpointGroupDetailsTabs(tabs.TabGroup):
    slug = "endpointgrouptabs"
    tabs = (EndpointGroupDetailsTab,)


class IPsecSiteConnectionDetailsTab(tabs.Tab):
    name = _("IPsec Site Connection Details")
    slug = "ipsecsiteconnectiondetails"
    template_name = "project/vpn/_ipsecsiteconnection_details.html"

    def get_context_data(self, request):
        ipsecsiteconnection = self.tab_group.kwargs['ipsecsiteconnection']
        return {'ipsecsiteconnection': ipsecsiteconnection}


class IPsecSiteConnectionDetailsTabs(tabs.TabGroup):
    slug = "ipsecsiteconnectiontabs"
    tabs = (IPsecSiteConnectionDetailsTab,)
