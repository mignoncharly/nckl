# 12 - Acceptance Criteria

## Audit Phase Acceptance

Status: verified when this document set exists.

- Documentation files exist under `docs/audit/` only.
- Findings distinguish verified fact, inference, recommendation, and unknown where relevant.
- Secret values are not reproduced in docs.
- No application source code changed.
- No dependencies installed/removed.
- No migrations, seeds, service restarts, Nginx changes, SSL changes, commits, or pushes performed.

## Isolation Acceptance

Before NCKL deployment:

- `rg -n "saha|SAHA|stl|STL|docufisc|gestionatech|/home/mignon/saha|saha_db|saha_user|stl_db|stl_user"` returns no active runtime references.
- Any remaining references are explicitly legacy documentation or tests that intentionally validate old-to-new migration behavior.
- NCKL uses dedicated `nckl-*` systemd services.
- NCKL uses dedicated database and DB role.
- NCKL uses dedicated Redis config/port/password or explicitly approved isolated Redis DB.
- NCKL static/media/log/backup paths are separate.
- NCKL `.env` contains only NCKL values and is not tracked.
- NCKL Nginx config contains only NCKL domains and NCKL aliases.

## Functional Acceptance

- Public pages show only NCKL brand/content/contact/legal data.
- Services, prices, destinations, pickup zones, and schedules match verified NCKL requirements.
- Request form submits valid data and rejects invalid data.
- Anonymous tracking exposes only approved minimal fields.
- Authenticated customers can see only their own requests.
- Admin/staff can manage requests, services, prices, schedules, loading dates, notifications, and audit logs.
- Non-admin users cannot access admin APIs.
- Email verification and password reset render NCKL-branded messages.
- Push notifications use NCKL VAPID keys and copy.
- Contact form reaches NCKL-owned destination.

## Security Acceptance

- No secrets, `.env`, private keys, database dumps, logs, media, uploads, or customer data are tracked.
- Upload validation includes size, extension, and content/MIME checks.
- Public write/auth endpoints are throttled.
- Public tracking is throttled or otherwise protected from practical enumeration.
- CSP does not reference SAHA and is reviewed before enforcement.
- Production cookies/security headers are configured for NCKL HTTPS.
- Audit logging redacts sensitive values where appropriate.
- Dependency audit is reviewed before launch.

## Test Acceptance

- Backend tests pass with isolated test settings.
- Frontend lint passes.
- Frontend production build succeeds in NCKL context.
- Permission tests cover admin/customer/public boundaries.
- Upload tests cover oversized, wrong extension, and invalid content.
- Form validation tests cover required NCKL fields.
- API tests cover service/pricing/schedule/request/tracking flows.
- Backup and restore test succeeds against disposable NCKL database.
- Smoke tests pass on NCKL staging/production domains.

## Operational Acceptance

- Deployment runbook uses no Docker for production.
- Rollback procedure is documented and tested at least in staging/dry-run form.
- Logs are written to NCKL path and rotated.
- Backups are written to NCKL path and protected.
- Health checks are defined.
- Monitoring/log review procedure exists.
- SAHA services/domains/databases remain untouched throughout.


## Image-Derived Business Acceptance

Before implementation is accepted:

- The app displays `NCKL Logistics Services` branding and no SAHA/STL public identity.
- Public content includes only owner-approved NCKL services visible in the images or later supplied text.
- Germany/Cameroon/Europe route wording matches the owner's final decision on transit times.
- No price, fee, commission, insurance, customs, or payment claim is displayed unless owner-confirmed.
- Drop-off location content matches owner-confirmed Bamenda, Douala, Berlin, and Leipzig details.
- Contact numbers are reconciled so the shorter/conflicting Image 1 Cameroon number is not published unless confirmed.
- Accepted item categories are represented accurately, including dry/frozen food, clothes, jewelries/bijoux, bags, shoes, cosmetics, hair extensions, dry herbs, documents, phones without battery, and small household equipment.
- Route/item conditions are visible and/or enforced where required: phones without battery, Germany-to-Cameroon-only scope if confirmed, and small household equipment max 31 kg if confirmed.
- Shopping assistance from Europe to Cameroon is either implemented as a structured request flow or intentionally handled as WhatsApp-only, based on owner decision.
- English/French/German language support matches the owner-approved launch scope.
- TikTok `@nckllogisticsservices` is included only if approved as an official social link.

## Implementation update - 2026-07-10

Implemented NCKL runtime decoupling, centralized configuration, configurable routes/items/locations/schedules, customer request workflow fields, admin-protected APIs, upload validation, NCKL branding/content updates, deployment templates, and local regression checks. See `docs/implementation/README.md` for current implementation status.
