# Infrastructure Troubleshooting Skill

This skill is activated when infrastructure troubleshooting is needed, covering:
- **Terraform** code for AWS resources (IAM, S3, EKS, etc.)
- **Kustomize** and **Helm** code for application deployments in EKS (Kubernetes)

---

## Repository Base Path

All repositories are located in: `~/github`

---

## Terraform Repository: `terraform-base`

| Environment | Folders |
|-------------|---------|
| **DEV** | `terraform-dev2` |
| **STAGE (INFRA)** | `stage/app-layer/stage-i`, `stage/base-layer/stage-i` |
| **STAGE (INFRA 2)** | `stage/app-layer/stage-infra-2`, `stage/base-layer/stage-infra-2` |
| **PROD (BOSTON)** | `prod/app-layer/prod`, `prod/base-layer/prod` |
| **PROD (HOUSTON)** | `prod/app-layer/infra-houston`, `prod/base-layer/infra-houston` |

**Full paths:**
- DEV: `~/github/terraform-base/terraform-dev2`
- STAGE (INFRA): `~/github/terraform-base/stage/app-layer/stage-i`, `~/github/terraform-base/stage/base-layer/stage-i`
- STAGE (INFRA 2): `~/github/terraform-base/stage/app-layer/stage-infra-2`, `~/github/terraform-base/stage/base-layer/stage-infra-2`
- PROD (BOSTON): `~/github/terraform-base/prod/app-layer/prod`, `~/github/terraform-base/prod/base-layer/prod`
- PROD (HOUSTON): `~/github/terraform-base/prod/app-layer/infra-houston`, `~/github/terraform-base/prod/base-layer/infra-houston`

---

## Helm & Kustomize Repositories

### Infrastructure Components

#### Repository: `dev-flux-releases`

| Environment | Folders |
|-------------|---------|
| **DEV** | `eks_dev2-WAd5LEa6` |
| **STAGE (INFRA)** | `eks_stage-Fn8wxweP` |
| **STAGE (INFRA 2)** | `eks_stage-infra-2-RkULlVMJ` |

**Full paths:**
- DEV: `~/github/dev-flux-releases/eks_dev2-WAd5LEa6`
- STAGE (INFRA): `~/github/dev-flux-releases/eks_stage-Fn8wxweP`
- STAGE (INFRA 2): `~/github/dev-flux-releases/eks_stage-infra-2-RkULlVMJ`

#### Repository: `flux-releases`

| Environment | Folders |
|-------------|---------|
| **PROD (BOSTON)** | `infrastructure-prodi` |
| **PROD (HOUSTON)** | `infrastructure/infra-houston` |

**Full paths:**
- PROD (BOSTON): `~/github/flux-releases/infrastructure-prodi`
- PROD (HOUSTON): `~/github/flux-releases/infrastructure/infra-houston`

---

### Business Applications

#### Repository: `dev-flux-steer`

| Environment | Folders |
|-------------|---------|
| **DEV** | `eks_dev2-WAd5LEa6` |
| **STAGE (INFRA)** | `eks_stage-Fn8wxweP` |
| **STAGE (INFRA 2)** | `eks_stage-infra-2-RkULlVMJ` |

**Full paths:**
- DEV: `~/github/dev-flux-steer/eks_dev2-WAd5LEa6`
- STAGE (INFRA): `~/github/dev-flux-steer/eks_stage-Fn8wxweP`
- STAGE (INFRA 2): `~/github/dev-flux-steer/eks_stage-infra-2-RkULlVMJ`

#### Repository: `flux-releases`

| Environment | Folders |
|-------------|---------|
| **PROD (BOSTON)** | `app/identity-prodi`, `app/infra-1-prodi` |
| **PROD (HOUSTON)** | `app-cluster/infra-houston` |

**Full paths:**
- PROD (BOSTON): `~/github/flux-releases/app/identity-prodi`, `~/github/flux-releases/app/infra-1-prodi`
- PROD (HOUSTON): `~/github/flux-releases/app-cluster/infra-houston`

---

## AWS Configuration & Commands

### AWS Profiles

| Environment | AWS Profile |
|-------------|-------------|
| **PROD** (BOSTON, HOUSTON) | `maprod` |
| **DEV** & **STAGE** (INFRA, INFRA 2) | `maroot` |

### Cluster Discovery & Kubeconfig Setup

Before running Kubernetes commands, discover clusters and update kubeconfig:

```bash
# List EKS clusters (requires AWS profile)
aws eks list-clusters --profile <profile>

# Update kubeconfig for a specific cluster
aws eks update-kubeconfig --name <cluster-name> --profile <profile>
```

### Example Workflow

```bash
# For DEV/STAGE environments
aws eks list-clusters --profile maroot
aws eks update-kubeconfig --name <cluster-name> --profile maroot

# For PROD environments
aws eks list-clusters --profile maprod
aws eks update-kubeconfig --name <cluster-name> --profile maprod
```

---

## Quick Reference

### Environments Summary

| Env Tier | Location | Repositories |
|----------|----------|--------------|
| **DEV** | Single | `terraform-base/terraform-dev2`, `dev-flux-releases/eks_dev2-WAd5LEa6`, `dev-flux-steer/eks_dev2-WAd5LEa6` |
| **STAGE** | Multi (INFRA / INFRA 2) | `terraform-base/stage/*`, `dev-flux-releases/eks_stage-*`, `dev-flux-steer/eks_stage-*` |
| **PROD** | Multi (BOSTON / HOUSTON) | `terraform-base/prod/*`, `flux-releases/*` |

### Key AWS Resources
- IAM (Identity and Access Management)
- S3 (Simple Storage Service)
- EKS (Elastic Kubernetes Service)
- Other AWS infrastructure components

### Deployment Technologies
- Terraform (Infrastructure as Code)
- Kustomize (Kubernetes configuration management)
- Helm (Kubernetes package manager)

### Kubernetes Tools

| Tool | Usage |
|------|-------|
| `kubectl` | Kubernetes CLI for cluster operations |
| `kustomize` | Kubernetes configuration customization |
| `helm` | Kubernetes package manager |

**Note:** Ensure kubeconfig is updated with `aws eks update-kubeconfig` before using these tools.
