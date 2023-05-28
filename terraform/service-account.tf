// --------------- For SERVICE ACCOUNT --------------- //

resource "yandex_iam_service_account" "service-account" {
  name        = "service-account"
  description = "<service account description>"
}

resource "yandex_resourcemanager_folder_iam_member" "editor" {
  # Service account to be assigned "editor" role.
  folder_id = var.folder_id
  role      = var.roles[3]
  member    = "serviceAccount:${yandex_iam_service_account.service-account.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "images-puller" {
  # Service account to be assigned "container-registry.images.puller" role.
  folder_id = var.folder_id
  role      = var.roles[4]
  member    = "serviceAccount:${yandex_iam_service_account.service-account.id}"
}
