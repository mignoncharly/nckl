# 02 - Source-Client Reference Audit

## Scope and Method

Status: verified fact.

Searches were run inside `/home/mignon/nckl` using targeted `rg -n` queries for SAHA/STL names, domains, emails, phone numbers, DB names/users, filesystem paths, service names, ports, seed data, destination/service terms, and secret/config identifiers. Vendor/build/runtime directories were excluded from the main code search where noted, but ignored artifacts were separately inventoried with `git status --ignored`, `find`, and targeted searches.

Do not copy any secret values from local runtime files into docs or commits. This audit reports variable names, paths, and risks only.

## Critical Findings

| Severity | Classification | Finding | Evidence | Action |
| --- | --- | --- | --- | --- |
| Critical | Security-sensitive | Ignored `.env` exists in checkout with runtime variables. | `git status --ignored`; variable names redacted via `awk` | Do not stage. Create NCKL-only `.env.example`; rotate any value copied from SAHA. |
| Critical | Security-sensitive | Ignored `deploy/.secrets.json` exists. | `git status --ignored`, `find` | Do not stage. Replace with NCKL-specific secret provisioning process; rotate copied values. |
| Critical | Security-sensitive / must be removed | Ignored `deploy/redis-saha.conf` exists and includes a `requirepass` line plus SAHA paths. | `deploy/redis-saha.conf:5` value intentionally not reproduced; paths at lines 6-7 | Do not reuse. Create `nckl` Redis config later with new secret and paths. |
| Critical | Production-data risk | Ignored `backups/` contains SQL dumps and secret/runtime backups. | `find backups -maxdepth 3 -type f` | Never stage. Determine whether they are SAHA data; purge from NCKL workspace only after explicit approval. |
| Critical | Production-data risk | Ignored `backend/media/` and `backend/test_media/` contain request photo files. | `find backend/media backend/test_media` | Treat as copied/customer-test artifacts until proven otherwise. Never stage or deploy as NCKL seed media. |
| High | Must be renamed | systemd service files use `saha-*` names and `/home/mignon/saha` paths. | `deploy/systemd/saha-api.service`, `saha-worker`, `saha-beat`, `saha-frontend`, `saha-redis` | Replace with `nckl-*` units before deployment. |
| High | Must be replaced | Nginx configs point to SAHA domains, logs, media/static paths, and ports. | `deploy/nginx/*` | Create NCKL server blocks only after domain/ports are confirmed. |
| High | Must become configurable | Frontend CSP allows only `https://api-saha.docufisc.de` in report-only connect source. | `frontend/next.config.js:13` | Move API origin into NCKL config and remove SAHA domain. |
| High | Must be replaced | Email sender/support identities default to `STL <info@gestionatech.de>` and `info@gestionatech.de`. | `backend/config/settings/base.py:172,177`, `production.py:22`, frontend contact/footer | Replace with NCKL sender/support values. |
| High | Must be renamed | Generated reference code prefix is `STL-YYYY-NNNNNN`. | `backend/apps/logistics/reference.py:11,21` | Change to confirmed NCKL prefix, update tests and UI examples. |

## Client-Specific Content and Branding

| Classification | Finding | Evidence | Recommended action |
| --- | --- | --- | --- |
| Must be replaced | README and existing docs describe SAHA, SAHA domains, SAHA deployment, and SAHA release process. | `README.md`, `docs/*.md`, `AGENTS.md` | Keep historical docs only if marked legacy; create NCKL docs for real operations. |
| Must be replaced | Public metadata title/description says SAHA and Cameroon route. | `frontend/src/app/layout.tsx:19-20` | Replace after NCKL brand/domain/services are confirmed. |
| Must be replaced | PWA manifest uses `SAHA Transport & Logistics` and `STL`. | `frontend/src/app/manifest.webmanifest/route.ts:10-12` | Replace app name, short name, description, theme colors, icons. |
| Must be replaced | Logo/icon SVGs contain `STL`. | `frontend/src/app/icon.svg`, `frontend/public/icons/icon.svg` | Replace with NCKL logo assets. |
| Must be replaced | Offline page says `STL` and SAHA copy. | `frontend/public/offline.html:7,53,56-57` | Replace with NCKL offline copy. |
| Must be replaced | Navbar, footer, auth card, admin sidebar display `STL` or `SAHA Transport & Logistics`. | `frontend/src/components/layout/AppNavbar.tsx:30`, `Footer.tsx`, `AuthCard.tsx`, `AdminSidebar.tsx` | Replace with centralized brand values. |
| Must be replaced | Email templates are branded SAHA/STL and hardcode support email/WhatsApp. | `backend/apps/notifications/emails.py:1,20-21,56,89-100,111-162` | Move brand/contact values to settings and rewrite copy. |
| Must be replaced | Contact page and footer hardcode `info@gestionatech.de`. | `frontend/src/app/contact/page.tsx:62,70`, `Footer.tsx:78,81` | Replace with NCKL contact email. |
| Must be replaced | WhatsApp fallback number is hardcoded. | `frontend/src/lib/constants.ts:2`, `.env.example:61`, `backend/apps/notifications/emails.py:20` | Use NCKL number from env/config. |
| Must be replaced | Frontend i18n dictionary contains many SAHA/STL strings. | `frontend/src/lib/i18n-config.ts` multiple lines | Rewrite bilingual copy from NCKL requirements. |
| Must be replaced | Backend gettext catalogs contain SAHA/STL email strings. | `backend/locale/fr/LC_MESSAGES/django.po`, `backend/locale/de/LC_MESSAGES/django.po` | Regenerate/update translations after replacing source strings. |

## Service, Route, Price, and Workflow Coupling

| Classification | Finding | Evidence | Recommended action |
| --- | --- | --- | --- |
| Must be replaced | Destination defaults and statuses assume Cameroon. | `backend/apps/destinations/models.py`, `backend/apps/logistics/models.py`, `backend/apps/logistics/status.py` | Confirm NCKL geography; rename `arrived_cameroon` if not applicable. |
| Must be replaced | Seed destinations are Douala, Yaounde, Bafoussam. | `backend/apps/destinations/seed_data.py` | Replace seed data with NCKL destinations. |
| Must be replaced | Service seed data: parcels, 200L barrels, volume, loaded car, other. | `backend/apps/services/seed_data.py` | Replace with NCKL services only if confirmed. |
| Must be replaced | Price seed data includes SAHA-specific prices. | `backend/apps/pricing/seed_data.py` | Do not load into NCKL unless NCKL confirms same offers/prices. |
| Must be replaced | Schedule seed data includes Germany/France/Luxembourg pickup regions and July 2026 dates. | `backend/apps/schedules/seed_data.py` | Replace with NCKL pickup coverage and real dates. |
| Must become configurable | Static frontend pickup and delivery city arrays are client-specific. | `frontend/src/lib/constants.ts:8-31` | Use backend-managed records or a centralized NCKL config. |
| Must be renamed | Status code `arrived_cameroon` encodes source destination. | `backend/apps/logistics/models.py`, `status.py`, frontend status components | Rename through migration only if NCKL destination is not Cameroon. |
| Requires owner clarification | Payment fields exist but online payment is not implemented. | `TransportRequest.payment_status`, `amount_paid`, `payment_note`; docs mention no online payment | Confirm NCKL payment workflow before exposing claims. |

## Infrastructure Coupling

| Classification | Finding | Evidence | Recommended action |
| --- | --- | --- | --- |
| Must be renamed | Docker container names use `stl-*`. | `docker-compose.yml`, `docker-compose.prod.yml` | Since NCKL production must not use Docker, either remove or mark local-only and rename if retained. |
| Must be replaced | `.env.example` uses `stl_db`, `stl_user`, STL sender, SAHA WhatsApp. | `.env.example:18-24,33,61` | Replace with NCKL placeholders only, no real values. |
| Must be replaced | `deploy/root_setup.sh` creates `saha_db`, `saha_user`, installs `saha-*` services, sets SAHA domains. | `deploy/root_setup.sh:12,16-17,47,64,84,94,113-119` | Do not run. Rewrite for NCKL only after deployment decisions. |
| Must be replaced | Backup/restore scripts use Docker and `stl_user`/`stl_db`. | `scripts/backup_db.sh`, `scripts/restore_db.sh` | Replace with no-Docker PostgreSQL backup/restore commands for NCKL. |
| Must be removed or replaced | `scripts/create_admin.py` hardcodes an admin email and weak password. | `scripts/create_admin.py:6-7` | Remove or replace with env-driven bootstrap command. |
| Must be renamed | Celery app named `stl`. | `backend/config/celery.py` | Low operational risk, but rename for clarity during decoupling. |
| Must be renamed | Log file name is `stl.log`. | `backend/config/settings/base.py:213` | Use `nckl.log` or configurable log path. |

## Build and Artifact Coupling

| Classification | Finding | Evidence | Recommended action |
| --- | --- | --- | --- |
| Must be removed | `frontend/tsconfig.tsbuildinfo` is tracked and contains absolute `/home/mignon/saha/...` paths. | `git ls-files`, `rg` output | Stop tracking build artifact in a future code phase; do not edit in this planning run. |
| Must be removed | Ignored `frontend/.next/`, `node_modules/`, `backend/staticfiles/` exist locally. | `git status --ignored` | Keep untracked; do not use as NCKL release source. |
| Must be removed | Existing ignored logs and media exist locally. | `git status --ignored`, `find` | Keep untracked; treat as sensitive artifacts. |

## Safe Reusable Generic Code

Recommendation.

The following appear reusable after configuration/content replacement:

| Area | Why reusable |
| --- | --- |
| Django app structure | Clean domain separation, public/admin split. |
| DRF serializers/views | Mostly generic logistics CRUD and request flow. |
| Auth/password reset/email verification | Generic with branding changes and token-storage review. |
| Request ownership checks | Good privacy boundary for customer-owned requests. |
| Public tracking serializer | Minimizes PII exposure for anonymous reference lookup. |
| Admin CRUD/editor patterns | Reusable once content and reference/status terms are NCKL-aligned. |
| Upload validation | Reusable with MIME/content validation improvements. |
| Audit log and status events | Useful operational controls. |
| Celery notifications | Reusable with NCKL VAPID, email sender, and copy. |
| i18n infrastructure | Reusable; translation content must be rewritten. |

## Requires Owner Clarification

Unknown/unverified.

| Topic | Why blocked |
| --- | --- |
| Final NCKL domain/API domain | Not supplied. |
| NCKL email sender/support email | Not supplied in inspected readable text. |
| NCKL phone/WhatsApp | Not verifiably extracted from blocked images. |
| NCKL services/prices/destinations | Image extraction blocked; no explicit text facts available. |
| NCKL legal entity, address, registration, privacy terms | Not supplied in readable text. |
| Required languages | Current app supports FR/DE; NCKL requirement must be confirmed. |
| Whether Cameroon-specific status remains valid | Depends on NCKL geography. |
| Whether online payment is expected | Existing app only records manual payment status. |

