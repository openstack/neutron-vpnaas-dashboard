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


from django import template
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django.utils.translation import pgettext_lazy

from horizon import exceptions
from horizon import tables

from openstack_dashboard import policy

from neutron_vpnaas_dashboard.api import vpn as api_vpn


forbid_updates = set(["PENDING_CREATE", "PENDING_UPDATE", "PENDING_DELETE"])


class AddIKEPolicyLink(tables.LinkAction):
    name = "addikepolicy"
    verbose_name = _("Add IKE Policy")
    url = "horizon:project:vpn:addikepolicy"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_ikepolicy"),)


class AddIPsecPolicyLink(tables.LinkAction):
    name = "addipsecpolicy"
    verbose_name = _("Add IPsec Policy")
    url = "horizon:project:vpn:addipsecpolicy"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_ipsecpolicy"),)


class AddVPNServiceLink(tables.LinkAction):
    name = "addvpnservice"
    verbose_name = _("Add VPN Service")
    url = "horizon:project:vpn:addvpnservice"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_vpnservice"),)


class AddEndpointGroupLink(tables.LinkAction):
    name = "addendpointgroup"
    verbose_name = _("Add Endpoint Group")
    url = "horizon:project:vpn:addendpointgroup"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_endpointgroup"),)


class AddIPsecSiteConnectionLink(tables.LinkAction):
    name = "addipsecsiteconnection"
    verbose_name = _("Add IPsec Site Connection")
    url = "horizon:project:vpn:addipsecsiteconnection"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_ipsec_site_connection"),)


class DeleteVPNServiceLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deletevpnservice"
    policy_rules = (("network", "delete_vpnservice"),)

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            u"Delete VPN Service",
            u"Delete VPN Services",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            u"Scheduled deletion of VPN service",
            u"Scheduled deletion of VPN services",
            count
        )

    def allowed(self, request, datum=None):
        if datum and datum.ipsecsiteconns:
            return False
        return True

    def delete(self, request, obj_id):
        try:
            api_vpn.vpnservice_delete(request, obj_id)
        except Exception:
            exceptions.handle(
                request, _('Unable to delete VPN service.'))


class DeleteEndpointGroupLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deleteendpointgroup"
    policy_rules = (("network", "delete_endpointgroup"),)

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            u"Delete Endpoint Group",
            u"Delete Endpoint Groups",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            u"Scheduled deletion of endpoint group",
            u"Scheduled deletion of endpoint groups",
            count
        )

    def delete(self, request, obj_id):
        try:
            api_vpn.endpointgroup_delete(request, obj_id)
        except Exception:
            exceptions.handle(
                request, _('Unable to delete endpoint group.'))


class DeleteIKEPolicyLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deleteikepolicy"
    policy_rules = (("network", "delete_ikepolicy"),)

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            u"Delete IKE Policy",
            u"Delete IKE Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            u"Scheduled deletion of IKE policy",
            u"Scheduled deletion of IKE policies",
            count
        )

    def allowed(self, request, datum=None):
        if datum and datum.ipsecsiteconns:
            return False
        return True

    def delete(self, request, obj_id):
        try:
            api_vpn.ikepolicy_delete(request, obj_id)
        except Exception:
            exceptions.handle(
                request, _('Unable to delete IKE policy.'))


class DeleteIPsecPolicyLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deleteipsecpolicy"
    policy_rules = (("network", "delete_ipsecpolicy"),)

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            u"Delete IPsec Policy",
            u"Delete IPsec Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            u"Scheduled deletion of IPsec policy",
            u"Scheduled deletion of IPsec policies",
            count
        )

    def allowed(self, request, datum=None):
        if datum and datum.ipsecsiteconns:
            return False
        return True

    def delete(self, request, obj_id):
        try:
            api_vpn.ipsecpolicy_delete(request, obj_id)
        except Exception:
            exceptions.handle(
                request, _('Unable to delete IPsec policy.'))


class DeleteIPsecSiteConnectionLink(policy.PolicyTargetMixin,
                                    tables.DeleteAction):
    name = "deleteipsecsiteconnection"
    policy_rules = (("network", "delete_ipsec_site_connection"),)

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            u"Delete IPsec Site Connection",
            u"Delete IPsec Site Connections",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            u"Scheduled deletion of IPsec site connection",
            u"Scheduled deletion of IPsec site connections",
            count
        )

    def delete(self, request, obj_id):
        try:
            api_vpn.ipsecsiteconnection_delete(request, obj_id)
        except Exception:
            exceptions.handle(request,
                              _('Unable to delete IPsec site connection.'))


class UpdateVPNServiceLink(tables.LinkAction):
    name = "update_vpnservice"
    verbose_name = _("Edit VPN Service")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_vpnservice"),)

    def get_link_url(self, vpnservice):
        return reverse("horizon:project:vpn:update_vpnservice",
                       kwargs={'vpnservice_id': vpnservice.id})

    def allowed(self, request, datum=None):
        if datum and datum.status not in forbid_updates:
            return True
        return False


class UpdateEndpointGroupLink(tables.LinkAction):
    name = "updateendpointgroup"
    verbose_name = _("Edit Endpoint Group")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_endpointgroup"),)

    def get_link_url(self, endpoint_group):
        return reverse("horizon:project:vpn:update_endpointgroup",
                       kwargs={'endpoint_group_id': endpoint_group.id})


class UpdateIKEPolicyLink(tables.LinkAction):
    name = "updateikepolicy"
    verbose_name = _("Edit IKE Policy")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_ikepolicy"),)

    def get_link_url(self, ikepolicy):
        return reverse("horizon:project:vpn:update_ikepolicy",
                       kwargs={'ikepolicy_id': ikepolicy.id})

    def allowed(self, request, datum=None):
        return not datum['ipsecsiteconns']


class UpdateIPsecPolicyLink(tables.LinkAction):
    name = "updateipsecpolicy"
    verbose_name = _("Edit IPsec Policy")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_ipsecpolicy"),)

    def get_link_url(self, ipsecpolicy):
        return reverse("horizon:project:vpn:update_ipsecpolicy",
                       kwargs={'ipsecpolicy_id': ipsecpolicy.id})

    def allowed(self, request, datum=None):
        return not datum['ipsecsiteconns']


class UpdateIPsecSiteConnectionLink(tables.LinkAction):
    name = "updateipsecsiteconnection"
    verbose_name = _("Edit Connection")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_ipsec_site_connection"),)

    def get_link_url(self, ipsecsiteconnection):
        return reverse("horizon:project:vpn:update_ipsecsiteconnection",
                       kwargs={'ipsecsiteconnection_id':
                               ipsecsiteconnection.id})

    def allowed(self, request, datum=None):
        if datum and datum.status not in forbid_updates:
            return True
        return False


STATUS_CHOICES = (
    ("active", True),
    ("down", True),
    ("created", True),
    ("error", False),
    ("inactive", False),
)


STATUS_DISPLAY_CHOICES = (
    ("active", pgettext_lazy("Current status of an IPsec site connection "
                             "and VPN service",
                             u"Active")),
    ("down", pgettext_lazy("Current status of an IPsec site connection "
                           "and VPN service",
                           u"Down")),
    ("error", pgettext_lazy("Current status of an IPsec site connection "
                            "and VPN service",
                            u"Error")),
    ("created", pgettext_lazy("Current status of an IPsec site connection "
                              "and VPN service",
                              u"Created")),
    ("pending_create", pgettext_lazy("Current status of an "
                                     "IPsec site connection and VPN service",
                                     u"Pending Create")),
    ("pending_update", pgettext_lazy("Current status of an "
                                     "IPsec site connection and VPN service",
                                     u"Pending Update")),
    ("pending_delete", pgettext_lazy("Current status of an "
                                     "IPsec site connection and VPN service",
                                     u"Pending Delete")),
    ("inactive", pgettext_lazy("Current status of an IPsec site connection "
                               "and VPN service",
                               u"Inactive")),
)


class UpdateIPsecSiteConnectionRow(tables.Row):
    ajax = True

    def get_data(self, request, conn_id):
        conn = api_vpn.ipsecsiteconnection_get(request, conn_id)
        conn.ikepolicy_name = conn['ikepolicy'].get('name',
                                                    conn['ikepolicy_id'])
        conn.ipsecpolicy_name = conn['ipsecpolicy'].get('name',
                                                        conn['ipsecpolicy_id'])
        conn.vpnservice_name = conn['vpnservice'].get('name',
                                                      conn['vpnservice_id'])
        return conn


class IPSSCFilterAction(tables.FilterAction):
    name = 'IPSSC_project_IKEPolicies'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('vpnservice', _("VPN Service ="), True),
        ('vpnservice_id', _("VPN Service ID ="), True),
        ('ikepolicy', _("IKE Policy ="), True),
        ('ikepolicy_id', _("IKE Policy ID ="), True),
        ('ipsecpolicy', _("IPsec Policy ="), True),
        ('ipsecpolicy_id', _("IPsec Policy ID ="), True),
        ('status', _("Status ="), True)
    )


class IPsecSiteConnectionsTable(tables.DataTable):
    name = tables.Column('name_or_id', verbose_name=_('Name'),
                         link="horizon:project:vpn:ipsecsiteconnectiondetails")
    description = tables.Column('description', verbose_name=_('Description'))
    vpnservice_name = tables.Column('vpnservice_name',
                                    verbose_name=_('VPN Service'))
    ikepolicy_name = tables.Column('ikepolicy_name',
                                   verbose_name=_('IKE Policy'))
    ipsecpolicy_name = tables.Column('ipsecpolicy_name',
                                     verbose_name=_('IPsec Policy'))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)

    def get_object_display(self, ipsecsiteconnection):
        return ipsecsiteconnection.name_or_id

    class Meta(object):
        name = "ipsecsiteconnectionstable"
        verbose_name = _("IPsec Site Connections")
        status_columns = ['status']
        row_class = UpdateIPsecSiteConnectionRow
        table_actions = (AddIPsecSiteConnectionLink,
                         DeleteIPsecSiteConnectionLink,
                         IPSSCFilterAction)
        row_actions = (UpdateIPsecSiteConnectionLink,
                       DeleteIPsecSiteConnectionLink)


def get_local_ips(vpn):
    template_name = 'project/vpn/_vpn_ips.html'
    context = {"external_v4_ip": vpn.get('external_v4_ip'),
               "external_v6_ip": vpn.get('external_v6_ip')}
    return template.loader.render_to_string(template_name, context)


def get_subnet_name(vpn):
    try:
        return vpn.subnet_name
    except AttributeError:
        return _("-")


class UpdateVPNServiceRow(tables.Row):
    ajax = True

    def get_data(self, request, vpn_id):
        vpn = api_vpn.vpnservice_get(request, vpn_id)
        vpn.router_name = vpn['router'].get('name', vpn['router_id'])
        if 'subnet' in vpn:
            vpn.subnet_name = vpn['subnet'].get('cidr', vpn['subnet_id'])
        return vpn


class VPNServicesFilterAction(tables.FilterAction):
    name = 'vpnservices_project_IKEPolicies'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('subnet_id', _("Subnet ID ="), True),
        ('subnet_name', _("Subnet ="), True),
        ('router_id', _("Router ID ="), True),
        ('router_name', _("Router ="), True),
    )


class VPNServicesTable(tables.DataTable):
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:vpnservicedetails")
    description = tables.Column('description', verbose_name=_('Description'))
    local_ips = tables.Column(get_local_ips,
                              verbose_name=_("Local Side Public IPs"))
    subnet_name = tables.Column(get_subnet_name, verbose_name=_('Subnet'))
    router_name = tables.Column('router_name', verbose_name=_('Router'))
    status = tables.Column("status",
                           verbose_name=_("Status"))

    def get_object_display(self, vpnservice):
        return vpnservice.name_or_id

    class Meta(object):
        name = "vpnservicestable"
        verbose_name = _("VPN Services")
        status_columns = ['status']
        row_class = UpdateVPNServiceRow
        table_actions = (AddVPNServiceLink,
                         DeleteVPNServiceLink,
                         VPNServicesFilterAction)
        row_actions = (UpdateVPNServiceLink, DeleteVPNServiceLink)


class EndpointGroupFilterAction(tables.FilterAction):
    name = 'endpointgroups_project'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('type', _("Type ="), True),
        ('endpoints', _("Endpoints ="), True),
    )


def _get_endpoints(epg):
    return ', '.join(epg.endpoints)


class EndpointGroupTable(tables.DataTable):
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:endpointgroupdetails")
    description = tables.Column('description', verbose_name=_('Description'))
    type = tables.Column('type', verbose_name=_('Type'))
    endpoints = tables.Column(_get_endpoints, verbose_name=_('Endpoints'))

    class Meta(object):
        name = "endpointgroupstable"
        verbose_name = _("Endpoint Groups")
        table_actions = (AddEndpointGroupLink,
                         DeleteEndpointGroupLink,
                         EndpointGroupFilterAction)
        row_actions = (UpdateEndpointGroupLink, DeleteEndpointGroupLink)

    def get_object_display(self, endpoitgroup):
        return endpoitgroup.name_or_id


class PoliciesFilterAction(tables.FilterAction):
    name = 'filter_project_IKEPolicies'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('auth_algorithm', _("Authorization algorithm ="), True),
        ('encryption_algorithm', _("Encryption algorithm ="), True),
        ('pfs', _("PFS ="), True),
    )


class IKEPoliciesTable(tables.DataTable):
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:ikepolicydetails")
    description = tables.Column('description', verbose_name=_('Description'))
    auth_algorithm = tables.Column('auth_algorithm',
                                   verbose_name=_('Authorization algorithm'))
    encryption_algorithm = tables.Column(
        'encryption_algorithm',
        verbose_name=_('Encryption algorithm'))
    pfs = tables.Column("pfs", verbose_name=_('PFS'))

    def get_object_display(self, ikepolicy):
        return ikepolicy.name_or_id

    class Meta(object):
        name = "ikepoliciestable"
        verbose_name = _("IKE Policies")
        table_actions = (AddIKEPolicyLink,
                         DeleteIKEPolicyLink,
                         PoliciesFilterAction)
        row_actions = (UpdateIKEPolicyLink, DeleteIKEPolicyLink)


class IPsecPoliciesTable(tables.DataTable):
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:ipsecpolicydetails")
    description = tables.Column('description', verbose_name=_('Description'))
    auth_algorithm = tables.Column('auth_algorithm',
                                   verbose_name=_('Authorization algorithm'))
    encryption_algorithm = tables.Column(
        'encryption_algorithm',
        verbose_name=_('Encryption algorithm'))
    pfs = tables.Column("pfs", verbose_name=_('PFS'))

    def get_object_display(self, ipsecpolicy):
        return ipsecpolicy.name_or_id

    class Meta(object):
        name = "ipsecpoliciestable"
        verbose_name = _("IPsec Policies")
        table_actions = (AddIPsecPolicyLink,
                         DeleteIPsecPolicyLink,
                         PoliciesFilterAction)
        row_actions = (UpdateIPsecPolicyLink, DeleteIPsecPolicyLink)
