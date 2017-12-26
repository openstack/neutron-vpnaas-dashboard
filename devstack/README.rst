============================================
DevStack plugin for neutron-vpnaas-dashboard
============================================

This is setup as a DevStack plugin.
For more information on DevStack plugins,
see the `DevStack Plugins documentation
<https://docs.openstack.org/devstack/latest/plugins.html>`__.

How to enable VPNaaS dashboard
------------------------------

Add the following to the localrc section of your local.conf.
You need to configure VPNaaS DevStack plugin as well.
DevStack plugin for VPNaaS dashaboard is configured,
``neutron-vpnaas-dashboard`` service is automatically enabled.

It is suggested to enable the DevStack plugin for neutron-vpnaas,
if you run horizon and neutron-server on a same server like
all-in-one environment.

.. code-block:: none

   [[local|localrc]]
   enable_plugin neutron-vpnaas https://git.openstack.org/openstack/neutron-vpnaas master
   enable_plugin neutron-vpnaas-dashboard https://git.openstack.org/openstack/neutron-vpnaas-dashboard master
