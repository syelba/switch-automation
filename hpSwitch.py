from netmiko import ConnectHandler



class ConfigSwitch():

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        self.hp_switch = {
            'device_type': 'hp_procurve',  # Device type for HP ProCurve/ArubaOS switches
            'host': f'{self.ip}',  # IP address of the switch
            'username': f'{self.username}',  # Username to login
            'password': f'{self.password}',  # Password to login
            'port': 22,  # SSH port (default is 22)
        }


    def setSNTP(self):
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

    from netmiko import ConnectHandler

def setSNMPV3(self, user, sha, password):
    configSNMPV3 = [
        'configure',
        'no snmpv3 enable',  # Reset SNMPv3
        'snmpv3 enable',  # Enable SNMPv3
        f'snmpv3 user {user} auth sha {sha} priv AES128 {password}',  # Create SNMPv3 user
        'show snmpv3 user',  # Verify configuration
        'snmpv3 restricted-access'
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

