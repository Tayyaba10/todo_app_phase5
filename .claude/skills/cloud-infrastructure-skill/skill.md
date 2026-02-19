---
name: cloud-infrastructure-skill
description: Design and manage cloud infrastructure across AKS (Azure), GKE (Google Cloud), OKE (Oracle Cloud), including networking, IAM, and persistent storage.
---

# Cloud Infrastructure Skill

## Instructions

1. **Managed Kubernetes Clusters**
   - Deploy clusters on AKS (Azure Kubernetes Service)
   - Deploy clusters on GKE (Google Kubernetes Engine)
   - Deploy clusters on OKE (Oracle Kubernetes Engine)
   - Configure node pools and autoscaling
   - Secure cluster access using role-based access control (RBAC)

2. **Cloud Networking**
   - Configure Virtual Networks (VNet / VPC)
   - Create subnets for public and private workloads
   - Set up load balancers and ingress controllers
   - Configure firewall rules and security groups
   - Enable private cluster endpoints when required

3. **Identity & Access Management (IAM)**
   - Define roles and permissions
   - Use service accounts for workloads
   - Apply least-privilege access policies
   - Integrate with cloud-native identity systems
   - Manage API keys and credentials securely

4. **Persistent Storage**
   - Configure Persistent Volumes (PV) and Persistent Volume Claims (PVC)
   - Use managed cloud storage (Azure Disk, GCP Persistent Disk, OCI Block Volume)
   - Set storage classes for performance tiers
   - Enable backups and snapshot policies
   - Handle stateful workloads securely

## Best Practices
- Separate dev, staging, and production environments
- Use Infrastructure as Code (Terraform / Pulumi)
- Enable monitoring and logging by default
- Apply network segmentation for security
- Use managed storage for reliability
- Rotate credentials regularly
- Enable encryption at rest and in transit

## Example Structure

### AKS Cluster Creation
```bash
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys
