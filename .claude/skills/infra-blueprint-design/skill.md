---
name: infra-blueprint-design
description: Design reusable infrastructure blueprints for cloud and local deployments, including architecture, resources, and best practices.
---

# Infrastructure Blueprint Design

## Instructions

1. **Define Architecture**
   - Identify core components (compute, storage, network, security)
   - Map interactions between components
   - Include redundancy and failover mechanisms
   - Consider scalability and performance requirements

2. **Create Blueprint Templates**
   - Use diagrams or structured spec files (YAML/JSON)
   - Include environment-specific variables (dev/staging/prod)
   - Define standard configurations and resource types
   - Make templates reusable across projects

3. **Resource Planning**
   - Specify compute resources, storage, and network setup
   - Define security groups, firewalls, and access policies
   - Include monitoring, logging, and alerting resources
   - Estimate cost and optimize resource usage

4. **Versioning & Documentation**
   - Version blueprints for iterative improvements
   - Document resource relationships and dependencies
   - Track changes and maintain audit logs
   - Align blueprint with CI/CD and IaC workflows

## Best Practices
- Keep blueprints modular and reusable
- Follow cloud provider best practices
- Separate environment-specific configs
- Use visual diagrams to clarify architecture
- Validate blueprint against real deployments
- Maintain clear documentation for team adoption

## Example Structure

### Blueprint Spec (YAML)
```yaml
compute:
  - name: app-server
    type: t3.medium
    replicas: 3
network:
  - name: vpc-main
    cidr: 10.0.0.0/16
  - name: subnet-public
    cidr: 10.0.1.0/24
storage:
  - name: app-data
    type: ssd
    size_gb: 100
security:
  - group: web-sg
    ingress:
      - protocol: tcp
        port: 80
        source: 0.0.0.0/0
monitoring:
  - type: prometheus
    retention_days: 15