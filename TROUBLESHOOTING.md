# Troubleshooting Log — Job Application Tracker DevOps Project

This log documents the real issues encountered while building and deploying the Job Application Tracker pipeline — from local testing through CI/CD, container security, Kubernetes, GitOps, and monitoring — along with the root cause and fix for each. It's kept separate from the main [README](README.md) since it's the most detailed, log-style part of the project.

Each issue was diagnosed using logs, command-line diagnostics, and configuration changes, then re-verified before moving on.

## Python / Pytest Environment

Pytest was initially unavailable when using the system Python environment. A Python virtual environment was created and project dependencies were installed:

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python -m pytest -v
```

The final test suite completed successfully.

## Docker Daemon

Docker commands initially failed because the Docker daemon was not running. Docker Desktop was started and the environment was verified:

```bash
docker version
docker ps
```

The Docker image was then built and tested successfully.

## Docker Image Vulnerabilities

The initial Docker image contained vulnerabilities in packages from the Debian base image. The base image and packages were updated, followed by another image build and Trivy scan. The final CI security scan completed successfully.

## SonarCloud Integration

SonarCloud initially required project configuration and GitHub Actions integration. The `sonar-project.properties` configuration file was added, and SonarCloud analysis was integrated into the GitHub Actions workflow.

## GitHub Actions AWS OIDC Authentication

GitHub Actions initially failed while attempting to assume the AWS IAM role, with an error similar to:

```text
Not authorized to perform sts:AssumeRoleWithWebIdentity
```

The AWS IAM trust relationship was corrected to properly authorize the GitHub Actions OIDC identity. After the correction, GitHub Actions successfully authenticated with AWS without using long-lived AWS access keys.

## Amazon ECR Permissions

The GitHub Actions IAM role required the correct permissions for Amazon ECR operations. A dedicated ECR push policy was configured, and the workflow then successfully authenticated with ECR and pushed the Docker image.

## Kubernetes Manifest Directory Structure

The Kubernetes manifests were temporarily placed inside an incorrect nested directory (`k8s/k8s/`). The structure was corrected to a flat `k8s/` directory:

```text
k8s/
├── namespace.yaml
├── deployment.yaml
├── service.yaml
├── ingress.yaml
└── argocd-application.yaml
```

This allowed Argo CD to correctly locate and synchronize the application manifests.

## Argo CD Service Synchronization

Argo CD initially synchronized the application but the Kubernetes Service was missing because the Service manifest had not yet been pushed to GitHub. Once the manifest was added and pushed, Argo CD detected the change and synchronized the missing resource.

## Private ECR Image Pull

K3s initially required additional configuration to pull the private ECR image. An ECR credential provider was installed and configured for the K3s kubelet, and an EC2 IAM role with ECR read-only permissions was attached to the Kubernetes host. The private image pull was then successfully verified.

## Argo CD Port Forwarding

While accessing Argo CD locally, a second port-forward attempt produced:

```text
Unable to listen on port 8080
address already in use
```

The existing listener was checked using:

```bash
sudo ss -ltnp | grep :8080
```

An existing `kubectl port-forward` process was already using the port, so it was reused instead of starting another one.

## Kubernetes Ingress

The application needed to be accessible externally while keeping the application Service as a ClusterIP. Traefik Ingress was configured to route external traffic in through the Service rather than exposing it directly, and the application was successfully accessed through the configured Ingress.

## Prometheus and Grafana Monitoring

After installing the monitoring stack, Prometheus targets were verified through the Targets page, with multiple Kubernetes and monitoring targets reporting `UP`. Grafana dashboards were then verified for cluster and pod-level metrics, confirming the Job Application Tracker workloads were visible in the Kubernetes resource dashboards.