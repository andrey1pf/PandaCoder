// --------------- For KUBERNETES --------------- //

resource "yandex_kubernetes_cluster" "zonal_cluster_panda_coder" {
  depends_on = [
    yandex_resourcemanager_folder_iam_member.editor,
    yandex_resourcemanager_folder_iam_member.images-puller,
    yandex_vpc_security_group.sg-1
  ]

  name        = "kebernetes-cluster"
  description = "description"

  network_id = yandex_vpc_network.vpc-net.id

  master {
    version = var.k8s_version
    zonal {
      zone      = yandex_vpc_subnet.vpc-subnet-a.zone
      subnet_id = yandex_vpc_subnet.vpc-subnet-a.id
    }

    public_ip = true

    security_group_ids = ["${yandex_vpc_security_group.sg-1.id}"]

    maintenance_policy {
      auto_upgrade = true

      maintenance_window {
        start_time = "15:00"
        duration   = "3h"
      }
    }

    # master_logging {
    #   enabled                    = true
    #   log_group_id               = yandex_logging_group.group1.id
    #   kube_apiserver_enabled     = true
    #   cluster_autoscaler_enabled = true
    #   events_enabled             = true
    # }
  }

  service_account_id      = yandex_iam_service_account.service-account.id
  node_service_account_id = yandex_iam_service_account.sa-node.id

  release_channel         = "RAPID"
  network_policy_provider = "CALICO"

  kms_provider {
    key_id = yandex_kms_symmetric_key.key-a.id
  }
}