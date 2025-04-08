import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def query_oid(host, user, auth_pass, priv_pass, oid):
    """
    Queries a specific OID from an SNMP agent using SNMPv3.

    Parameters:
        host (str): Hostname or IP address of the SNMP agent.
        user (str): Security username for SNMPv3.
        auth_pass (str): Authentication password.
        priv_pass (str): Privacy password.
        oid (str): OID to query.

    Returns:
        str: The SNMP query result or "N/A" if the query fails.
    """
    command = (
        f"snmpget -v3 -l authPriv -u {user} "
        f"-a SHA -A '{auth_pass}' -x AES -X '{priv_pass}' {host} {oid}"
    )

    print(f"\nRunning SNMP command: {command}")
    output = os.popen(command).read().strip()

    if "Timeout" in output or "Error" in output or not output:
        print(f"SNMP query failed for {host}, OID {oid}")
        return "N/A"
    else:
        result = output.split("= ", 1)[-1].strip()
        print(f"SNMP query successful for {host}, OID {oid}: {result}")
        return result

def update_csv_results(csv_file, user, auth_pass, priv_pass):
    """
    Updates the CSV file with connectivity results and hardware information.

    Parameters:
        csv_file (str): Path to the CSV file.
        user (str): Security username for SNMPv3.
        auth_pass (str): Authentication password.
        priv_pass (str): Privacy password.
    """
    # Ensure CSV file exists before reading
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    try:
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Ensure required columns exist
        required_columns = ['switch_name', 'modal_name', 'system_location', 'sn']
        for col in required_columns:
            if col not in df.columns:
                df[col] = "N/A"  # Add missing columns

        # Iterate over each switch_name and retrieve SNMP data
        for index, row in df.iterrows():
            host = row['switch_name']
            print(f"\nQuerying SNMP data for {host}...")

            # Query the required OIDs
            model_name = query_oid(host, user, auth_pass, priv_pass, "1.3.6.1.2.1.47.1.1.1.1.13.1")
            system_location = query_oid(host, user, auth_pass, priv_pass, "1.3.6.1.2.1.1.6.0")
            serial_number = query_oid(host, user, auth_pass, priv_pass, "1.3.6.1.2.1.47.1.1.1.1.11.1")

            # Update DataFrame with retrieved values
            df.loc[index, 'modal_name'] = model_name
            df.loc[index, 'system_location'] = system_location
            df.loc[index, 'sn'] = serial_number

        # Save updated results back to CSV
        df.to_csv(csv_file, index=False)
        print("\n✅ Results successfully updated in the CSV file.")

    except Exception as e:
        print(f"Error processing CSV file: {e}")

# Example Usage
csv_file = "las_list.csv"  # CSV file must be in the same directory

update_csv_results(
    csv_file=csv_file,
    user=os.getenv('las_user'),
    auth_pass=os.getenv('auth'),
    priv_pass=os.getenv('AES128')
)
