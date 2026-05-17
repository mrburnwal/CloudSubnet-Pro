def generate_terraform_code(vpc_config):
    # vpc_config expected to have 'parent_cidr', 'public_subnets', 'private_subnets', 'database_subnets'
    parent_cidr = vpc_config.get('parent_cidr', '10.0.0.0/16')
    public_subnets = vpc_config.get('public_subnets', [])
    private_subnets = vpc_config.get('private_subnets', [])
    database_subnets = vpc_config.get('database_subnets', [])

    tf = f"""# CloudSubnet Pro - Terraform Generated VPC
resource "aws_vpc" "main" {{
  cidr_block           = "{parent_cidr}"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name = "main-vpc"
  }}
}}

resource "aws_internet_gateway" "igw" {{
  vpc_id = aws_vpc.main.id

  tags = {{
    Name = "main-igw"
  }}
}}
"""

    for i, cidr in enumerate(public_subnets):
        tf += f"""
resource "aws_subnet" "public_{i}" {{
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "{cidr}"
  map_public_ip_on_launch = true

  tags = {{
    Name = "public-subnet-{i}"
  }}
}}
"""

    for i, cidr in enumerate(private_subnets):
        tf += f"""
resource "aws_subnet" "private_{i}" {{
  vpc_id     = aws_vpc.main.id
  cidr_block = "{cidr}"

  tags = {{
    Name = "private-subnet-{i}"
  }}
}}
"""

    for i, cidr in enumerate(database_subnets):
        tf += f"""
resource "aws_subnet" "database_{i}" {{
  vpc_id     = aws_vpc.main.id
  cidr_block = "{cidr}"

  tags = {{
    Name = "database-subnet-{i}"
  }}
}}
"""

    tf += """
# Route Tables and NAT Gateway placeholders would go here.
# Note: NAT Gateways incur costs in AWS.
"""
    return tf
