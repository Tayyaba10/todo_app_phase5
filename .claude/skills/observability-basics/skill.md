---
name: observability-basics
description: Implement observability in applications and infrastructure to monitor, trace, and debug effectively.
---

# Observability Basics

## Instructions

1. **Metrics Collection**
   - Collect system and application metrics (CPU, memory, requests)
   - Use tools like Prometheus, StatsD, or Cloud Monitoring
   - Define key performance indicators (KPIs)
   - Store metrics for trend analysis

2. **Logging**
   - Centralize logs from all services and components
   - Use structured logging (JSON) for easier parsing
   - Aggregate logs with Fluentd, Logstash, or Loki
   - Index and search logs efficiently

3. **Tracing**
   - Track requests across distributed systems
   - Use tools like OpenTelemetry, Jaeger, or Zipkin
   - Measure latency and identify bottlenecks
   - Connect traces to logs and metrics for full c
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