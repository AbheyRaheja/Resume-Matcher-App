############################################################
# Simple Terraform example (EXPLAINABLE)
#
# This file shows a minimal set of AWS resources commonly
# used for ML projects. It is intentionally simple and heavily
# commented so you can read and explain each block.
#
# WARNING: This is a learning example. Do NOT run in production
# without reviewing security (IAM policies, passwords, VPC, etc).
############################################################

provider "aws" {
  # region will be provided via variable or environment
  region = var.aws_region
}

############################################################
# 1) S3 Bucket: used to store artifacts like model files,
#    DVC remote, or MLflow artifacts (in production you would
#    use this to store trained model files & datasets).
############################################################
resource "aws_s3_bucket" "artifacts" {
  bucket = var.s3_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name = "${var.project_name}-artifacts"
    Project = var.project_name
  }
}

############################################################
# 2) IAM Role for EC2: gives the EC2 instance permission to
#    access S3 and other AWS services securely (best practice
#    is to assign minimal permissions needed).
############################################################
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "${var.project_name}-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

############################################################
# Attach a managed policy that allows S3 access. In the real
# world you'd create a custom policy with least privilege.
############################################################
resource "aws_iam_role_policy_attachment" "ec2_s3_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

############################################################
# 3) RDS (Postgres): often used as MLflow backend store.
#    This example creates a small db instance. It is stateful
#    and will cost money if created — treat with care.
############################################################
resource "aws_db_instance" "mlflow_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "14.5"
  instance_class       = "db.t3.micro"
  name                 = "mlflowdb"
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
  tags = {
    Name = "${var.project_name}-db"
  }
}

############################################################
# 4) DynamoDB: small NoSQL table for caching or job lookups.
############################################################
resource "aws_dynamodb_table" "jobs_table" {
  name         = "${var.project_name}-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "jobId"

  attribute {
    name = "jobId"
    type = "S"
  }

  tags = {
    Project = var.project_name
  }
}

############################################################
# 5) EC2 Instance: a simple compute host. In production you'd
#    likely use ECS/EKS or an ASG behind a load balancer.
############################################################
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  owners = ["099720109477"] # Canonical's owner ID for Ubuntu
}

resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  tags = {
    Name = "${var.project_name}-instance"
  }
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

############################################################
# Outputs: values returned after 'terraform apply' to help
# you connect services (like the S3 bucket name, DB endpoint).
############################################################
output "s3_bucket_name" {
  value = aws_s3_bucket.artifacts.bucket
}
output "db_endpoint" {
  value = aws_db_instance.mlflow_db.address
}
