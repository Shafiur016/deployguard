variable "container_name" {
  type    = string
  default = "deployguard-terraform"
}
variable "host_port" {
  type    = number
  default = 8003
}

resource "docker_image" "api" {
  name         = "deployguard:local"
  keep_locally = true
  build {
    context = "${path.module}/.."
  }
}

resource "docker_container" "api" {
  name    = var.container_name
  image   = docker_image.api.image_id
  restart = "unless-stopped"
  ports {
    internal = 8002
    external = var.host_port
  }
  healthcheck {
    test     = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8002/readyz', timeout=3)"]
    interval = "20s"
    timeout  = "5s"
    retries  = 3
  }
}
output "healthcheck_url" {
  value = "http://localhost:${var.host_port}/healthz"
}
