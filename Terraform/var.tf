variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidr_blocks" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones for the subnets"
  type        = list(string)
}

variable "private_subnet_cidr_blocks" {
  description = "CIDR blocks for the private subnets"
  type        = list(string)
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "iam_role_name_cluster" {
  description = "Name of the IAM role for the EKS cluster"
  type        = string
}

variable "iam_role_name_node" {
  description = "Name of the IAM role for the EKS worker nodes"
  type        = string
}

variable "node_group_name" {
  description = "Name of the EKS node group"
  type        = string
}

variable "desired_capacity" {
  description = "Desired number of worker nodes in the EKS node group"
  type        = number
}

variable "max_size" {
  description = "Maximum number of worker nodes in the EKS node group"
  type        = number
}

variable "min_size" {
  description = "Minimum number of worker nodes in the EKS node group"
  type        = number
}

variable "update_config_max_unavailable" {
  description = "Maximum number of worker nodes that can be unavailable during an update"
  type        = number
}

variable "instance_type" {
  description = "EC2 instance type for the EKS worker nodes"
  type        = string
}

