# 07 - Database Isolation Plan

## Reuse Decision

Status: recommendation.

The copied schema can be reused as a baseline because it models generic logistics concepts: users, customers, service types, destinations, prices, schedules, transport requests, request photos, status history, comments, notifications, and audit logs.

The copied data must not be reused unless explicitly confirmed as generic and non-sensitive. NCKL must start with an empty customer/request/media/notification/audit dataset and NCKL-specific reference data.

## Required Isolation

| Item | NCKL requirement |
| --- | --- |
| Database | Dedicated PostgreSQL database, proposed name `nckl_db` |
| Role | Dedicated role, proposed name `nckl_user` |
| Password | New generated secret, never committed |
| Connection string | NCKL-only `DATABASE_URL` |
| Schema | Not shared with SAHA |
| Migrations | Run only against NCKL database after backup and approval |
| Dumps | NCKL-only backup files; no SAHA dumps in NCKL release process |

## Tables That Must Start Empty

Status: recommendation.

| Model/table area | Reason |
| --- | --- |
| `accounts.User` except approved NCKL admin bootstrap | Users are personal/security data |
| `customers.Customer` | Customer PII |
| `logistics.TransportRequest` | Customer shipment data |
| `logistics.TransportRequestPhoto` | Uploaded customer images/files |
| `logistics.RequestStatusEvent` | Operational/customer history |
| `logistics.RequestComment` | Operational/customer notes |
| `notifications.PushSubscription` | Device endpoints and keys |
| `notifications.CustomerNotification` | Customer-specific data |
| `notifications.NotificationPreference` | Customer preference data |
| `notifications.NotificationLog` | Operational history tied to old campaigns |
| `audit.AuditLog` | Old actor/entity metadata |
| Celery result/beat tables | Runtime state; recreate clean |

## Reference Data To Recreate

Status: recommendation.

| Data | Current source | NCKL treatment |
| --- | --- | --- |
| Services | `backend/apps/services/seed_data.py` | Replace with NCKL services after requirements extraction |
| Prices | `backend/apps/pricing/seed_data.py` | Replace with NCKL prices/rules only when confirmed |
| Destinations | `backend/apps/destinations/seed_data.py` | Replace with NCKL destinations |
| Pickup regions/schedules | `backend/apps/schedules/seed_data.py` | Replace with NCKL pickup zones and dates |
| Admin account | `deploy/root_setup.sh`, `scripts/create_admin.py` | Replace with secure env-driven NCKL bootstrap |

## Schema Changes To Consider

Status: recommendation.

| Area | Current issue | Proposed change | Risk |
| --- | --- | --- | --- |
| Reference codes | `STL-YYYY-NNNNNN` prefix | Configurable or NCKL prefix | Medium |
| Status values | `arrived_cameroon` | Rename to generic destination status if NCKL is not Cameroon-specific | High, requires migration and frontend updates |
| Destination default | `country='Cameroun'` | Remove default or configure NCKL default | Medium |
| Pickup region default | `country='Allemagne'` | Remove default or configure NCKL default | Medium |
| Upload validation | Extension/size only | Add MIME/Pillow verification and filename hardening | Medium |
| Customer phone | No unique normalized constraint | Consider normalized phone field/index if matching reliability matters | Medium |
| Monetary fields | Decimal with currency on price rules; request prices no currency field | Confirm NCKL currency and add request currency if needed | Medium |
| Audit logs | Generic JSON metadata | Redact PII and define retention | Medium |
| Data retention | Photo purge and optional customer anonymization | Confirm retention days and GDPR policy | Medium |

## Indexes and Constraints

Status: verified fact + recommendation.

Existing visible constraints include unique `User.email`, unique `TransportRequest.reference_code`, unique `LoadingDate.date`, and unique `PushSubscription.endpoint`. Price rules include active/validity filtering but no unique rule constraint.

Potential NCKL additions:

| Addition | Purpose |
| --- | --- |
| Index `TransportRequest(status, created_at)` | Admin filters/dashboard |
| Index `TransportRequest(pickup_city)` | Admin filters/reporting |
| Index `RequestStatusEvent(request, created_at)` | History reads |
| Index `AuditLog(created_at, action, entity_type)` | Audit filtering |
| Optional normalized phone field/index | Customer matching reliability |
| Optional price validity constraint | Prevent invalid date windows |

## Migration Strategy

Recommendation.

1. Keep existing migrations as baseline history.
2. Create new NCKL migrations only for actual schema changes.
3. Review each migration before applying.
4. Run migrations only against an isolated NCKL database.
5. Back up NCKL database before every migration once deployed.
6. Never point `DATABASE_URL` at SAHA.

## Seed Strategy

Recommendation.

Create a NCKL seed command or fixtures that are:

- idempotent,
- NCKL-specific,
- free of customer data,
- environment-safe,
- easy to run in staging and production,
- documented with source requirements.

Do not run existing SAHA seed data for NCKL.

## Backup and Restore Strategy

Recommendation.

Use no-Docker PostgreSQL commands in NCKL deployment docs:

- `pg_dump` of `nckl_db` only.
- Restricted backup directory permissions.
- Retention policy.
- Periodic restore test into a disposable NCKL test database.
- No secrets in backup filenames or logs.

Existing `scripts/backup_db.sh` and `scripts/restore_db.sh` are not suitable because they use Docker and STL DB names.

## Data Retention

Status: verified fact + recommendation.

Current retention code can purge photos on terminal requests older than `DATA_RETENTION_DAYS` and optionally anonymize customers. Defaults are 365 days and customer anonymization disabled.

NCKL must confirm:

- retention period,
- whether anonymization is required,
- legal basis,
- user deletion process,
- backup retention,
- audit log retention.

