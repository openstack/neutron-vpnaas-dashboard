# plugin.sh - DevStack plugin.sh dispatch script neutron-vpnaas-dashboard

VPNAAS_DASHBOARD_DIR=$(cd $(dirname $BASH_SOURCE)/.. && pwd)
VPNAAS_ENABLED_DIR=$VPNAAS_DASHBOARD_DIR/neutron_vpnaas_dashboard/enabled
HORIZON_ENABLED_DIR=$DEST/horizon/openstack_dashboard/local/enabled

function install_neutron_vpnaas_dashboard {
    setup_develop $VPNAAS_DASHBOARD_DIR
}

function configure_neutron_vpnaas_dashboard {
    cp -a $VPNAAS_ENABLED_DIR/_[0-9]*.py $HORIZON_ENABLED_DIR
    # NOTE: If locale directory does not exist, compilemessages will fail,
    # so check for an existence of locale directory is required.
    if [ -d $VPNAAS_DASHBOARD_DIR/neutron_vpnaas_dashboard/locale ]; then
        (cd $VPNAAS_DASHBOARD_DIR/neutron_vpnaas_dashboard; \
         DJANGO_SETTINGS_MODULE=openstack_dashboard.settings ../manage.py compilemessages)
    fi
}

# check for service enabled
if is_service_enabled neutron-vpnaas-dashboard; then

    if [[ "$1" == "stack" && "$2" == "pre-install"  ]]; then
        # Set up system services
        # no-op
        :

    elif [[ "$1" == "stack" && "$2" == "install"  ]]; then
        # Perform installation of service source
        echo_summary "Installing Neutron VPNaaS Dashboard"
        install_neutron_vpnaas_dashboard

    elif [[ "$1" == "stack" && "$2" == "post-config"  ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configurng Neutron VPNaaS Dashboard"
        configure_neutron_vpnaas_dashboard

    elif [[ "$1" == "stack" && "$2" == "extra"  ]]; then
        # no-op
        :
    fi

    if [[ "$1" == "unstack"  ]]; then
        # Remove enabled file(s)
        for _enabled_file in $VPNAAS_ENABLED_DIR/_[0-9]*.py; do
            _enabled_basename=$(basename $_enabled_file .py)
            rm -f $HORIZON_ENABLED_DIR/${_enabled_basename}.py*
            rm -f $HORIZON_ENABLED_DIR/__pycache__/${_enabled_basename}.*pyc
        done
    fi

    if [[ "$1" == "clean"  ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        :
    fi
fi
