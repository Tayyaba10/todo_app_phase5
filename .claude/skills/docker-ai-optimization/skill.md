---
name: docker-ai-optimization
description: Optimize Docker images, containers, and deployments using AI-powered recommendations and automation.
---

# Docker AI Optimization

## Instructions

1. **Image Optimization**
   - Analyze Dockerfile layers for efficiency
   - Reduce image size using minimal base images
   - Remove unnecessary dependencies
   - Cache layers effectively to speed up builds

2. **Container Performance**
   - Monitor CPU, memory, and I/O usage
   - Detect underutilized or overutilized containers
   - Suggest resource limits and requests automatically
   - Recommend container scaling strategies

3. **Deployment Automation**
   - Use AI to recommend container orchestration settings
   - Optimize Docker Compose or Kubernetes manifests
   - Automate updates, rollbacks, and healthchecks
4. **Alerting & Dashboards**
   - Define meaningful alerting thresholds
   - Integrate alerts with Slack, email, or PagerDuty
   - Create dashboards to visualize metrics, logs, and traces
   - Monitor SLA and SLO compliance

## Best Practices
- Use consistent naming conventions for metrics, logs, and traces
- Correlate logs, metrics, and traces for full observability
- Avoid alert fatigue by fine-tuning thresholds
- Ensure observability tools are part of CI/CD
- Document observability setup for team adoption
- Test alerts and dashboards regularly

## Example Structure

### Metrics Collection (Prometheus)
```yaml
scrape_configs:
  - job_name: 'app-metrics'
    static_configs:
      - targets: ['localhost:8000']