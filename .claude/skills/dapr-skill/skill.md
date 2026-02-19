---
name: dapr-skill
description: Build distributed applications using Dapr with Pub/Sub messaging, state management, bindings, secrets management, and service invocation.
---

# Dapr Skill

## Instructions

1. **Pub/Sub Messaging**
   - Configure pub/sub components (Kafka, Redis, etc.)
   - Publish events to topics
   - Subscribe to topics via Dapr sidecar
   - Handle message retries and delivery guarantees

2. **State Management**
   - Configure state store components (Redis, PostgreSQL, etc.)
   - Save and retrieve application state
   - Use key-value pattern for task storage
   - Enable state versioning and concurrency control

3. **Bindings (Cron & External Systems)**
   - Configure input/output bindings
   - Use cron binding for scheduled tasks
   - Trigger workflows from external services
   - Handle binding events inside application routes

4. **Secrets Management**
   - Configure secret store (Kubernetes, Vault, etc.)
   - Retrieve secrets securely via Dapr API
   - Avoid hardcoding credentials
   - Rotate secrets without app redeployment

5. **Service Invocation**
   - Invoke other microservices via Dapr
   - Use service discovery automatically
   - Handle timeouts and retries
   - Secure communication between services

## Best Practices
- Keep Dapr components modular and reusable
- Use sidecar pattern consistently
- Separate environment configurations (dev/staging/prod)
- Avoid direct service coupling
- Secure all pub/sub and secret stores
- Monitor Dapr sidecar logs

## Example Structure

### Pub/Sub Publish
```python
requests.post(
    "http://localhost:3500/v1.0/publish/pubsub/task-events",
    json={"event": "task_created", "task_id": 123}
)
