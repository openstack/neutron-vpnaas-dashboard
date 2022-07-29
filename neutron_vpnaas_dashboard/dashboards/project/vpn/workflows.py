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
from horizon import forms
from horizon import workflows

from openstack_dashboard import api

from neutron_vpnaas_dashboard.api import vpn as api_vpn


class AddVPNServiceAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"), required=False)
    description = forms.CharField(
        initial="", required=False,
        max_length=80, label=_("Description"))
    router_id = forms.ThemableChoiceField(label=_("Router"))
    subnet_id = forms.ThemableChoiceField(
        label=_("Subnet"),
        help_text=_("Optional. No need to be specified "
                    "when you use endpoint groups."),
        required=False)
    admin_state_up = forms.BooleanField(
        label=_("Enable Admin State"),
        help_text=_("The state of VPN service to start in. If disabled "
                    "(not checked), VPN service does not forward packets."),
        initial=True,
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddVPNServiceAction, self).__init__(request, *args, **kwargs)

    def populate_subnet_id_choices(self, request, context):
        subnet_id_choices = [('', _("Select a Subnet"))]
        try:
            tenant_id = request.user.tenant_id
            networks = api.neutron.network_list_for_tenant(request, tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve networks list.'))
            networks = []
        for n in networks:
            for s in n['subnets']:
                subnet_id_choices.append((s.id, s.cidr))
        self.fields['subnet_id'].choices = subnet_id_choices
        return subnet_id_choices

    def populate_router_id_choices(self, request, context):
        router_id_choices = [('', _("Select a Router"))]
        try:
            tenant_id = request.user.tenant_id
            routers = api.neutron.router_list(request, tenant_id=tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve routers list.'))
            routers = []
        for r in routers:
            if not r.external_gateway_info:
                continue
            router_id_choices.append((r.id, r.name))
        self.fields['router_id'].choices = router_id_choices
        return router_id_choices

    class Meta(object):
        name = _("Add New VPN Service")
        permissions = ('openstack.services.network',)
        help_text_template = "project/vpn/_add_vpn_service_help.html"


class AddVPNServiceStep(workflows.Step):
    action_class = AddVPNServiceAction
    contributes = ("name", "description", "subnet_id",
                   "router_id", "admin_state_up")

    def contribute(self, data, context):
        context = super(AddVPNServiceStep, self).contribute(data, context)
        if data:
            return context


class AddVPNService(workflows.Workflow):
    slug = "addvpnservice"
    name = _("Add VPN Service")
    finalize_button_name = _("Add")
    success_message = _('Added VPN service "%s".')
    failure_message = _('Unable to add VPN service "%s".')
    success_url = "horizon:project:vpn:index"
    default_steps = (AddVPNServiceStep,)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def handle(self, request, context):
        try:
            api_vpn.vpnservice_create(request, **context)
            return True
        except Exception:
            return False


class AddEndpointGroupAction(workflows.Action):
    name = forms.CharField(
        max_length=80,
        label=_("Name"),
        required=False)
    description = forms.CharField(
        initial="",
        required=False,
        max_length=80,
        label=_("Description"))
    type = forms.ThemableChoiceField(
        label=_("Type"),
        help_text=_("IPsec connection validation requires that local "
                    "endpoints are subnets, and peer endpoints are CIDRs."),
        choices=[('cidr', _('CIDR (for external systems)')),
                 ('subnet', _('Subnet (for local systems)'))],
        widget=forms.ThemableSelectWidget(attrs={
            'class': 'switchable',
            'data-slug': 'type', }))
    cidrs = forms.MultiIPField(
        required=False,
        label=_("External System CIDRs"),
        widget=forms.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'type',
            'data-type-cidr': _("External System CIDRs"),
        }),
        help_text=_("Remote peer subnet(s) address(es) "
                    "with mask(s) in CIDR format "
                    "separated with commas if needed "
                    "(e.g. 20.1.0.0/24, 21.1.0.0/24). "
                    "This field is valid if type is CIDR"),
        version=forms.IPv4 | forms.IPv6,
        mask=True)
    subnets = forms.MultipleChoiceField(
        required=False,
        label=_("Local System Subnets"),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'switched',
            'data-switch-on': 'type',
            'data-type-subnet': _("External System Subnets"),
        }),
        help_text=_("Local subnet(s). "
                    "This field is valid if type is Subnet"),)

    def populate_subnets_choices(self, request, context):
        subnets_choices = []
        try:
            tenant_id = request.user.tenant_id
            networks = api.neutron.network_list_for_tenant(request, tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve networks list.'))
            networks = []
        for n in networks:
            for s in n['subnets']:
                subnets_choices.append((s.id, s.cidr))
        self.fields['subnets'].choices = subnets_choices
        return subnets_choices

    class Meta(object):
        name = _("Add New Endpoint Groups")
        permissions = ('openstack.services.network',)
        help_text_template = "project/vpn/_add_endpoint_group_help.html"


class AddEndpointGroupStep(workflows.Step):
    action_class = AddEndpointGroupAction
    contributes = ("name", "description", "type",
                   "cidrs", "subnets", "endpoints")

    def contribute(self, data, context):
        context = super(AddEndpointGroupStep, self).contribute(data, context)
        if context['type'] == 'cidr':
            cidrs = context['cidrs']
            context['endpoints'] = [
                cidr.strip() for cidr in cidrs.split(',') if cidr.strip()]
        else:
            context['endpoints'] = context['subnets']
        if data:
            return context


class AddEndpointGroup(workflows.Workflow):
    slug = "addendpointgroup"
    name = _("Add Endpoint Group")
    finalize_button_name = _("Add")
    success_message = _('Added endpoint group "%s".')
    failure_message = _('Unable to add endpoint group "%s".')
    success_url = "horizon:project:vpn:index"
    default_steps = (AddEndpointGroupStep,)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def handle(self, request, context):
        try:
            api_vpn.endpointgroup_create(request,
                                         name=context['name'],
                                         description=context['description'],
                                         type=context['type'],
                                         endpoints=context['endpoints'])
            return True
        except Exception:
            return False


class AddIKEPolicyAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"), required=False)
    description = forms.CharField(
        initial="", required=False,
        max_length=80, label=_("Description"))
    auth_algorithm = forms.ThemableChoiceField(
        label=_("Authorization algorithm"),
        required=False)
    encryption_algorithm = forms.ThemableChoiceField(
        label=_("Encryption algorithm"),
        required=False)
    ike_version = forms.ThemableChoiceField(
        label=_("IKE version"),
        required=False)
    lifetime_units = forms.ThemableChoiceField(
        label=_("Lifetime units for IKE keys"),
        required=False)
    lifetime_value = forms.IntegerField(
        min_value=60, label=_("Lifetime value for IKE keys"),
        initial=3600,
        help_text=_("Equal to or greater than 60"),
        required=False)
    pfs = forms.ThemableChoiceField(
        label=_("Perfect Forward Secrecy"), required=False)
    phase1_negotiation_mode = forms.ThemableChoiceField(
        label=_("IKE Phase1 negotiation mode"), required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddIKEPolicyAction, self).__init__(request, *args, **kwargs)

        auth_algorithm_choices = [
            ("sha1", "sha1"),
            ('sha256', _('sha256')),
            ('sha384', _('sha384')),
            ('sha512', _('sha512')),
        ]
        self.fields['auth_algorithm'].choices = auth_algorithm_choices
        # Currently this field has only one choice, so mark it as readonly.
        self.fields['auth_algorithm'].widget.attrs['readonly'] = True

        encryption_algorithm_choices = [("3des", "3des"),
                                        ("aes-128", "aes-128"),
                                        ("aes-192", "aes-192"),
                                        ("aes-256", "aes-256")]
        self.fields[
            'encryption_algorithm'].choices = encryption_algorithm_choices
        self.fields['encryption_algorithm'].initial = "aes-128"

        ike_version_choices = [("v1", "v1"),
                               ("v2", "v2")]
        self.fields['ike_version'].choices = ike_version_choices

        lifetime_units_choices = [("seconds", "seconds")]
        self.fields['lifetime_units'].choices = lifetime_units_choices
        # Currently this field has only one choice, so mark it as readonly.
        self.fields['lifetime_units'].widget.attrs['readonly'] = True

        pfs_choices = [("group2", "group2"),
                       ("group5", "group5"),
                       ("group14", "group14")]
        self.fields['pfs'].choices = pfs_choices
        self.fields['pfs'].initial = "group5"

        phase1_neg_mode_choices = [("main", "main"),
                                   ("aggressive", "aggressive")]
        self.fields[
            'phase1_negotiation_mode'].choices = phase1_neg_mode_choices

    class Meta(object):
        name = _("Add New IKE Policy")
        permissions = ('openstack.services.network',)
        help_text_template = "project/vpn/_add_ike_policy_help.html"


class AddIKEPolicyStep(workflows.Step):
    action_class = AddIKEPolicyAction
    contributes = ("name", "description", "auth_algorithm",
                   "encryption_algorithm", "ike_version",
                   "lifetime_units", "lifetime_value",
                   "pfs", "phase1_negotiation_mode")

    def contribute(self, data, context):
        context = super(AddIKEPolicyStep, self).contribute(data, context)
        context['lifetime'] = {'units': data['lifetime_units'],
                               'value': data['lifetime_value']}
        context.pop('lifetime_units')
        context.pop('lifetime_value')
        if data:
            return context


class AddIKEPolicy(workflows.Workflow):
    slug = "addikepolicy"
    name = _("Add IKE Policy")
    finalize_button_name = _("Add")
    success_message = _('Added IKE policy "%s".')
    failure_message = _('Unable to add IKE policy "%s".')
    success_url = "horizon:project:vpn:index"
    default_steps = (AddIKEPolicyStep,)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def handle(self, request, context):
        try:
            api_vpn.ikepolicy_create(request, **context)
            return True
        except Exception:
            return False


class AddIPsecPolicyAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"), required=False)
    description = forms.CharField(
        initial="", required=False,
        max_length=80, label=_("Description"))
    auth_algorithm = forms.ThemableChoiceField(
        label=_("Authorization algorithm"), required=False)
    encapsulation_mode = forms.ThemableChoiceField(
        label=_("Encapsulation mode"), required=False)
    encryption_algorithm = forms.ThemableChoiceField(
        label=_("Encryption algorithm"), required=False)
    lifetime_units = forms.ThemableChoiceField(
        label=_("Lifetime units"), required=False)
    lifetime_value = forms.IntegerField(
        min_value=60, label=_("Lifetime value for IKE keys "),
        initial=3600,
        help_text=_("Equal to or greater than 60"),
        required=False)
    pfs = forms.ThemableChoiceField(
        label=_("Perfect Forward Secrecy"), required=False)
    transform_protocol = forms.ThemableChoiceField(
        label=_("Transform Protocol"), required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddIPsecPolicyAction, self).__init__(request, *args, **kwargs)

        auth_algorithm_choices = [
            ("sha1", "sha1"),
            ('sha256', _('sha256')),
            ('sha384', _('sha384')),
            ('sha512', _('sha512')),
        ]
        self.fields['auth_algorithm'].choices = auth_algorithm_choices
        # Currently this field has only one choice, so mark it as readonly.
        self.fields['auth_algorithm'].widget.attrs['readonly'] = True

        encapsulation_mode_choices = [("tunnel", "tunnel"),
                                      ("transport", "transport")]
        self.fields['encapsulation_mode'].choices = encapsulation_mode_choices

        encryption_algorithm_choices = [("3des", "3des"),
                                        ("aes-128", "aes-128"),
                                        ("aes-192", "aes-192"),
                                        ("aes-256", "aes-256")]
        self.fields[
            'encryption_algorithm'].choices = encryption_algorithm_choices
        self.fields['encryption_algorithm'].initial = "aes-128"

        lifetime_units_choices = [("seconds", "seconds")]
        self.fields['lifetime_units'].choices = lifetime_units_choices
        # Currently this field has only one choice, so mark it as readonly.
        self.fields['lifetime_units'].widget.attrs['readonly'] = True

        pfs_choices = [("group2", "group2"),
                       ("group5", "group5"),
                       ("group14", "group14")]
        self.fields['pfs'].choices = pfs_choices
        self.fields['pfs'].initial = "group5"

        transform_protocol_choices = [("esp", "esp"),
                                      ("ah", "ah"),
                                      ("ah-esp", "ah-esp")]
        self.fields['transform_protocol'].choices = transform_protocol_choices

    class Meta(object):
        name = _("Add New IPsec Policy")
        permissions = ('openstack.services.network',)
        help_text_template = 'project/vpn/_add_ipsec_policy_help.html'


class AddIPsecPolicyStep(workflows.Step):
    action_class = AddIPsecPolicyAction
    contributes = ("name", "description", "auth_algorithm",
                   "encapsulation_mode", "encryption_algorithm",
                   "lifetime_units", "lifetime_value",
                   "pfs", "transform_protocol")

    def contribute(self, data, context):
        context = super(AddIPsecPolicyStep, self).contribute(data, context)
        context['lifetime'] = {'units': data['lifetime_units'],
                               'value': data['lifetime_value']}
        context.pop('lifetime_units')
        context.pop('lifetime_value')
        if data:
            return context


class AddIPsecPolicy(workflows.Workflow):
    slug = "addipsecpolicy"
    name = _("Add IPsec Policy")
    finalize_button_name = _("Add")
    success_message = _('Added IPsec policy "%s".')
    failure_message = _('Unable to add IPsec policy "%s".')
    success_url = "horizon:project:vpn:index"
    default_steps = (AddIPsecPolicyStep,)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def handle(self, request, context):
        try:
            api_vpn.ipsecpolicy_create(request, **context)
            return True
        except Exception:
            return False


class AddIPsecSiteConnectionAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Name"), required=False)
    description = forms.CharField(
        initial="", required=False,
        max_length=80, label=_("Description"))
    vpnservice_id = forms.ThemableChoiceField(
        label=_("VPN service associated with this connection"))
    local_ep_group_id = forms.ThemableChoiceField(
        required=False,
        label=_("Endpoint group for local subnet(s)"),
        help_text=_("Local subnets which the new IPsec connection is "
                    "connected to. Required if no subnet is specified "
                    "in a VPN service selected."))
    ikepolicy_id = forms.ThemableChoiceField(
        label=_("IKE policy associated with this connection"))
    ipsecpolicy_id = forms.ThemableChoiceField(
        label=_("IPsec policy associated with this connection"))
    peer_address = forms.CharField(
        label=_("Peer gateway public IPv4/IPv6 Address or FQDN"),
        help_text=_("Peer gateway public IPv4/IPv6 address or FQDN for "
                    "the VPN Connection"),)
    peer_id = forms.CharField(
        label=_("Peer router identity for authentication (Peer ID)"),
        help_text=_("Peer router identity for authentication. "
                    "Can be IPv4/IPv6 address, e-mail, key ID, or FQDN"),)
    peer_ep_group_id = forms.ThemableChoiceField(
        required=False,
        label=_("Endpoint group for remote peer CIDR(s)"),
        help_text=_("Remote peer CIDR(s) connected to the new IPsec "
                    "connection."))
    peer_cidrs = forms.MultiIPField(
        required=False,
        label=_("Remote peer subnet(s)"),
        help_text=_("(Deprecated) Remote peer subnet(s) address(es) "
                    "with mask(s) in CIDR format "
                    "separated with commas if needed "
                    "(e.g. 20.1.0.0/24, 21.1.0.0/24)"),
        version=forms.IPv4 | forms.IPv6,
        mask=True)
    psk = forms.CharField(
        max_length=80,
        label=_("Pre-Shared Key (PSK) string"),
        widget=forms.PasswordInput(render_value=False),
        help_text=_("The pre-defined key string "
                    "between the two peers of the VPN connection"))

    def populate_ikepolicy_id_choices(self, request, context):
        ikepolicy_id_choices = [('', _("Select IKE policy"))]
        try:
            tenant_id = self.request.user.tenant_id
            ikepolicies = api_vpn.ikepolicy_list(request, tenant_id=tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve IKE policies list.'))
            ikepolicies = []
        for p in ikepolicies:
            ikepolicy_id_choices.append((p.id, p.name_or_id))
        self.fields['ikepolicy_id'].choices = ikepolicy_id_choices
        return ikepolicy_id_choices

    def populate_ipsecpolicy_id_choices(self, request, context):
        ipsecpolicy_id_choices = [('', _("Select IPsec Policy"))]
        try:
            tenant_id = self.request.user.tenant_id
            ipsecpolicies = api_vpn.ipsecpolicy_list(request,
                                                     tenant_id=tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve IPsec policies list.'))
            ipsecpolicies = []
        for p in ipsecpolicies:
            ipsecpolicy_id_choices.append((p.id, p.name_or_id))
        self.fields['ipsecpolicy_id'].choices = ipsecpolicy_id_choices
        return ipsecpolicy_id_choices

    def populate_vpnservice_id_choices(self, request, context):
        vpnservice_id_choices = [('', _("Select VPN service"))]
        try:
            tenant_id = self.request.user.tenant_id
            vpnservices = api_vpn.vpnservice_list(request, tenant_id=tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve VPN services list.'))
            vpnservices = []
        for s in vpnservices:
            vpnservice_id_choices.append((s.id, s.name_or_id))
        self.fields['vpnservice_id'].choices = vpnservice_id_choices
        return vpnservice_id_choices

    def populate_local_ep_group_id_choices(self, request, context):
        try:
            tenant_id = self.request.user.tenant_id
            endpointgroups = api_vpn.endpointgroup_list(request,
                                                        tenant_id=tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve endpoint group list.'))
            endpointgroups = []
        local_ep_group_ids = [(ep.id, ep.name_or_id) for ep in endpointgroups
                              if ep.type == 'subnet']
        local_ep_group_ids.insert(0, ('', _("Select local endpoint group")))
        self.fields['local_ep_group_id'].choices = local_ep_group_ids
        return local_ep_group_ids

    def populate_peer_ep_group_id_choices(self, request, context):
        try:
            tenant_id = self.request.user.tenant_id
            endpointgroups = api_vpn.endpointgroup_list(request,
                                                        tenant_id=tenant_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve endpoint group list.'))
            endpointgroups = []
        peer_ep_group_ids = [(ep.id, ep.name_or_id)
                             for ep in endpointgroups if ep.type == 'cidr']
        peer_ep_group_ids.insert(0, ('', _("Select peer endpoint group")))
        self.fields['peer_ep_group_id'].choices = peer_ep_group_ids
        return peer_ep_group_ids

    class Meta(object):
        name = _("Add New IPsec Site Connection")
        permissions = ('openstack.services.network',)
        help_text = _("Create IPsec site connection for current "
                      "project. Assign a name and description for the "
                      "IPsec site connection. "
                      "All fields in this tab are required."
                      )


class AddIPsecSiteConnectionStep(workflows.Step):
    action_class = AddIPsecSiteConnectionAction
    contributes = ("name", "description",
                   "vpnservice_id", "ikepolicy_id", "ipsecpolicy_id",
                   "peer_address", "peer_id", "peer_cidrs", "psk",
                   "local_ep_group_id", "peer_ep_group_id")


class AddIPsecSiteConnectionOptionalAction(workflows.Action):
    mtu = forms.IntegerField(
        min_value=68,
        label=_("Maximum Transmission Unit size for the connection"),
        initial=1500,
        required=False,
        help_text=_("Equal to or greater than 68 if the local subnet is IPv4. "
                    "Equal to or greater than 1280 if the local subnet "
                    "is IPv6."))
    dpd_action = forms.ThemableChoiceField(
        label=_("Dead peer detection actions"),
        required=False)
    dpd_interval = forms.IntegerField(
        min_value=1, label=_("Dead peer detection interval"),
        initial=30,
        required=False,
        help_text=_("Valid integer lesser than DPD timeout"))
    dpd_timeout = forms.IntegerField(
        min_value=1, label=_("Dead peer detection timeout"),
        initial=120,
        required=False,
        help_text=_("Valid integer greater than the DPD interval"))
    initiator = forms.ThemableChoiceField(
        label=_("Initiator state"), required=False)
    admin_state_up = forms.BooleanField(
        label=_("Enable Admin State"),
        help_text=_("The state of IPsec site connection to start in. "
                    "If disabled (not checked), IPsec site connection "
                    "does not forward packets."),
        initial=True,
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(AddIPsecSiteConnectionOptionalAction, self).__init__(
            request, *args, **kwargs)

        initiator_choices = [("bi-directional", "bi-directional"),
                             ("response-only", "response-only")]
        self.fields['initiator'].choices = initiator_choices

    def populate_dpd_action_choices(self, request, context):
        dpd_action_choices = [("hold", "hold"),
                              ("clear", "clear"),
                              ("disabled", "disabled"),
                              ("restart", "restart"),
                              ("restart-by-peer", "restart-by-peer")]
        self.fields['dpd_action'].choices = dpd_action_choices
        return dpd_action_choices

    def clean(self):
        cleaned_data = super(AddIPsecSiteConnectionOptionalAction,
                             self).clean()
        interval = cleaned_data.get('dpd_interval')
        timeout = cleaned_data.get('dpd_timeout')

        if not interval < timeout:
            msg = _("DPD Timeout must be greater than DPD Interval")
            self._errors['dpd_timeout'] = self.error_class([msg])
        return cleaned_data

    class Meta(object):
        name = _("Optional Parameters")
        permissions = ('openstack.services.network',)
        help_text = _("Fields in this tab are optional. "
                      "You can configure the detail of "
                      "IPsec site connection created."
                      )


class AddIPsecSiteConnectionOptionalStep(workflows.Step):
    action_class = AddIPsecSiteConnectionOptionalAction
    contributes = ("dpd_action", "dpd_interval", "dpd_timeout",
                   "initiator", "mtu", "admin_state_up")

    def contribute(self, data, context):
        context = super(
            AddIPsecSiteConnectionOptionalStep, self).contribute(data, context)
        context['dpd'] = {'action': data['dpd_action'],
                          'interval': data['dpd_interval'],
                          'timeout': data['dpd_timeout']}
        context.pop('dpd_action')
        context.pop('dpd_interval')
        context.pop('dpd_timeout')

        cidrs = context['peer_cidrs']
        context['peer_cidrs'] = [cidr.strip() for cidr in cidrs.split(',')
                                 if cidr.strip()]

        if data:
            return context


class AddIPsecSiteConnection(workflows.Workflow):
    slug = "addipsecsiteconnection"
    name = _("Add IPsec Site Connection")
    finalize_button_name = _("Add")
    success_message = _('Added IPsec site connection "%s".')
    failure_message = _('Unable to add IPsec site connection "%s".')
    success_url = "horizon:project:vpn:index"
    default_steps = (AddIPsecSiteConnectionStep,
                     AddIPsecSiteConnectionOptionalStep)

    def format_status_message(self, message):
        return message % self.context.get('name')

    def handle(self, request, context):
        try:
            api_vpn.ipsecsiteconnection_create(request, **context)
            return True
        except Exception:
            return False
