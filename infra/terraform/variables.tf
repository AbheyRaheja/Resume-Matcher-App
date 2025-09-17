variable "aws_region" {
  description = "AWS region to deploy into"
  type = string
  default = "us-east-1"
}

variable "project_name" {
  description = "A short name for tagging resources"
  type = string
  default = "resume-matcher-explainable"
}

variable "s3_bucket_name" {
  description = "S3 bucket name (must be globally unique)"
  type = string
  default = "resume-matcher-explainable-bucket-123456789"
}

variable "db_username" {
  description = "RDS master username"
  type = string
  default = "mlflowuser"
}

variable "db_password" {
  description = "RDS master password (DO NOT use this in prod)"
  type = string
  default = "ChangeMe123!"
}
