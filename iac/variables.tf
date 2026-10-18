variable "tenancy_ocid" {
  description = "OCID of the enterprise OCI tenancy"
  type        = string
  default     = "ocid1.tenancy.oc1..aaaaaaaam2bdbfk4wcxurwvccl7cu2veljv3on7i3xdtibtqvmo7zueg6ueq"
}

variable "compartment_ocid" {
  description = "OCID of the target compartment"
  type        = string
  default     = "ocid1.tenancy.oc1..aaaaaaaam2bdbfk4wcxurwvccl7cu2veljv3on7i3xdtibtqvmo7zueg6ueq"
}

variable "region" {
  description = "OCI region in the Kingdom of Saudi Arabia"
  type        = string
  default     = "me-jeddah-1"
}
