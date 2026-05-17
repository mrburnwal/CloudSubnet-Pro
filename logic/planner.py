import ipaddress

def plan_aws_vpc(parent_cidr, config):
    try:
        network = ipaddress.ip_network(parent_cidr, strict=False)
        azs = int(config.get('azs', 2))
        public_count = int(config.get('public', 1))
        private_count = int(config.get('private', 1))
        database_count = int(config.get('database', 1))
        
        # Calculate total subnets needed
        # We assume each type of subnet is spread across AZs
        # Total = (Public + Private + Database) * AZs
        # But for simplicity, the user asks for "Number of public subnets" etc.
        # Usually, you want 1 public per AZ, 1 private per AZ.
        
        # Let's assume the user means "per type, how many subnets in total" or "per AZ"?
        # Standard AWS practice: Type * AZs.
        # But I'll follow the user input directly for now as "Total subnets of this type".
        
        total_subnets_needed = public_count + private_count + database_count
        
        # We need to find a prefix that fits at least total_subnets_needed
        import math
        bits_needed = math.ceil(math.log2(total_subnets_needed)) if total_subnets_needed > 0 else 0
        new_prefix = network.prefixlen + bits_needed
        
        if new_prefix > 32:
            raise ValueError("Parent CIDR is too small for the requested number of subnets.")
            
        all_subnets = list(network.subnets(new_prefix=new_prefix))
        
        plan = {
            "public": [],
            "private": [],
            "database": [],
            "recommendations": [
                "Internet Gateway (IGW) required for Public Subnets.",
                "NAT Gateway required in Public Subnet for Private/DB Subnets internet access.",
                "Public Route Table: Destination 0.0.0.0/0 -> Target IGW.",
                "Private Route Table: Destination 0.0.0.0/0 -> Target NAT Gateway."
            ]
        }
        
        idx = 0
        for i in range(public_count):
            if idx < len(all_subnets):
                plan["public"].append(str(all_subnets[idx]))
                idx += 1
        
        for i in range(private_count):
            if idx < len(all_subnets):
                plan["private"].append(str(all_subnets[idx]))
                idx += 1
                
        for i in range(database_count):
            if idx < len(all_subnets):
                plan["database"].append(str(all_subnets[idx]))
                idx += 1
                
        return plan
    except Exception as e:
        raise ValueError(f"AWS Planning error: {str(e)}")
