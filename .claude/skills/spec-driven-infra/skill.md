---
name: spec-driven-infra
description: Automate infrastructure provisioning and management using specification-driven definitions and templates.
---

# Spec-Driven Infrastructure

## Instructions

1. **Define Infrastructure Specs**
   - Use clear, structured specifications for resources
   - Include compute, network, storage, and security requirements
   - Use YAML/JSON or declarative formats
   - Maintain versioned spec files

2. **Provision Resources**
   - Map specifications to actual cloud or local infrastructure
   - Automate creation using IaC tools (Terraform, Pulumi, CloudFormation)
   - Validate resources against specs
   - Track dependencies and relationships

3. **Manage Infras**
- Apply changes incrementally via spec updates
   - Maintain idempotency for repeatable deployments
   - Rollback changes if provisioning fails
   - Monitor and audit resource states

4. **Integration & Automation**
   - Integrate with CI/CD pipelines for automated provisioning
   - Use specs to generate documentation and diagrams
   - Connect with monitoring and alerting tools
   - Support multi-environment deployments (dev/staging/prod)

## Best Practices
- Keep specifications modular and reusable
- Validate specs before applying changes
- Use version control for all infra specs
- Avoid hardcoding values; use variables and parameters
- Test in isolated environments before production
- Document resource purpose and ownership clearly

## Example Structure

### Infrastructure Spec (YAML)
```yaml
compute:
  - name: web-server
    type: t2.medium
    count: 2
network:
  - name: vpc-main
    cidr: 10.0.0.0/16
storage:
  - name: app-data
    type: ssd
    size_gb: 50
security:
  - group: web-sg
    ingress:
      - protocol: tcp
        port: 80
        source: 0.0.0.0/0