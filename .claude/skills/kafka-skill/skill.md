---
name: kafka-skill
description: Implement event-driven architecture using Kafka with topic management, producers, consumers, and cloud integration.
---

# Kafka Skill

## Instructions

1. **Topic Management**
   - Create topics for different event types
   - Use clear naming conventions (task-events, reminders, task-updates)
   - Define partition count based on expected load
   - Configure retention and replication settings

2. **Producer Implementation**
   - Publish events to appropriate topics
   - Serialize messages using JSON or Avro
   - Include event metadata (timestamp, event type, source)
   - Ensure idempotent message production

3. **Consumer Implementation**
   - Subscribe to relevant topics
   - Process messages reliably
   - Commit offsets after successful processing
   - Handle consumer groups for scalability

4. **Cloud Integration**
   - Connect to Confluent or Redpanda Cloud clusters
   - Configure secure authentication (API keys, SASL, TLS)
   - Manage topics and consumers remotely
   - Monitor cloud metrics and throughput

5. **Event Schema Design**
   - Define consistent message structure
   - Include versioning in schema
   - Validate messages before publishing
   - Maintain schema documentation

6. **Retry & Error Handling**
   - Implement retry logic for failed messages
   - Use dead-letter topics for unprocessable events
   - Log errors for debugging
   - Monitor failed message rates

## Best Practices
- Use separate topics for different event domains
- Keep messages small and focused
- Version event schemas for compatibility
- Avoid tight coupling between producers and consumers
- Monitor consumer lag regularly
- Test retry and failure scenarios

## Example Structure

### Topic Creation
```bash
kafka-topics --create \
  --topic task-events \
  --partitions 3 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
