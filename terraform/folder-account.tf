// --------------- For FOLDER ACCOUNT --------------- //

resource "yandex_iam_service_account" "sa-resource" {
  name        = "resource-manager"
  description = "service account to manage RESOURCEs"
}

resource "yandex_resourcemanager_folder_iam_binding" "resource-account-rule1" {
  folder_id = var.folder_id
  role      = var.roles[0]

  members = [
    "serviceAccount:${yandex_iam_service_account.sa-resource.id}",
  ]

  depends_on = [
    yandex_iam_service_account.sa-resource
  ]
}

resource "yandex_resourcemanager_folder_iam_binding" "resource-account-rule2" {
  folder_id = var.folder_id
  role      = var.roles[1]

  members = [
    "serviceAccount:${yandex_iam_service_account.sa-resource.id}",
  ]

  depends_on = [
    yandex_iam_service_account.sa-resource
  ]
}

resource "yandex_resourcemanager_folder_iam_binding" "resource-account-rule3" {
  folder_id = var.folder_id
  role      = var.roles[2]

  members = [
    "serviceAccount:${yandex_iam_service_account.sa-resource.id}",
  ]

  depends_on = [
    yandex_iam_service_account.sa-resource
  ]
}

resource "yandex_iam_service_account" "sa-node" {
  name        = "node-manager"
  description = "service account to manage NODEs"
}

resource "yandex_resourcemanager_folder_iam_binding" "node-account" {
  folder_id = var.folder_id
  role      = var.roles[3]

  members = [
    "serviceAccount:${yandex_iam_service_account.sa-node.id}",
  ]

  depends_on = [
    yandex_iam_service_account.sa-node
  ]
}
