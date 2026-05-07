variable "project_name" {
  description = "Project name"
  type        = string
  default     = "devsecops-task"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "allowed_cidr" {
  description = "Allowed ingress CIDR"
  type        = string
  default     = "0.0.0.0/0"
}