
import os
import pandas as pd
from dotenv import load_dotenv
from netmiko import ConnectHandler
load_dotenv()


class ConfigSwitch():

    def __init__(self,IP):
        self.ip = IP
        self.cisco_device = {
            'device_type': 'cisco_ios',  # Device type for HP ProCurve/ArubaOS switches
            'host': f'{IP}',  # IP address of the switch
            'username': f'{os.getenv('cisco_user')}',  # Username to login
            'password': f'{os.getenv('cisco_password')}',  # Password to login
            'secret': os.getenv("secret"),
            'port': 22,  # SSH port (default is 22)
            'global_delay_factor': 2,  # You can add this to give more time for commands
        }


    def setSNMPV3(self):
        net_connect = ConnectHandler(**self.cisco_device)

        # Enter enable mode using the 'secret' enable password
        net_connect.enable()  # This uses the 'secret' value to enter enable mode

        config_commands = [
            'no snmp-server',
            'snmp-server view SNMP-RO iso included', #set read only'
            f'snmp-server group {os.getenv('cisco_group')} v3 priv read SNMP-RO', #SNMP-RO its alias just a name no config type
            f'snmp-server user {os.getenv('cisco_SNMP3_user')} {os.getenv('cisco_group')} v3 auth sha {os.getenv('cisco_auth')} priv aes 128 {os.getenv('cisco_priv_key')}',
            'ip access-list standard SNMP-RO',
            'permit 10.189.180.41',
            'permit 10.189.180.65',
            'permit 10.66.225.195',
            'permit 10.66.225.197',
            'permit 10.185.11.128',
            'permit 10.185.227.93',
            'permit 10.12.176.13',
            'permit 10.190.220.132', 
            'permit 10.190.220.133',
            'permit 10.190.220.134',
            'permit 10.190.220.135',
            'permit 10.165.91.253',
            'permit 10.185.69.2',
            'permit 10.185.69.3',
            'permit 10.185.69.4',
            'permit 10.189.192.4',
            'permit 10.189.192.5',
            'permit 10.189.192.6',
            'permit 10.189.192.7',
            'permit 10.13.160.4',
            'permit 10.13.160.5',
            'permit 10.13.160.6',
            'permit 10.13.160.7'
        ]
        output = net_connect.send_config_set(config_commands)
        print(output)
        net_connect.disconnect()


data = []
for i in data:
    runnner = ConfigSwitch(IP=i)
    runnner.setSNMPV3()
