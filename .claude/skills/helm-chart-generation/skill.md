---
name: helm-chart-generation
description: Create and manage Helm charts for Kubernetes applications, including templates, values, and deployments.
---

# Helm Chart Generation

## Instructions

1. **Chart Initialization**
   - Use `helm create <chart-name>` to scaffold a new chart
   - Organize templates and values.yaml
   - Set metadata in Chart.yaml (name, version, description)
   - Maintain chart directory structure

2. **Template Management**
   - Create Deployment, Service, ConfigMap, Secret templates
   - Use Helm template syntax (`{{ .Values.key }}`)
   - Manage conditional resources with `if` statements
   - Use loops for multiple resources

3. **Values & Configuration**
   - Define default values in `values.yaml`
   - Override values per environment using `--values` or `--set`
   - Separate environment-specific configurations
   - Validate values before deployment

4. **Deployment & Updates**
   - Install chart with `helm install`
   - Upgrade existing releases with `helm upgrade`
   - Rollback to previous versions if needed
   - Use `helm template` for local testing

## Best Practices
- Keep templates reusable and modular
- Version charts properly
- Use descriptive names and labels
- Avoid hardcoding values; rely on `values.yaml`
- Document chart usage and values
- Test charts in local Minikube or kind cluster

## Example Structure

### Chart.yaml
```yaml
apiVersion: v2
name: my-app
description: A Helm chart for Kubernetes deployment
version: 0.1.0
appVersion: "1.0.0"
