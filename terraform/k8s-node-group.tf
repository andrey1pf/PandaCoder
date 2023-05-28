// --------------- For NODE GROUP --------------- //

resource "yandex_kubernetes_node_group" "panda_coder_node_group" {
  cluster_id  = yandex_kubernetes_cluster.zonal_cluster_panda_coder.id
  name        = "panda-coder-nodes"
  description = "description"
  
  version = var.k8s_version

  instance_template {
    platform_id = var.platform_id

    network_interface {
      nat                = true
      subnet_ids         = ["${yandex_vpc_subnet.vpc-subnet-a.id}"]
      security_group_ids = ["${yandex_vpc_security_group.sg-1.id}"]
    }

    resources {
      memory = 4
      cores  = 2
    }

    boot_disk {
      type = "network-hdd"
      size = 64
    }

    scheduling_policy {
      preemptible = false
    }

    container_runtime {
      type = "containerd"
    }
  }

  scale_policy {
    fixed_scale {
      size = 2
    }
  }

  allocation_policy {
    location {
      zone = var.zone
    }
  }

  maintenance_policy {
    auto_upgrade = true
    auto_repair  = true
  }
}
