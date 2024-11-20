import pulumi
import pulumi_aws as aws


# Create a new VPC and subnet first
vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "foreverLc-vpc"}
)

subnet = aws.ec2.Subnet(
    "my-subnet",
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
            "cidr_blocks": ["0.0.0.0/0"]
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
