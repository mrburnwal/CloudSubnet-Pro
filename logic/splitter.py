import ipaddress

def split_parent_network(parent_cidr, child_mask=None, num_subnets=None):
    try:
        network = ipaddress.ip_network(parent_cidr, strict=False)
        
        if child_mask:
            # If child_mask is like "24" or "/24"
            if isinstance(child_mask, str) and child_mask.startswith('/'):
                new_prefix = int(child_mask[1:])
            else:
                new_prefix = int(child_mask)
                
            if new_prefix <= network.prefixlen:
                raise ValueError("Child mask must be larger than parent prefix.")
            
            subnets = list(network.subnets(new_prefix=new_prefix))
            
        elif num_subnets:
            num = int(num_subnets)
            # Find the smallest prefix that fits 'num' subnets
            # 2^k >= num => k = ceil(log2(num))
            import math
            k = math.ceil(math.log2(num))
            new_prefix = network.prefixlen + k
            
            if new_prefix > 32:
                raise ValueError("Too many subnets for this parent network.")
                
            subnets = list(network.subnets(new_prefix=new_prefix))[:num]
        else:
            raise ValueError("Must provide either child_mask or num_subnets.")

        return [str(s) for s in subnets]
    except Exception as e:
        raise ValueError(f"Error splitting subnet: {str(e)}")
