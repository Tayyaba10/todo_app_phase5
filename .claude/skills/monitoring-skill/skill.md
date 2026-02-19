---
name: monitoring-skill
description: Implement observability using Prometheus metrics, Grafana dashboards, centralized logging, distributed tracing, and alerting systems.
---

# Monitoring Skill

## Instructions

1. **Prometheus Metrics**
   - Expose application metrics using `/metrics` endpoint
   - Instrument services with Prometheus client libraries
   - Configure Prometheus scrape targets
   - Use labels for service, environment, and version
   - Monitor CPU, memory, latency, error rates, and request throughput

2. **Grafana Dashboards**
   - Connect Grafana to Prometheus data source
   - Create dashboards for system and application metrics
   - Visualize latency (P95/P99), error rates, and traffic
   - Build environment-specific dashboards (dev/staging/prod)
   - Share dashboards across teams

3. **Centralized Logging**
   - Collect logs from all services and containers
   - Use structured logging (JSON format)
   - Aggregate logs into a centralized system (e.g., ELK stack)
   - Enable log filtering and correlation with trace IDs
   - Retain logs based on environment policy

4. **Distributed Tracing**
   - Instrument services with OpenTelemetry
   - Propagate trace context between services
   - Visualize traces in tracing backend (Jaeger/Tempo)
   - Monitor request flow across microservices
   - Detect bottlenecks and latency spikes

5. **Alerting System**
   - Define alert rules in Prometheus
   - Configure Alertmanager for routing
   - Set threshold-based and anomaly-based alerts
   - Send alerts to Slack, Email, or PagerDuty
   - Avoid alert fatigue with proper severity levels

## Best Practices
- Monitor the “Golden Signals”: latency, traffic, errors, saturation
- Use consistent metric naming conventions
- Correlate metrics, logs, and traces
- Separate alerts by severity (info, warning, critical)
- Regularly test alert rules
- Use dashboards tailored to stakeholders (DevOps, developers, management)

## Example Structure

### Prometheus Scrape Config
```yaml
scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['my-app:8080']
