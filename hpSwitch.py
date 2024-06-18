from netmiko import ConnectHandler
import time

# Define the device to connect to
hp_switch = {
    'device_type': 'hp_procurve',  # Device type for HP ProCurve/ArubaOS switches
    'host': '10.12.212.120',  # IP address of the switch
    'username': 'ils',  # Username to login
    'password': 'Pa$$w0rd',  # Password to login
    'port': 22,  # SSH port (default is 22)
}

ilsManaged = ['10.12.183.32', '10.12.188.252', '10.12.188.240', '10.12.185.241', '10.12.185.253', '10.12.177.252',
              '10.12.177.251', '10.12.186.253', '10.12.186.84', '10.12.186.16', '10.12.184.188', '10.12.189.59',
              '10.12.189.80', '10.12.183.44', '10.12.189.106','10.12.189.4'
              ]


def configHP(hp_switch, configuration):
    # Establish the connection
    # Use ** to unpack the dictionary into keyword arguments for ConnectHandler
    net_connect = ConnectHandler(**hp_switch)
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


# Execute a configuration command
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

# # Iterate over the list of IP addresses
# for ip in ilsManaged:
#     # Update the host in the base configuration
#     hp_switch = hp_switch.copy()
#     hp_switch['host'] = '10.12.183.32'
#     configHP(ip,setTime)
for ip in ilsManaged:
    hp_switch = hp_switch.copy()
    print(ip)
    hp_switch['host'] = ip
    try:
        print(configHP(hp_switch,setTime))
    except Exception as e:
        print(e)
