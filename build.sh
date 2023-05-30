#!/usr/bin/env bash

# echo $ENV

# Capture the first argument as the testbed name
TESTBED_NAME=$1

# Remove the first argument
shift

# Capture all remaining arguments as ansible arguments
# like --tags (-t), --skip-tags, --vvvv (-vvvv)
ANSIBLE_ARGS="$@"

source testbeds/$TESTBED_NAME/.env

ENV="--env VIRL_HOST=${virl_host} \
--env VIRL_USERNAME=${virl_username} \
--env VIRL_PASSWORD=${virl_password} \
--env VCENTER_HOST=${vcenter_host} \
--env VCENTER_USERNAME=${vcenter_username} \
--env VCENTER_PASSWORD=${vcenter_password} \
--env NODE_USERNAME=${node_username} \
--env NODE_PASSWORD=${node_password} \
--env NODE_ENABLE=${node_enable} \
--env JUMPSERVER_HOST=${jumpserver_host} \
--env JUMPSERVER_INFRA_HOST=${jumpserver_infra_host} \
--env JUMPSERVER_USERNAME=${jumpserver_username} \
--env JUMPSERVER_CFG_PATH=${jumpserver_cfg_path} \
--env JUMPSERVER_PASSWORD=${jumpserver_password} \
--env OOB_SWITCH=${oob_switch}"



docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env ANSIBLE_ROLES_PATH=/ansible/roles \
$ENV auto-vsda ansible-playbook $ANSIBLE_ARGS -i testbeds/$TESTBED_NAME/inventory testbeds/$TESTBED_NAME/$TESTBED_NAME.yml