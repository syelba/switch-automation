from netmiko import ConnectHandler
import logging

# Enable logging for troubleshooting (optional)
logging.basicConfig(filename='netmiko_log.txt', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

# Define the device to connect to
raritan_pdu = {
    'device_type': 'linux',      # Custom device type for Raritan PDU (you may need to check Netmiko documentation or source for exact type)
    'host': '192.168.1.1',         # IP address of the PDU
    'username': 'user',           # Username to login
    'password': 'password',        # Password to login
    'port': 22,                    # SSH port (default is 22)
}

try:
    # Establish the connection
    net_connect = ConnectHandler(**raritan_pdu)

    # Execute a command (example: show status or similar command for Raritan PDU)
    output = net_connect.send_command('show network')
    # Print the output
    print(output)

    # Disconnect from the PDU
    net_connect.disconnect()

except Exception as e:
    print(f"An error occurred: {e}")
