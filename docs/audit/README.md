# NCKL Audit README

## What Was Inspected

Verified fact: this planning run inspected the `/home/mignon/nckl` repository, including backend Django apps, frontend Next.js app, environment templates, deployment templates, scripts, docs, git status/history, ignored artifact inventory, route structure, key settings, models, serializers, views, permissions, throttles, and source-client references.

Image limitation: `docs/nckl_1.jpeg` through `docs/nckl_7.jpeg` are present but could not be visually/OCR inspected because image processing was blocked by the sandbox. NCKL-specific requirements from those images remain open.

## Identified Stack

- Backend: Django 5.2.15, Django REST Framework 3.16.1, PostgreSQL, Redis, Celery, Gunicorn.
- Frontend: Next.js 14.2.5 App Router, React 18, TypeScript, Tailwind CSS.
- Forms: `react-hook-form` and `zod`.
- Notifications: Django email, Celery tasks, web push through VAPID/`pywebpush`, in-app notifications.
- i18n: French and German in backend gettext and frontend dictionary.
- Production pattern: Nginx reverse proxy to systemd-managed backend/frontend/worker/beat/Redis services.

## Main Risks

- Critical: copied ignored secrets, Redis config, `.env`, frontend env, SQL backups, and media artifacts exist locally.
- Critical: deployment templates still target SAHA paths, domains, service names, ports, database names, and Redis config.
- High: frontend/backend/email content still contains SAHA/STL branding and source-client contact details.
- High: service/pricing/destination/schedule seed data is source-client specific.
- High: NCKL requirements from supplied images are not yet extractable in this environment.
- Medium: token storage uses browser `localStorage`; upload validation needs MIME/content checks.

## Recommended Approach

Reuse the proven architecture and domain logic, but first isolate and decouple:

1. Make repository safety and ignored artifact handling explicit.
2. Centralize NCKL-specific configuration without building a multi-tenant platform.
3. Replace SAHA/STL content, seed data, references, email templates, icons, and deployment names.
4. Preserve request/customer/admin/notification/audit workflows where they match NCKL requirements.
5. Use a dedicated NCKL database, role, secrets, ports, services, Nginx config, static/media/log/backup paths.
6. Do not deploy or migrate until requirements, secrets, domain, and infrastructure naming are confirmed.

## Implementation Phases

- Phase A: Repository and safety baseline.
- Phase B: Decouple source-client configuration.
- Phase C: NCKL requirements and branding.
- Phase D: Business workflows.
- Phase E: Backend and database hardening.
- Phase F: Frontend quality.
- Phase G: Infrastructure preparation.
- Phase H: Testing and acceptance.
- Phase I: Controlled deployment.

## Blocking Questions

- What are the NCKL frontend and API domains?
- What are NCKL's verified contact details, legal identity, and privacy/imprint text?
- What services, prices, pickup areas, destinations, and workflows should NCKL support?
- Should the app remain French/German only?
- Does the Cameroon-specific status/data model remain valid?
- Is online payment required?
- Can the NCKL JPEGs be supplied as text or inspected through an approved viewer/OCR path?

## Audit Documents

1. [01-current-architecture.md](01-current-architecture.md)
2. [02-source-client-reference-audit.md](02-source-client-reference-audit.md)
3. [03-security-review.md](03-security-review.md)
4. [04-reuse-adaptation-matrix.md](04-reuse-adaptation-matrix.md)
5. [05-nckl-requirements.md](05-nckl-requirements.md)
6. [06-isolation-and-deployment-architecture.md](06-isolation-and-deployment-architecture.md)
7. [07-database-isolation-plan.md](07-database-isolation-plan.md)
8. [08-phased-implementation-plan.md](08-phased-implementation-plan.md)
9. [09-file-by-file-roadmap.md](09-file-by-file-roadmap.md)
10. [10-open-questions-and-decisions.md](10-open-questions-and-decisions.md)
11. [11-risk-register.md](11-risk-register.md)
12. [12-acceptance-criteria.md](12-acceptance-criteria.md)

## Implementation update - 2026-07-10

Implemented NCKL runtime decoupling, centralized configuration, configurable routes/items/locations/schedules, customer request workflow fields, admin-protected APIs, upload validation, NCKL branding/content updates, deployment templates, and local regression checks. See `docs/implementation/README.md` for current implementation status.
