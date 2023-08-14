
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.77.0"
    }
  }
}

provider "google" {
  project = "cybage-devops"
  region  = "us-central1"
  zone    = "us-central1-c"
}

# deploy sample-python-app-lmt to cloud run service 
# Path: sample-python-app-lmt\sample-python-app-lmt\gcp\main.tf

resource "google_cloudbuild_trigger" "sample-python-app-lmt-trigger" {
  source_to_build {
    uri       = "https://github.com/cybage-devops/sample-python-app-lmt.git"
    ref       = "refs/heads/main"
    repo_type = "GITHUB"
  }

  git_file_source {
    path      = "cloudbuild.yaml"
    uri       = "https://github.com/cybage-devops/sample-python-app-lmt.git"
    revision  = "refs/heads/main"
    repo_type = "GITHUB"
  }

  name = "sample-python-app-lmt-trigger"
}
resource "google_cloud_run_service" "sample-python-app-lmt" {
  name     = "sample-python-app-lmt"
  location = "us-central1"
  # ingress = "INGRESS_TRAFFIC_ALL"
  template {
    spec {
      containers {
        # name = "sample-python-app-lmt"
        image = "us-central1-docker.pkg.dev/cybage-devops/sample-python-app-lmt/sample-python-app-lmt:latest"
        ports {
          container_port = 5000
        }
        env {
          name  = "DB_USER_NAME"
          value = "ctgdevops"
        }
        env {
          name  = "DB_HOST"
          value = "40.76.150.114"
        }
        env {
          name  = "DB_NAME"
          value = "ctg_devops_ktracker"
        }
        env {
          name = "DB_PASSWORD"
          value_from {
            secret_key_ref {
              name = "cloud-run-python-app-db-secret"
              key  = "1"
            }
          }
        }
      }
    }
  }
    traffic {
      percent         = 100
      latest_revision = true
    }
  
}

resource "google_cloud_run_service_iam_member" "sample-python-app-lmt-i-am" {
  service  = google_cloud_run_service.sample-python-app-lmt.name
  location = google_cloud_run_service.sample-python-app-lmt.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
