terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.6.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}


resource "aws_vpc" "memos-vpc-tf" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name      = "memos-vpc-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_internet_gateway" "memos-gw-tf" {
  vpc_id = aws_vpc.memos-vpc-tf.id

  tags = {
    Name      = "memos-gw-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_route_table" "memos-rt-tf" {
  vpc_id = aws_vpc.memos-vpc-tf.id

  tags = {
    Name      = "memos-rt-tf"
    ManagedBy = "terraform"
  }

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.memos-gw-tf.id
  }
}

resource "aws_route_table_association" "memos-associ-rt-tf" {
  subnet_id      = aws_subnet.memos-sn-tf.id
  route_table_id = aws_route_table.memos-rt-tf.id
}

resource "aws_subnet" "memos-sn-tf" {
  vpc_id     = aws_vpc.memos-vpc-tf.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name      = "memos-sn-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_network_acl" "memos-acl-tf" {
  vpc_id     = aws_vpc.memos-vpc-tf.id
  subnet_ids = [aws_subnet.memos-sn-tf.id]

  egress {
    protocol   = "-1"
    rule_no    = 210
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = "0"
    to_port    = "0"
  }

  ingress {
    protocol   = "-1"
    rule_no    = 210
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = "0"
    to_port    = "0"
  }

  tags = {
    Name      = "memos-acl-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_security_group" "memos-sg-tf" {
  vpc_id = aws_vpc.memos-vpc-tf.id

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name      = "memos-sg-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_eip_association" "memos-eip_assoc-tf" {
  instance_id   = aws_instance.memos-instance-tf7.id
  allocation_id = aws_eip.memos-eip-tf.id
}

resource "aws_instance" "memos-instance-tf7" {
  #ami           = "ami-04505e74c0741db8d"
  ami           = "ami-0dbf783f8193d25f3"
  instance_type = "t2.micro"
  key_name      = "memos-ami-ubuntu"
  subnet_id     = aws_subnet.memos-sn-tf.id

  tags = {
    Name      = "memos-instance-tf7"
    ManagedBy = "terraform"
  }
}

resource "aws_eip" "memos-eip-tf" {
  vpc        = true
  instance   = aws_instance.memos-instance-tf7.id
  depends_on = [aws_internet_gateway.memos-gw-tf]
}

output "instance_public_dns" {
  description = "The public_ip and public_dns for logging in to the instance."
  value       = "public_ip = ${aws_instance.memos-instance-tf7.public_ip}, and public_dns = ${aws_instance.memos-instance-tf7.public_dns}"
}

