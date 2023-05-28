variable "cloud_id" {
  type    = string
  default = "b1ghmu2f91v5gacflenc"
}

variable "folder_id" {
  type    = string
  default = "b1g22pb8mgkotr12pcoh"
}

variable "zone" {
  type    = string
  default = "ru-central1-a"
}

variable "roles" {
  type    = list(string)
  default = ["vpc.publicAdmin", "load-balancer.admin", "k8s.clusters.agent", "editor", "container-registry.images.puller"]
}

variable "platform_id" {
  type    = string
  default = "standard-v1"
}

variable "allowed_ips" {
  description = "List of allowed IPv4 CIDR blocks."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "cluster_ipv4_range" {
  description = <<EOF
  CIDR block. IP range for allocating pod addresses.
  It should not overlap with any subnet in the network
  the Kubernetes cluster located in. Static routes will
  be set up for this CIDR blocks in node subnets.
  EOF
  type        = string
  default     = "172.17.0.0/16"
}

variable "service_ipv4_range" {
  description = <<EOF
    CIDR block. IP range from which Kubernetes service cluster IP addresses 
    will be allocated from. It should not overlap with
    any subnet in the network the Kubernetes cluster located in
    EOF
  type        = string
  default     = "172.18.0.0/16"
}

variable "k8s_version" {
  default = 1.22
}
