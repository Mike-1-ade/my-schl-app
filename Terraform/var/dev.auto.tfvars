aws_region = "eu-west-2"
vpc_cidr_block = "10.0.0.0/16"
public_subnet_cidr_blocks = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
private_subnet_cidr_blocks  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
availability_zones = ["eu-west-2a", "eu-west-2b", "eu-west-2c"]
cluster_name = "eks-cluster-taskimage"
instance_type = "t3.medium"
iam_role_name_node = "eks-auto-node-taskimage"
node_group_name = "eks-node-group-taskimage"
iam_role_name_cluster = "eks-cluster-taskimage"
desired_capacity = 2
max_size = 3
min_size = 1
update_config_max_unavailable =2

