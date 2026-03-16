# AWS Snapshot Cleanup

## Overview
This project deploys an AWS Lambda function inside a VPC to automatically identify and delete EC2 snapshots older than 365 days.

## Chosen IaC Tool
Terraform was chosen because it is simple, readable, modular, and widely used for AWS infrastructure automation.

## Solution Components
- VPC
- Private subnet
- Security group for Lambda
- IAM role and policy for Lambda
- AWS Lambda function written in Python
- EventBridge rule to trigger the Lambda daily
- CloudWatch Logs for monitoring

## Lambda Function Behavior
The Lambda function:
1. Connects to AWS EC2 using boto3
2. Retrieves snapshots owned by the current AWS account
3. Filters snapshots older than 365 days using `StartTime`
4. Attempts to delete old snapshots
5. Logs actions and errors to CloudWatch Logs

## Repository Structure
```text
Aws-snapshot-cleanup/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── networking.tf
│   ├── iam.tf
│   ├── lambda.tf
│   └── eventbridge.tf
├── lambda/
│   └── cleanup_snapshots.py
└── README.md

## Deployment Steps

### 1. Package the Lambda Function

Navigate to the lambda folder and package the code:

```bash
cd lambda
zip function.zip cleanup_snapshots.py

cd terraform
terraform init

terraform plan


---


