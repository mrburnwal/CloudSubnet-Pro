import ipaddress

def validate_overlapping_subnets(cidrs):
    networks = []
    for c in cidrs:
        try:
            networks.append(ipaddress.ip_network(c.strip(), strict=False))
        except ValueError:
            continue
    
    overlaps = []
    for i in range(len(networks)):
        for j in range(i + 1, len(networks)):
            if networks[i].overlaps(networks[j]):
                overlaps.append({
                    "a": str(networks[i]),
                    "b": str(networks[j]),
                    "message": f"{networks[i]} overlaps with {networks[j]}"
                })
                
    return {
        "has_overlap": len(overlaps) > 0,
        "overlaps": overlaps
    }
