// --------------- For VPC NET --------------- //

resource "yandex_vpc_network" "vpc-net" {
  name = "vpc-k8s"
}

resource "yandex_vpc_subnet" "vpc-subnet-a" {
  v4_cidr_blocks = ["10.100.0.0/16"]
  network_id     = yandex_vpc_network.vpc-net.id
  zone           = var.zone
}

// --------------- For VPC SECURITY GROUP --------------- //

resource "yandex_vpc_security_group" "sg-1" {
  name        = "security-g1"
  description = "description for my security group"
  network_id  = yandex_vpc_network.vpc-net.id

  ingress {
    protocol       = "ANY"
    description    = "All incoming access"
    v4_cidr_blocks = try(var.allowed_ips, "0.0.0.0/0")
    port           = -1
  }
  ingress {
    protocol          = "TCP"
    description       = "Rule allows availability checks from load balancer's address range. It is required for the operation of a fault-tolerant cluster and load balancer services."
    predefined_target = "loadbalancer_healthchecks"
    v4_cidr_blocks    = ["0.0.0.0/0"]
    port              = 80
  }

  ingress {
    protocol          = "TCP"
    description       = "Rule allows availability checks from load balancer's address range. It is required for the operation of a fault-tolerant cluster and load balancer services."
    predefined_target = "loadbalancer_healthchecks"
    from_port         = 0
    to_port           = 65535
  }

  ingress {
    protocol          = "ANY"
    description       = "Rule allows master-node and node-node communication inside a security group."
    predefined_target = "self_security_group"
    from_port         = 0
    to_port           = 65535
  }

  ingress {
    protocol       = "ANY"
    description    = "Rule allows pod-pod and service-service communication inside a security group. Indicate your IP ranges."
    v4_cidr_blocks = [var.cluster_ipv4_range, var.service_ipv4_range]
    from_port      = 0
    to_port        = 65535
  }

  ingress {
    protocol       = "TCP"
    description    = "Rule allows incomming traffic from the Internet to the NodePort port range. Add ports or change existing ones to the required ports."
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 30000
    to_port        = 32767
  }

  ingress {
    protocol       = "TCP"
    description    = "Rule allows incomming traffic from the Internet for kubeconfig"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 6443
  }

  ingress {
    protocol       = "TCP"
    description    = "Rule allows incomming traffic from the Internet for kubeconfig"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 443
  }

  egress {
    protocol       = "ANY"
    description    = "Rule allows all outgoing traffic. Nodes can connect to Yandex Container Registry, Yandex Object Storage, Docker Hub, and so on."
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 0
    to_port        = 65535
  }
}
