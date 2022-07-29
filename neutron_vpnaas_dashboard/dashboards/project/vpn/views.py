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
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tabs as horizon_tabs
from horizon.utils import memoized
from horizon import workflows as horizon_workflows

from neutron_vpnaas_dashboard.api import vpn as api_vpn
from neutron_vpnaas_dashboard.dashboards.project.vpn import forms
from neutron_vpnaas_dashboard.dashboards.project.vpn import tables
from neutron_vpnaas_dashboard.dashboards.project.vpn import tabs
from neutron_vpnaas_dashboard.dashboards.project.vpn import workflows


class IndexView(horizon_tabs.TabbedTableView):
    tab_group_class = tabs.VPNTabs
    template_name = 'project/vpn/index.html'
    page_title = _("Virtual Private Network")


class AddVPNServiceView(horizon_workflows.WorkflowView):
    workflow_class = workflows.AddVPNService


class AddEndpointGroupView(horizon_workflows.WorkflowView):
    workflow_class = workflows.AddEndpointGroup


class AddIPsecSiteConnectionView(horizon_workflows.WorkflowView):
    workflow_class = workflows.AddIPsecSiteConnection


class AddIKEPolicyView(horizon_workflows.WorkflowView):
    workflow_class = workflows.AddIKEPolicy


class AddIPsecPolicyView(horizon_workflows.WorkflowView):
    workflow_class = workflows.AddIPsecPolicy


class IKEPolicyDetailsView(horizon_tabs.TabView):
    tab_group_class = tabs.IKEPolicyDetailsTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ ikepolicy.name|default:ikepolicy.id }}"

    @memoized.memoized_method
    def get_data(self):
        pid = self.kwargs['ikepolicy_id']
        try:
            return api_vpn.ikepolicy_get(self.request, pid)
        except Exception:
            msg = _('Unable to retrieve IKE policy details.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = super(IKEPolicyDetailsView, self).get_context_data(**kwargs)
        ikepolicy = self.get_data()
        table = tables.IKEPoliciesTable(self.request)
        context["ikepolicy"] = ikepolicy
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(ikepolicy)
        return context

    def get_tabs(self, request, *args, **kwargs):
        ikepolicy = self.get_data()
        return self.tab_group_class(request, ikepolicy=ikepolicy, **kwargs)

    @staticmethod
    def get_redirect_url():
        return reverse('horizon:project:vpn:index')


class IPsecPolicyDetailsView(horizon_tabs.TabView):
    tab_group_class = tabs.IPsecPolicyDetailsTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ ipsecpolicy.name|default:ipsecpolicy.id }}"

    @memoized.memoized_method
    def get_data(self):
        pid = self.kwargs['ipsecpolicy_id']
        try:
            return api_vpn.ipsecpolicy_get(self.request, pid)
        except Exception:
            msg = _('Unable to retrieve IPsec policy details.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = super(IPsecPolicyDetailsView, self).get_context_data(
            **kwargs)
        ipsecpolicy = self.get_data()
        table = tables.IPsecPoliciesTable(self.request)
        context["ipsecpolicy"] = ipsecpolicy
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(ipsecpolicy)
        return context

    def get_tabs(self, request, *args, **kwargs):
        ipsecpolicy = self.get_data()
        return self.tab_group_class(request, ipsecpolicy=ipsecpolicy, **kwargs)

    @staticmethod
    def get_redirect_url():
        return reverse('horizon:project:vpn:index')


class VPNServiceDetailsView(horizon_tabs.TabView):
    tab_group_class = tabs.VPNServiceDetailsTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ vpnservice.name|default:vpnservice.id }}"

    @memoized.memoized_method
    def get_data(self):
        sid = self.kwargs['vpnservice_id']

        try:
            vpnservice = api_vpn.vpnservice_get(self.request, sid)
        except Exception:
            vpnservice = []
            msg = _('Unable to retrieve VPN service details.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())
        try:
            connections = api_vpn.ipsecsiteconnection_list(
                self.request, vpnservice_id=sid)
            vpnservice.vpnconnections = connections
        except Exception:
            vpnservice.vpnconnections = []

        return vpnservice

    def get_context_data(self, **kwargs):
        context = super(VPNServiceDetailsView, self).get_context_data(**kwargs)
        vpnservice = self.get_data()
        table = tables.VPNServicesTable(self.request)
        context["vpnservice"] = vpnservice
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(vpnservice)
        return context

    def get_tabs(self, request, *args, **kwargs):
        vpnservice = self.get_data()
        return self.tab_group_class(request, vpnservice=vpnservice, **kwargs)

    @staticmethod
    def get_redirect_url():
        return reverse('horizon:project:vpn:index')


class EndpointGroupDetailsView(horizon_tabs.TabView):
    tab_group_class = tabs.EndpointGroupDetailsTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ endpointgroup.name|default:endpointgroup.id }}"

    @memoized.memoized_method
    def get_data(self):
        gid = self.kwargs['endpoint_group_id']

        try:
            endpointgroup = api_vpn.endpointgroup_get(self.request, gid)
        except Exception:
            msg = _('Unable to retrieve endpoint group details.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())
        try:
            connections = api_vpn.ipsecsiteconnection_list(
                self.request, endpoint_group_id=gid)
            endpointgroup.vpnconnections = connections
        except Exception:
            endpointgroup.vpnconnections = []

        return endpointgroup

    def get_context_data(self, **kwargs):
        context = super(EndpointGroupDetailsView, self).get_context_data(
            **kwargs)
        endpointgroup = self.get_data()
        table = tables.EndpointGroupTable(self.request)
        context["endpointgroup"] = endpointgroup
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(endpointgroup)
        return context

    def get_tabs(self, request, *args, **kwargs):
        endpointgroup = self.get_data()
        return self.tab_group_class(request, endpointgroup=endpointgroup,
                                    **kwargs)

    @staticmethod
    def get_redirect_url():
        return reverse('horizon:project:vpn:index')


class IPsecSiteConnectionDetailsView(horizon_tabs.TabView):
    tab_group_class = tabs.IPsecSiteConnectionDetailsTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ ipsecsiteconnection.name|default:ipsecsiteconnection.id}}"

    @memoized.memoized_method
    def get_data(self):
        cid = self.kwargs['ipsecsiteconnection_id']
        try:
            return api_vpn.ipsecsiteconnection_get(self.request, cid)
        except Exception:
            msg = _('Unable to retrieve IPsec site connection details.')
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = super(IPsecSiteConnectionDetailsView, self).get_context_data(
            **kwargs)
        ipsecsiteconnection = self.get_data()
        table = tables.IPsecSiteConnectionsTable(self.request)
        context["ipsecsiteconnection"] = ipsecsiteconnection
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(ipsecsiteconnection)
        return context

    def get_tabs(self, request, *args, **kwargs):
        ipsecsiteconnection = self.get_data()
        return self.tab_group_class(request,
                                    ipsecsiteconnection=ipsecsiteconnection,
                                    **kwargs)

    @staticmethod
    def get_redirect_url():
        return reverse('horizon:project:vpn:index')


class UpdateVPNServiceView(horizon_forms.ModalFormView):
    form_class = forms.UpdateVPNService
    form_id = "update_vpnservice_form"
    template_name = "project/vpn/update_vpnservice.html"
    context_object_name = 'vpnservice'
    submit_label = _("Save Changes")
    submit_url = "horizon:project:vpn:update_vpnservice"
    success_url = reverse_lazy("horizon:project:vpn:index")
    page_title = _("Edit VPN Service")

    def get_context_data(self, **kwargs):
        context = super(UpdateVPNServiceView, self).get_context_data(**kwargs)
        context["vpnservice_id"] = self.kwargs['vpnservice_id']
        args = (self.kwargs['vpnservice_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        vpnservice_id = self.kwargs['vpnservice_id']
        try:
            return api_vpn.vpnservice_get(self.request, vpnservice_id)
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve VPN service details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        vpnservice = self._get_object()
        return {'name': vpnservice['name'],
                'vpnservice_id': vpnservice['id'],
                'description': vpnservice['description'],
                'admin_state_up': vpnservice['admin_state_up']}


class UpdateEndpointGroupView(horizon_forms.ModalFormView):
    form_class = forms.UpdateEndpointGroup
    form_id = "update_endpointgroup_form"
    template_name = "project/vpn/update_endpointgroup.html"
    context_object_name = 'endpointgroup'
    submit_label = _("Save Changes")
    submit_url = "horizon:project:vpn:update_endpointgroup"
    success_url = reverse_lazy("horizon:project:vpn:index")
    page_title = _("Edit Endpoint Group")

    def get_context_data(self, **kwargs):
        context = super(UpdateEndpointGroupView, self).get_context_data(
            **kwargs)
        context["endpoint_group_id"] = self.kwargs['endpoint_group_id']
        args = (self.kwargs['endpoint_group_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        endpoint_group_id = self.kwargs['endpoint_group_id']
        try:
            return api_vpn.endpointgroup_get(self.request, endpoint_group_id)
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve endpoint group details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        endpointgroup = self._get_object()
        return {'name': endpointgroup['name'],
                'endpoint_group_id': endpointgroup['id'],
                'description': endpointgroup['description']}


class UpdateIKEPolicyView(horizon_forms.ModalFormView):
    form_class = forms.UpdateIKEPolicy
    form_id = "update_ikepolicy_form"
    template_name = "project/vpn/update_ikepolicy.html"
    context_object_name = 'ikepolicy'
    submit_label = _("Save Changes")
    submit_url = "horizon:project:vpn:update_ikepolicy"
    success_url = reverse_lazy("horizon:project:vpn:index")
    page_title = _("Edit IKE Policy")

    def get_context_data(self, **kwargs):
        context = super(UpdateIKEPolicyView, self).get_context_data(**kwargs)
        context["ikepolicy_id"] = self.kwargs['ikepolicy_id']
        args = (self.kwargs['ikepolicy_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        ikepolicy_id = self.kwargs['ikepolicy_id']
        try:
            return api_vpn.ikepolicy_get(self.request, ikepolicy_id)
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve IKE policy details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        ikepolicy = self._get_object()
        return {'name': ikepolicy['name'],
                'ikepolicy_id': ikepolicy['id'],
                'description': ikepolicy['description'],
                'auth_algorithm': ikepolicy['auth_algorithm'],
                'encryption_algorithm': ikepolicy['encryption_algorithm'],
                'ike_version': ikepolicy['ike_version'],
                'lifetime_units': ikepolicy['lifetime']['units'],
                'lifetime_value': ikepolicy['lifetime']['value'],
                'pfs': ikepolicy['pfs'],
                'phase1_negotiation_mode': ikepolicy[
                    'phase1_negotiation_mode']}


class UpdateIPsecPolicyView(horizon_forms.ModalFormView):
    form_class = forms.UpdateIPsecPolicy
    form_id = "update_ipsecpolicy_form"
    template_name = "project/vpn/update_ipsecpolicy.html"
    context_object_name = 'ipsecpolicy'
    submit_label = _("Save Changes")
    submit_url = "horizon:project:vpn:update_ipsecpolicy"
    success_url = reverse_lazy("horizon:project:vpn:index")
    page_title = _("Edit IPsec Policy")

    def get_context_data(self, **kwargs):
        context = super(UpdateIPsecPolicyView, self).get_context_data(**kwargs)
        context["ipsecpolicy_id"] = self.kwargs['ipsecpolicy_id']
        args = (self.kwargs['ipsecpolicy_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        ipsecpolicy_id = self.kwargs['ipsecpolicy_id']
        try:
            return api_vpn.ipsecpolicy_get(self.request, ipsecpolicy_id)
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve IPsec policy details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        ipsecpolicy = self._get_object()
        return {'name': ipsecpolicy['name'],
                'ipsecpolicy_id': ipsecpolicy['id'],
                'description': ipsecpolicy['description'],
                'auth_algorithm': ipsecpolicy['auth_algorithm'],
                'encapsulation_mode': ipsecpolicy['encapsulation_mode'],
                'encryption_algorithm': ipsecpolicy['encryption_algorithm'],
                'lifetime_units': ipsecpolicy['lifetime']['units'],
                'lifetime_value': ipsecpolicy['lifetime']['value'],
                'pfs': ipsecpolicy['pfs'],
                'transform_protocol': ipsecpolicy['transform_protocol']}


class UpdateIPsecSiteConnectionView(horizon_forms.ModalFormView):
    form_class = forms.UpdateIPsecSiteConnection
    form_id = "update_ipsecsiteconnection_form"
    template_name = "project/vpn/update_ipsecsiteconnection.html"
    context_object_name = 'ipsecsiteconnection'
    submit_label = _("Save Changes")
    submit_url = "horizon:project:vpn:update_ipsecsiteconnection"
    success_url = reverse_lazy("horizon:project:vpn:index")
    page_title = _("Edit IPsec Site Connection")

    def get_context_data(self, **kwargs):
        context = super(
            UpdateIPsecSiteConnectionView, self).get_context_data(**kwargs)
        context["ipsecsiteconnection_id"] = self.kwargs[
            'ipsecsiteconnection_id']
        args = (self.kwargs['ipsecsiteconnection_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def _get_object(self, *args, **kwargs):
        connection_id = self.kwargs['ipsecsiteconnection_id']
        try:
            return api_vpn.ipsecsiteconnection_get(self.request, connection_id)
        except Exception:
            redirect = self.success_url
            msg = _('Unable to retrieve IPsec site connection details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        ipsecsiteconnection = self._get_object()
        data = {
            'name': ipsecsiteconnection['name'],
            'ipsecsiteconnection_id': ipsecsiteconnection['id'],
            'description': ipsecsiteconnection['description'],
            'peer_address': ipsecsiteconnection['peer_address'],
            'peer_id': ipsecsiteconnection['peer_id'],
            'psk': ipsecsiteconnection['psk'],
            'mtu': ipsecsiteconnection['mtu'],
            'dpd_action': ipsecsiteconnection['dpd']['action'],
            'dpd_interval': ipsecsiteconnection['dpd']['interval'],
            'dpd_timeout': ipsecsiteconnection['dpd']['timeout'],
            'initiator': ipsecsiteconnection['initiator'],
            'admin_state_up': ipsecsiteconnection['admin_state_up']
        }
        if 'local_ep_group_id' in ipsecsiteconnection:
            data['local_ep_group_id'] = \
                ipsecsiteconnection['local_ep_group_id']
            data['peer_ep_group_id'] = ipsecsiteconnection['peer_ep_group_id']
            return data
        else:
            data['peer_cidrs'] = ", ".join(ipsecsiteconnection['peer_cidrs'])
            return data
