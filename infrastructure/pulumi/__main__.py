import pulumi
import pulumi_aws as aws


config = pulumi.Config()
allowed_ip = config.require_secret('ip_address')
public_key = config.require("public_key")


# Django Configurations
django_secret = config.require_secret('django_secret_key')
django_allowed_hosts = config.require_secret('django_allowed_hosts')

# Database configuration
db_password = config.require_secret('db_password')
db_user = config.require_secret('db_user')
db_host = config.require_secret('db_host')
db_port = config.require_secret('db_port')
db_name = config.require_secret('db_name')

# OAuth credentials
oidc_client_id = config.require_secret('oidc_client_id')
oidc_client_secret = config.require_secret('oidc_client_secret')
oidc_provider_url = config.require_secret('oidc_provider_url')

# API Credentials
africas_talking_api_key = config.require_secret('africas_talking_api_key')
africas_talking_username = config.require_secret('africas_talking_username')


# Create a new VPC and subnet first
vpc = aws.ec2.Vpc(
    "foreverLc-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "foreverLc-vpc"}
)

subnet = aws.ec2.Subnet(
    "foreverLc-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={"Name": "forever-locket"}
)

# Creating Security group
security_group = aws.ec2.SecurityGroup(
    "web-secgrp",
    description="Enable HTTP access",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"]
        },
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": [allowed_ip]
        }
    ],
    egress=[
        {
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"]
        }
    ]
)

# Create a key pair
key_pair = aws.ec2.KeyPair(
    "foreverlc-ec2",
    public_key=public_key
)

# Creating EC2 instance
instance = aws.ec2.Instance(
    "web-server",
    instance_type="t2.micro",
    vpc_security_group_ids=[security_group.id],
    subnet_id=subnet.id,
    ami="ami-0664c8f94c2a2261b",
    tags={"Name": "foreverLc-server"}
)

# Export the instance's public IP
pulumi.export('public_ip', instance.public_ip)
