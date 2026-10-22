# Enterprise Hybrid Cloud Landing Zone - Oracle Cloud Infrastructure (OCI me-jeddah-1)
# Designed for Zero-SPOF Multi-Tier High-Availability

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 5.0.0"
    }
  }
}

provider "oci" {
  tenancy_ocid = var.tenancy_ocid
  region       = var.region
}

# 1. Virtual Cloud Network (VCN)
resource "oci_core_vcn" "enterprise_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "coe-enterprise-vcn-jeddah"
  dns_label      = "coevcn"
}

# 2. Internet Gateway
resource "oci_core_internet_gateway" "igw" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.enterprise_vcn.id
  display_name   = "coe-internet-gateway"
  enabled        = true
}

# 3. Route Table
resource "oci_core_route_table" "public_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.enterprise_vcn.id
  display_name   = "coe-public-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.igw.id
  }
}

# 4. Security List - HTTPS and WireGuard ingress only (single public subnet skeleton)
resource "oci_core_security_list" "secure_sl" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.enterprise_vcn.id
  display_name   = "coe-security-list"

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
    stateless   = false
  }

  # Ingress HTTPS
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 443
      max = 443
    }
  }

  # Ingress VPN / WireGuard
  ingress_security_rules {
    protocol = "17"
    source   = "0.0.0.0/0"
    udp_options {
      min = 51820
      max = 51820
    }
  }
}

# 5. Public Application Subnet
resource "oci_core_subnet" "public_subnet" {
  cidr_block          = "10.0.1.0/24"
  compartment_id      = var.compartment_ocid
  vcn_id              = oci_core_vcn.enterprise_vcn.id
  display_name        = "coe-public-app-subnet"
  dns_label           = "appsubnet"
  route_table_id      = oci_core_route_table.public_rt.id
  security_list_ids   = [oci_core_security_list.secure_sl.id]
}
