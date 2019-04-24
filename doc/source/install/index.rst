..
      Copyright 2017 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

============
Installation
============

Manual Installation
-------------------

Before installing neutron-vpnaas-dashboard,
you first need to install horizon in your environment.

Fetch the source code from git and run pip install.
Make sure to install neutron-vpnaas-dashboard into the same python environment
where horizon is installed.

.. code-block:: console

   $ git clone https://opendev.org/openstack/neutron-vpnaas-dashboard
   $ cd neutron-vpnaas-dashboard
   $ sudo pip install .

Enable the horizon plugin.

.. code-block:: console

   $ cp neutron_vpnaas_dashboard/enabled/_7100_project_vpn_panel.py \
         /opt/stack/horizon/openstack_dashboard/local/enabled/_7100_project_vpn_panel.py

.. note::

   The directory ``local/enabled`` may be different depending on your
   environment or distribution used. For example, for Ubuntu, this is
   ``/usr/share/openstack-dashboard/openstack_dashboard/local/enabled``.

.. note::

   The number of the plugin enabled file determines the order of panels.
   If you would like to configure the place of the Neutron VPNaaS dashboard,
   change the number of the file.

.. note::

   For more detail of the horizon plugin settings,
   see `Pluggable Settings
   <https://docs.openstack.org/developer/horizon/install/settings.html#pluggable-settings>`__
   in the horizon documentation.

Compile the message catalogs of Neutron VPNaaS dashboard.

.. code-block:: console

   $ cd neutron-vpnaas-dashboard
   $ ./manage.py compilemessages

Run the Django update commands (if you use).

.. code-block:: console

   $ DJANGO_SETTINGS_MODULE=openstack_dashboard.settings python manage.py collectstatic --noinput
   $ DJANGO_SETTINGS_MODULE=openstack_dashboard.settings python manage.py compress --force

Restart Apache:

.. code-block:: console

   $ sudo service apache2 restart
