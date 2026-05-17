import ipaddress

def calculate_cidr_details(cidr_str):
    try:
        network = ipaddress.ip_network(cidr_str, strict=False)
        print(network)
        # AWS reserves 5 IPs:
        # 1. Network address
        # 2. VPC router
        # 3. DNS
        # 4. Future use
        # 5. Broadcast address
        # So it's total_ips - 5. If it's a /32 or /31, it's different but usually subnets are larger.
        aws_usable = max(0, network.num_addresses - 5)
        print(aws_usable)
        
        # Traditional usable: total - 2 (network and broadcast)
        # For /31 and /32, it's special in ipaddress module, but we'll follow standard rules for subnets.
        if network.prefixlen == 32:
            traditional_usable = 1
            aws_usable = 0
        elif network.prefixlen == 31:
            traditional_usable = 0
            aws_usable = 0
        else:
            traditional_usable = network.num_addresses - 2

        return {
            "network_address": str(network.network_address),
            "broadcast_address": str(network.broadcast_address),
            "total_ips": network.num_addresses,
            "traditional_usable": traditional_usable,
            "aws_usable": aws_usable,
            "subnet_mask": str(network.netmask),
            "wildcard_mask": str(network.hostmask),
            "first_usable": str(network[1]) if network.num_addresses > 2 else str(network[0]),
            "last_usable": str(network[-2]) if network.num_addresses > 2 else str(network[-1]),
            "prefix": network.prefixlen
        }
    except ValueError as e:
        raise ValueError(f"Invalid CIDR block: {str(e)}")

