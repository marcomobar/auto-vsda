import pexpect
import sys
import time
import os

virl_host = os.environ.get('VIRL_HOST')
virl_username = os.environ.get('VIRL_USERNAME')
virl_password = os.environ.get('VIRL_PASSWORD')
node_username = os.environ.get('NODE_USERNAME')
node_password = os.environ.get('NODE_PASSWORD')
node_enable = os.environ.get('NODE_ENABLE')

virl_lab = sys.argv[1]
node_name = sys.argv[2]
management_ip = sys.argv[3]
management_mask = sys.argv[4]
management_gateway = sys.argv[5]
domain = sys.argv[6]

# jumpserver_username = sys.argv[7]
# jumpserver_password = sys.argv[8]
jumpserver_host = sys.argv[7]
# jumpserver_cfg_path = sys.argv[10]


node_path = "/" + virl_lab + "/" + node_name + "/0"



child = pexpect.spawn('ssh -o "StrictHostKeyChecking no" %s@%s' % (virl_username, virl_host))
child.logfile = sys.stdout.buffer
child.timeout = 1800  # 30mins
child.expect('password:')
child.sendline(virl_password)
child.expect('>')
# time.sleep(30)  # wait for node to be available
child.sendline('open %s' % node_path)
child.send("\r")
child.expect('yes/no]')
# child.expect('v4 on GigabitEthernet0/0,Vlan1')
child.sendline('no')
child.expect('enable secret:')
child.sendline(node_enable)
child.expect('enable secret:')
child.sendline(node_enable)
child.send("\r")
child.send("\r")
child.expect('>')
child.sendline('enable')
child.expect('Password:')
child.sendline(node_enable)

'''
Configuration
'''

child.expect('#')
child.sendline('conf t')
child.expect('\(config\)#')

# shutdown all ports
child.sendline('interface range g1/0/1 - 8')
child.expect('\(config-if-range\)#')
child.sendline('shutdown')
child.sendline('exit')

# child.expect('\(config\)#')
# child.sendline('hostname %s' % (node_name))
# child.expect('\(config\)#')
# child.sendline('username %s privilege 15 password %s' % (node_username, node_password))
# child.expect('\(config\)#')
# child.sendline('enable secret %s' % (node_enable))
child.expect('\(config\)#')
child.sendline('license boot level network-advantage addon dna-advantage')
child.expect('\(config\)#')
child.sendline('ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 %s' % (management_gateway))
child.expect('\(config\)#')
child.sendline('ip domain name %s' % (domain))
child.expect('\(config\)#')
child.sendline('crypto key generate rsa modulus 2048')
child.send('\r')
child.expect('\(config\)#')
child.sendline('ip ssh version 2')
child.expect('\(config\)#')
child.sendline('ip tftp source-interface GigabitEthernet 0/0')
child.expect('\(config\)#')
# child.sendline('ip ssh source-interface GigabitEthernet 0/0')
# child.expect('\(config\)#')
# child.sendline('line vty 0 15')
# child.sendline('login local')
# child.sendline('exit')
child.sendline('interface GigabitEthernet0/0')
child.expect('\(config-if\)#')
child.sendline('ip address %s %s' % (management_ip, management_mask))
child.sendline('no shutdown')
child.sendline('exit')
child.expect('\(config\)#')
child.sendline('end')
child.expect('#')
child.sendline('wr mem')
child.expect('[OK]')
child.expect('#')
child.sendline('\r')
time.sleep(3)
child.sendline('\r')
child.expect('#')
# child.sendline('copy scp://%s:%s@%s/%s/%s-confg startup-config' % (jumpserver_username, jumpserver_password, jumpserver_infra_host, jumpserver_cfg_path, node_name))
# child.expect('Destination filename \[startup-config\]?')
# child.sendline('\r')
child.sendline('copy tftp://%s/%s-confg startup-config' % (jumpserver_host, node_name))
child.expect('Destination filename \[startup-config\]?')
child.sendline('\r')

'''
Configuration
'''
time.sleep(3)
child.sendline('\r')
child.expect('#')
child.sendline('reload')
i = child.expect(['yes/no]', 'confirm]'])
if i == 0:
    child.sendline('no')
    child.expect('confirm]')
    child.send("\r")
    child.send("\r")
elif i == 1:
    child.send("\r")
    child.send("\r")

