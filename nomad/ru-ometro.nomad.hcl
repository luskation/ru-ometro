# Passed by the pipeline: nomad job run -var "image=ghcr.io/<owner>/ru-ometro:<sha>" ...
variable "image" {
  type    = string
  default = "ru-ometro:local"
}

job "ru-ometro" {
  datacenters = ["dc1"]
  type        = "service"

  group "api" {
    count = 1

    network {
      # Host port 8080 -> container port 8000
      port "http" {
        static = 8080
        to     = 8000
      }
    }

    # Equivalent to the K8s Service + probes
    service {
      name     = "ru-ometro"
      provider = "nomad"
      port     = "http"

      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }

    # Equivalent to the K8s RollingUpdate strategy
    update {
      max_parallel     = 1
      health_check     = "checks"
      min_healthy_time = "10s"
      healthy_deadline = "2m"
      auto_revert      = true
    }

    # Restart the task at most 3 times every 5 minutes before failing
    restart {
      attempts = 3
      interval = "5m"
      delay    = "10s"
      mode     = "fail"
    }

    task "api" {
      driver = "docker"

      config {
        image = var.image
        ports = ["http"]
      }

      # Same values as k8s/configmap.yaml
      env {
        APP_NAME  = "RU-ometro"
        SEED_DATA = "true"
        LOG_LEVEL = "info"
      }

      resources {
        cpu    = 200 # MHz
        memory = 128 # MB
      }
    }
  }
}
