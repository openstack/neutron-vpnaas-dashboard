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

from django.urls import re_path

from neutron_vpnaas_dashboard.dashboards.project.vpn import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^addikepolicy$',
            views.AddIKEPolicyView.as_view(), name='addikepolicy'),
    re_path(r'^update_ikepolicy/(?P<ikepolicy_id>[^/]+)/$',
            views.UpdateIKEPolicyView.as_view(), name='update_ikepolicy'),
    re_path(r'^addipsecpolicy$',
            views.AddIPsecPolicyView.as_view(), name='addipsecpolicy'),
    re_path(r'^update_ipsecpolicy/(?P<ipsecpolicy_id>[^/]+)/$',
            views.UpdateIPsecPolicyView.as_view(), name='update_ipsecpolicy'),
    re_path(r'^addipsecsiteconnection$',
            views.AddIPsecSiteConnectionView.as_view(),
            name='addipsecsiteconnection'),
    re_path(r'^update_ipsecsiteconnection/(?P<ipsecsiteconnection_id>[^/]+)/$',
            views.UpdateIPsecSiteConnectionView.as_view(),
            name='update_ipsecsiteconnection'),
    re_path(r'^addvpnservice$',
            views.AddVPNServiceView.as_view(), name='addvpnservice'),
    re_path(r'^update_vpnservice/(?P<vpnservice_id>[^/]+)/$',
            views.UpdateVPNServiceView.as_view(), name='update_vpnservice'),
    re_path(r'^addendpointgroup$',
            views.AddEndpointGroupView.as_view(), name='addendpointgroup'),
    re_path(r'^update_endpointgroup/(?P<endpoint_group_id>[^/]+)/$',
            views.UpdateEndpointGroupView.as_view(),
            name='update_endpointgroup'),
    re_path(r'^ikepolicy/(?P<ikepolicy_id>[^/]+)/$',
            views.IKEPolicyDetailsView.as_view(), name='ikepolicydetails'),
    re_path(r'^ipsecpolicy/(?P<ipsecpolicy_id>[^/]+)/$',
            views.IPsecPolicyDetailsView.as_view(), name='ipsecpolicydetails'),
    re_path(r'^vpnservice/(?P<vpnservice_id>[^/]+)/$',
            views.VPNServiceDetailsView.as_view(), name='vpnservicedetails'),
    re_path(r'^endpointgroup/(?P<endpoint_group_id>[^/]+)/$',
            views.EndpointGroupDetailsView.as_view(),
            name='endpointgroupdetails'),
    re_path(r'^ipsecsiteconnection/(?P<ipsecsiteconnection_id>[^/]+)/$',
            views.IPsecSiteConnectionDetailsView.as_view(),
            name='ipsecsiteconnectiondetails'),
]
