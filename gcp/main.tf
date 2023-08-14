
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  project = "cybage-devops"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_compute_network" "vpc_network" {
  name = "sample-python-app-lmt-network"
}

resource "google_compute_firewall" "firewall" {
  name    = "sample-python-app-lmt-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "8080"]
  }

  source_ranges = ["103.81.78.0/24"]
}

# deploy sample-python-app-lmt to cloud run service 
# Path: sample-python-app-lmt\sample-python-app-lmt\gcp\main.tf

resource "google_cloudbuild_trigger" "sample-python-app-lmt" {
  trigger_template {
    branch_name = "main"
    repo_name   = "sample-python-app-lmt"
  }

  filename = "cloudbuild.yaml"
  name     = "sample-python-app-lmt"
}
resource "google_cloud_run_service" "sample-python-app-lmt" {
  name     = "sample-python-app-lmt"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/sample-python-app-lmt/sample-python-app-lmt:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

}

resource "google_cloud_run_service_iam_member" "sample-python-app-lmt" {
  service = google_cloud_run_service.sample-python-app-lmt.name
  location = google_cloud_run_service.sample-python-app-lmt.location
  role = "roles/run.invoker"
  member = "allUsers"
}
