#!/bin/bash
#$1 for switch
# SNMPv3 credentials
HOST=$1
USER=""
AUTH_PASS=""
PRIV_PASS=""


# OIDs
IF_NAME_OID=".1.3.6.1.2.1.2.2.1.2"
MAC_OID="SNMPv2-SMI::enterprises.9.9.315.1.2.1.1.10"
VLAN_OID="1.3.6.1.4.1.9.9.68.1.2.2.1.2"

# Collect interface names
declare -A if_name_map
while IFS= read -r line; do
    index=$(echo "$line" | awk -F '.' '{print $NF}' | awk '{print $1}')
    value=$(echo "$line" | awk -F ' = ' '{print $2}')
    if [[ -n "$index" ]]; then
        if_name_map["$index"]="$value"
    fi
done < <(snmpwalk -v3 -l authPriv -u "$USER" -a SHA -A "$AUTH_PASS" -x AES -X "$PRIV_PASS" "$HOST" "$IF_NAME_OID")

# Collect VLANs for ifIndex range 9–56
declare -A vlan_map
for ((i=9; i<=73; i++)); do
    vlan_line=$(snmpget -v3 -l authPriv -u "$USER" -a SHA -A "$AUTH_PASS" -x AES -X "$PRIV_PASS" "$HOST" "$VLAN_OID.$i" 2>/dev/null)
    vlan_id=$(echo "$vlan_line" | awk -F ' = ' '{print $2}' | awk '{print $NF}')
    if [[ -n "$vlan_id" ]]; then
        vlan_map["$i"]="$vlan_id"
    fi
done

# Match and print in original format with VLAN
while IFS= read -r line; do
    index=$(echo "$line" | awk -F '.' '{print $NF}' | awk '{print $1}')
    if_name="${if_name_map[$index]}"
    vlan="${vlan_map[$index]}"
    if [[ -n "$if_name" ]]; then
        echo "$line >> $IF_NAME_OID.$index = $if_name | VLAN: ${vlan:-N/A}"
    fi
done < <(snmpwalk -v3 -l authPriv -u "$USER" -a SHA -A "$AUTH_PASS" -x AES -X "$PRIV_PASS" "$HOST" "$MAC_OID")
