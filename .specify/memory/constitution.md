<!-- SYNC IMPACT REPORT:
Version change: 5.0.0 -> 5.0.1
Modified principles: None (minor version bump for date amendment)
Added sections: None
Removed sections: None
Templates requiring updates:
- ⚠ .specify/templates/plan-template.md (Needs review for Constitution Check alignment)
- ⚠ .specify/templates/spec-template.md (Needs review for Requirements alignment)
- ⚠ .specify/templates/tasks-template.md (Needs review for task categorization alignment)
- ⚠ README.md (Needs update to reflect Phase V)
Follow-up TODOs: Update Agent & Skills Constitution and Operating Rules to reflect Phase V.
-->
# Phase V Todo Chatbot Constitution

## 1️⃣ Project Purpose
Upgrade the Todo Chatbot to a **cloud-native, event-driven system** with advanced task features, Dapr integration, Kafka messaging, and deployment to managed Kubernetes (AKS, GKE, or OKE).
---
## 2️⃣ Governance Principles
1.  **Spec-Driven Workflow:** Follow: **spec → plan → tasks → implementation**. No manual coding outside this flow.
2.  **Microservices Architecture:** Separate services (Chat API, Recurring Task Service, Notification Service, Audit Service, Realtime/WebSocket Service) must be independently deployable.
3.  **Event-Driven System:** Use **Kafka** for all task-related events, including `task-events`, `reminders`, and `task-updates` topics.
4.  **Dapr Integration:** All services must use Dapr for Pub/Sub (Kafka), State management, Service invocation, Secrets, and Cron bindings.
5.  **Cloud-Native Deployment:** Run locally on **Minikube** and deploy to **AKS, GKE, or Oracle OKE** using **Helm charts** for deployments.
6.  **CI/CD Automation:** Implement GitHub Actions pipeline for Build, Test, Containerize, and Deploy via Helm.
7.  **Observability:** Implement Monitoring with Prometheus and Dashboards.
---
## 3️⃣ Agents & Responsibilities
| Agent | Responsibilities | Skills |
|-------|-----------------|--------|
| **DevOps Agent** | Kubernetes management, deployment orchestration | `k8s-local-deployment`, `helm-chart-generation`, `ai-k8s-operations` |
| **Docker Agent** | Containerization, Docker AI optimization | `containerize-frontend-backend`, `docker-ai-optimization`, `local-docker-testing` |
| **Infrastructure Agent** | Spec-driven automation, blueprint creation | `spec-driven-infra`, `infra-blueprint-design` |
| **Monitoring Agent** | Observability, logging, health checks | `k8s-health-monitoring`, `observability-basics` |
---
## 4️⃣ Skills Constitution
1. **`k8s-local-deployment`** — Deploy frontend/backend to Minikube, manage replicas & services.
2. **`helm-chart-generation`** — Generate reusable Helm charts, configure `values.yaml`, support rollbacks.
3. **`ai-k8s-operations`** — Pod failure diagnosis, scaling recommendations, service exposure.
4. **`containerize-frontend-backend`** — Generate Dockerfiles for frontend/backend, production-ready multi-stage builds.
5. **`docker-ai-optimization`** — Optimize image size & caching, apply security best practices.
6. **`local-docker-testing`** — Validate containers before Kubernetes deployment.
7. **`spec-driven-infra`** — Translate spec to deployment blueprint, Claude Code powered execution.
8. **`infra-blueprint-design`** — Create reusable Kubernetes + Helm templates, enforce spec compliance.
9. **`k8s-health-monitoring`** — Pod readiness & liveness checks, node resource usage.
10. **`observability-basics`** — Log collection, error tracking, metrics reporting.
---
## 5️⃣ Operating Rules
1. **Skill Execution Rule:** Tasks must execute via AI agent using its designated skill. Manual CLI only as fallback.
2. **Spec Compliance Rule:** Deployments must match spec definitions; specs are versioned & auditable.
3. **Error Handling Rule:** AI agents log and report all errors; monitoring agent reviews post-deployment health.
4. **Secrets Handling Rule:** Secrets must never be committed to Git; use `.env` at runtime and `.env.example` placeholder.
5. **Reproducibility Rule:** All Helm charts, Docker images, and blueprints must be portable for local deployment.
---
## 6️⃣ Governance Enforcement
- **Agent Hierarchy:**
  - DevOps & Docker agents execute deployments
  - Infrastructure agent validates specs & blueprints
  - Monitoring agent ensures cluster stability

- **Audit:** Every skill execution logged; errors trigger automated alerts.
- **AI-Assisted Automation:** kubectl-ai, kagent, Gordon AI enforce zero-manual deployment.

---
## 7️⃣ Progressive Learning Principle
Every deployment iteration captures:
- AI decisions & prompts
- Spec changes & blueprint updates
- Metrics from monitoring agent

Ensures **continuous learning** and **infrastructure reliability**.

**Version**: 5.0.1 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-02-17

---
## Required Features
- Priorities, tags, search, filter, sort
- Due dates and reminders
- Recurring tasks
- Event-driven notifications
---
## Definition of Done
- Runs on Minikube with Dapr and Kafka
- Deployed to cloud Kubernetes
- CI/CD working
- Monitoring enabled
- All services communicate via events
