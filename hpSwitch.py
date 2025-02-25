from netmiko import ConnectHandler

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

    def setSNMPV3(self):
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
