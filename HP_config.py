from netmiko import ConnectHandler
import os
from dotenv import load_dotenv
load_dotenv()




class ConfigHPSwitch():

    def __init__(self, ip):
        self.ip = ip
        self.username = os.getenv('cisco_user')
        self.password = os.getenv('cisco_password')

        self.hp_switch = {
            'device_type': 'hp_procurve',  # Device type for HP ProCurve/ArubaOS switches
            'host': f'{self.ip}',  # IP address of the switch
            'username': f'{self.username}',  # Username to login
            'password': f'{self.password}',  # Password to login
            'port': 22,  # SSH port (default is 22)
        }


    def setSNTP_HP(self):
        setTime = [
            'configure',
            'time',
            'sntp',
            'sntp server priority 1 10.128.12.31',
            'sntp server priority 2 10.128.12.32',
            'show sntp',
            'timesync sntp',
            'sntp unicast',
            'time'
        ]
        # Establish the connection
        # Use ** to unpack the dictionary into keyword arguments for ConnectHandler
        net_connect = ConnectHandler(**self.hp_switch)
        # Enter enable mode (if necessary)
        net_connect.enable()
        # Enter configuration mode
        net_connect.config_mode()
        try:
            output = net_connect.send_config_set(setTime)
            net_connect.disconnect()
            return output
        except Exception as e:
            net_connect.disconnect()
            return e


    def setSNMPV3_HP(self):
        configSNMPV3 = [
            'configure',
            'no snmpv3 enable',  # Reset SNMPv3
            'snmpv3 enable',  # Enable SNMPv3
            f'snmpv3 user {os.getenv('cisco_SNMP3_user')} auth sha {os.getenv('cisco_auth')} priv AES 128 {os.getenv('cisco_priv_key')}',  # Create SNMPv3 user
            'show snmpv3 user',  # Verify configuration
            'snmpv3 restricted-access',
            'snmpv3 user secureUser ip 10.189.180.41',
            'snmpv3 user secureUser ip 10.189.180.65',
            'snmpv3 user secureUser ip 10.66.225.195',
            'snmpv3 user secureUser ip 10.66.225.197',
            'snmpv3 user secureUser ip 10.185.11.128',
            'snmpv3 user secureUser ip 10.185.227.93',
            'snmpv3 user secureUser ip 10.12.176.13',
            'snmpv3 user secureUser ip 10.190.220.132', 
            'snmpv3 user secureUser ip 10.190.220.133',
            'snmpv3 user secureUser ip 10.190.220.134',
            'snmpv3 user secureUser ip 10.190.220.135',
            'snmpv3 user secureUser ip 10.165.91.253',
            'snmpv3 user secureUser ip 10.185.69.2',
            'snmpv3 user secureUser ip 10.185.69.3',
            'snmpv3 user secureUser ip 10.185.69.4',
            'snmpv3 user secureUser ip 10.189.192.4',
            'snmpv3 user secureUser ip 10.189.192.5',
            'snmpv3 user secureUser ip 10.189.192.6',
            'snmpv3 user secureUser ip 10.189.192.7',
            'snmpv3 user secureUser ip 10.13.160.4',
            'snmpv3 user secureUser ip 10.13.160.5',
            'snmpv3 user secureUser ip 10.13.160.6',
            'snmpv3 user secureUser ip 10.13.160.7'
        ]
        # Establish the connection
        net_connect = ConnectHandler(**self.hp_switch)
        try:
            net_connect.enable()
            net_connect.config_mode()
            
            # Send the configuration set
            output = net_connect.send_config_set(configSNMPV3, exit_config_mode=True, cmd_verify=False)

            # Handle potential confirmation prompts
            if "y/n" in output.lower():
                output += net_connect.send_command_timing("y")  # Auto-confirm with "y"

            net_connect.disconnect()
            return output
        except Exception as e:
            net_connect.disconnect()
            return str(e)

