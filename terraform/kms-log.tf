// --------------- For KMS --------------- //

resource "yandex_kms_symmetric_key" "key-a" {
  name              = "kms-key"
  description       = "description for key"
  default_algorithm = "AES_128"
  rotation_period   = "8760h" // equal to 1 year
}

// --------------- For LOG GROUP --------------- //

resource "yandex_logging_group" "group1" {
  name = "test-logging-group"
}