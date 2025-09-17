README - Terraform explainable notes
-----------------------------------
- This folder shows a minimal Terraform setup. Each resource is commented.
- To run:
  1. Install terraform
  2. Configure AWS credentials in env (AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY)
  3. terraform init
  4. terraform plan -var='s3_bucket_name=your-unique-bucket-name'
  5. terraform apply -var='s3_bucket_name=your-unique-bucket-name' -auto-approve
- Remember: creating RDS & EC2 costs money—destroy with `terraform destroy` when done.
