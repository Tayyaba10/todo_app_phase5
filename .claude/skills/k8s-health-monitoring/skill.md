---
name: k8s-health-monitoring
description: Monitor Kubernetes clusters and applications to track health, performance, and resource usage.
---

# Kubernetes Health Monitoring

## Instructions

1. **Cluster Monitoring**
   - Monitor node status and resource usage (CPU, memory, disk)
   - Track pod health and readiness/liveness probes
   - Identify pending or failed pods
   - Watch for resource bottlenecks

2. **Application Monitoring**
   - Check container status and logs
   - Track service availability and latency
   - Collect metrics from deployed applications
   - Set up alerts for failures or anomalies

3. **Logging & Metrics**
   - Aggregate logs using tools like Fluentd, Loki, or ELK
   - Collect metrics using Prometheus and Grafana
   - Visualize cluster and application health dashboards
   - Maintain historical metrics for trend analysis

4. **Alerting & Remediation**
   - Configure alerts for node/pod failures, high resource usage
   - Auto-scale deployments when needed
   - Trigger automated remediation scripts if available
   - Integrate with Slack, email, or monitoring platforms

## Best Practices
- Use liveness and readiness probes for all critical pods
- Monitor
- Use liveness and readiness probes for all critical pods
- Monitor resource quotas and limits
- Keep dashboards simple and actionable
- Alert only on meaningful thresholds to avoid noise
- Document monitoring setup and alert policies
- Test alerts and remediation procedures regularly

## Example Structure

### Monitor Pods
```bash
kubectl get pods -A
kubectl describe pod <pod-name>
kubectl logs <pod-name>