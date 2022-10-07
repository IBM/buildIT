# @file tables.py
#
# Copyright IBM Corporation 2022
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Headers Table

headers = {
   'data': 'data "%s" "%s" {',
   'module': 'module "%s" {',
   'output': 'output "%s" {',
   'provider': 'provider "%s" {',
   'resource': 'resource "%s" "%s" {',
   'terraform': 'terraform {',
   'variable': 'variable "%s" {'
}

# Footers Table

footers = {
   'data': '}',
   'module': '}',
   'output': '}',
   'provider': '}',
   'resource': '}',
   'terraform': '}',
   'variable': '}'
}

# Resources Table

# Translate sheet names to resource names.
# Resource names are not used as sheet names due to sheet name limit.

resources = {
   'aclheaders': 'ibm_is_network_acl',
   'aclrules': 'ibm_is_network_acl',
   'cisdomains': 'ibm_cis_domain',
   'cisglbs': 'ibm_cis_global_load_balancer',
   'cishealthchecks': 'ibm_cis_healthcheck',
   'cisinstances': 'ibm_cis',
   'cisoriginpools': 'ibm_cis_origin_pool',
   'floatingips': 'ibm_is_floating_ip',
   'flowlogs': 'ibm_is_flow_log',
   'ikepolicies': 'ibm_is_ike_policy',
   'images': 'ibm_is_image',
   'instances': 'ibm_is_instance',
   'instancegroups': 'ibm_is_instance_group',
   'instancemanagers': 'ibm_is_instance_group_manager',
   'instancepolicies': 'ibm_is_instance_group_manager_policy',
   'instancetemplates': 'ibm_is_instance_template',
   'ipsecpolicies': 'ibm_is_ipsec_policy',
   'loadbalancers': 'ibm_is_lb',
   'lblisteners': 'ibm_is_lb_listener',
   'lbmembers': 'ibm_is_lb_pool_member',
   'lbpolicies': 'ibm_is_lb_listener_policy',
   'lbpools': 'ibm_is_lb_pool',
   'lbrules': 'ibm_is_lb_listener_policy_rule',
   'networkinterfaces': 'ibm_is_instance_nic',
   'publicgateways': 'ibm_is_public_gateway',
   'resourcegroups': 'ibm_resource_group',
   'sgheaders': 'ibm_is_security_group',
   'sgnics': 'ibm_is_security_group_network_interface_attachment',
   'sgrules': 'ibm_is_security_group_rule',
   'sshkeys': 'ibm_is_ssh_key',
   'subnets': 'ibm_is_subnet',
   'transitconnections': 'ibm_tg_connection',
   'transitgateways': 'ibm_tg_gateway',
   'volumes': 'ibm_is_volume',
   'vpcaddresses': 'ibm_is_vpc_address_prefix',
   'vpcroutes': 'ibm_is_vpc_route',
   'vpcs': 'ibm_is_vpc',
   'vpnconnections': 'ibm_is_vpn_gateway_connection',
   'vpngateways': 'ibm_is_vpn_gateway',
   'localfiles': 'local_file' 
}
