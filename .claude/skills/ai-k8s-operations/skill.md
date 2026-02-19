---
name: ai-k8s-operations
description: Automate Kubernetes cluster management and application operations using AI-powered tools and agents.
---

# AI Kubernetes Operations

## Instructions

1. **Cluster Management**
   - Monitor cluster health and resource usage
   - Scale nodes automatically based on load
   - Apply updates and patches safely
   - Detect and resolve pod failures

2. **Deployment Automation**
   - Deploy applications using AI-assisted Helm or YAML templates
   - Optimize deployment strategies (rolling, canary, blue-green)
   - Auto-update services based on AI recommendations
   - Predict potential bottlenecks or failures

3. **Monitoring & Logging**
   - Collect logs and metrics from pods, services, and nodes
   - Analyze patterns using AI models
   - Generate alerts for anomalies or performance degradation
   - Visualize cluster and application health

4. **Optimization & Remediation**
   - Recommend resource limits and requests
   - Suggest configuration improvements
   - Automatically restart or reschedule unhealthy pods
   - Identify and remove unused resources

## Best Practices
- Use namespaces for isolation and organization
- Keep Helm charts and manifests version-controlled
- Test AI-driven changes in a local or staging environment first
- Maintain security and RBAC policies
- Use AI suggestions, but verify critical changes manually
- Document AI-assisted operations and workflows

## Example Structure

### AI-Driven Pod Scaling
```python
from k8s_ai_agent import ClusterAgent

agent = ClusterAgent(cluster_context="minikube")
agent.monitor_resources()
agent.autoscale_pods(deployment="my-app", target_cpu=50)
