# 03 - Security Review

## Summary

Status: recommendation.

The current codebase has several mature controls worth preserving: Django password validators, DRF token authentication, explicit admin role permission, throttles on sensitive public endpoints, privacy-safe anonymous tracking, customer-owned request scoping, HTTPS production settings, audit logging, and file size/extension validation.

The highest NCKL risks are not novel code bugs; they are isolation and contamination risks from copied SAHA runtime artifacts, secrets, backups, media, domains, service names, and hardcoded client identity.

## Critical

| Finding | Evidence | Risk | Remediation | Validation |
| --- | --- | --- | --- | --- |
| Ignored runtime secrets exist in NCKL checkout. | `.env`, `deploy/.secrets.json`, `deploy/redis-saha.conf`, `frontend/.env.production` shown by `git status --ignored` | Secrets may be copied from SAHA or accidentally staged during public repo work. | Keep ignored; never stage. Replace with NCKL-only secrets. Rotate any values copied from SAHA. Add pre-commit/CI secret scanning. | `git status --short --ignored`; staged secret scan before every commit. |
| Ignored database backups exist. | `backups/*.sql`, backup `.env.bak`, `.secrets.json.bak`, `redis-saha.conf.bak` | Possible production data or secret leakage in local workspace. | Do not commit. Confirm origin. Remove from NCKL workspace only after explicit approval and backup policy decision. | `find backups -maxdepth 3 -type f`; `git check-ignore backups/...`. |
| Ignored media/test media files exist. | `backend/media/request_photos/*`, `backend/test_media/request_photos/*` | Possible customer-uploaded PII/documents/images. | Do not commit or seed. Use empty NCKL media root at launch. | `find backend/media backend/test_media -type f`; verify NCKL media directory empty before deploy. |
| Deployment files point at SAHA production paths/domains/ports. | `deploy/systemd/saha-*`, `deploy/nginx/*`, `deploy/root_setup.sh` | Running these for NCKL could collide with or expose SAHA resources. | Do not run existing deployment scripts. Rewrite for `nckl-*` only after domain/port/database decisions. | Static review; dry-run Nginx/systemd unit review in NCKL-only paths. |

## High

| Finding | Evidence | Risk | Remediation | Validation |
| --- | --- | --- | --- | --- |
| Frontend CSP report-only allows `https://api-saha.docufisc.de`. | `frontend/next.config.js:13` | Browser config still references source API; NCKL could leak requests or reports. | Replace with NCKL API origin or env-derived CSP. | Search for `api-saha` returns zero before launch. |
| DRF token stored in `localStorage`. | `frontend/src/lib/auth.ts:5-13` | XSS can steal tokens. | Harden CSP and sanitize all rendered content; consider HttpOnly cookie/session alternative before launch. | Security review and auth regression tests. |
| Email templates and sender identities are hardcoded to SAHA/STL. | `backend/apps/notifications/emails.py`, `DEFAULT_FROM_EMAIL` defaults | NCKL emails could impersonate source client or use wrong sender. | Centralize brand/email settings and replace values. | Send email only in isolated test backend; inspect rendered messages. |
| Contact form uses submitter email as `from_email`. | `backend/apps/contact/views.py` | SPF/DMARC delivery failures; possible header handling concerns mitigated by Django but still operationally poor. | Use NCKL verified sender as `from_email`, set user email as reply-to. | Unit test message headers. |
| Upload validation checks extension and size, not MIME/content. | `backend/apps/uploads/validators.py` | Malicious file with allowed extension could be uploaded. | Add MIME/content sniffing with Pillow verification, normalize filenames, keep files outside executable paths. | Upload tests for wrong MIME, oversized, malformed images. |
| Anonymous tracking exists by reference code. | `PublicTransportRequestDetailView` | Reference guessing could expose limited shipment state. Current serializer is minimal. | Keep minimal serializer; consider rate throttle and non-sequential/less guessable references. | Assert tracking output excludes PII/prices/photos/internal notes. |
| Reference codes are sequential `STL-YYYY-NNNNNN`. | `backend/apps/logistics/reference.py:21` | Easy enumeration pattern; also client-specific. | Use NCKL prefix and consider random suffix or sufficient throttling. | Reference tests and tracking rate-limit tests. |

## Medium

| Finding | Evidence | Risk | Remediation | Validation |
| --- | --- | --- | --- | --- |
| Global DRF default permission is `AllowAny`. | `backend/config/settings/base.py` REST framework settings | New endpoints may accidentally become public. | Prefer default authenticated permission or enforce lint/review rule that public endpoints explicitly opt out. | Endpoint permission tests. |
| CSP in backend middleware has `connect-src 'self' http://localhost:*` and unsafe script allowances. | `backend/apps/core/middleware.py` | CSP may be ineffective or inconsistent with frontend. | Consolidate CSP at Nginx/Next/backend with NCKL domains; enforce after report-only period. | Browser header check. |
| Production `SECURE_SSL_REDIRECT=True` may be risky behind reverse proxy if not configured correctly. | `backend/config/settings/production.py` | Redirect loops if proxy headers are wrong. | Validate Nginx `X-Forwarded-Proto` and Django `SECURE_PROXY_SSL_HEADER`. | Staging smoke tests. |
| `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` split empty env values directly. | `backend/config/settings/production.py` | Empty entries or misconfig could cause availability/security issues. | Validate required env at startup; fail fast if missing. | Django check/boot validation. |
| `send_mail(..., fail_silently=True)` for contact form. | `backend/apps/contact/views.py` | Operators may miss failed customer inquiries. | Log failures or create `ContactMessage` model/email log. | Unit test error path; ops dashboard. |
| Audit metadata may include sensitive values depending on signals. | `audit` app | PII may enter audit logs. | Redact selected fields, define retention. | Audit log tests. |
| No explicit rate limit on public tracking GET found. | `PublicTransportRequestDetailView` | Brute force reference lookup. | Add scoped throttle. | Rate-limit tests. |

## Low

| Finding | Evidence | Risk | Remediation |
| --- | --- | --- | --- |
| Logs write to `backend/logs/stl.log`. | `backend/config/settings/base.py:213` | Naming contamination; possible PII in local logs. | Rename and route NCKL logs to dedicated path with rotation. |
| Build artifact `frontend/tsconfig.tsbuildinfo` is tracked. | `git ls-files` | Absolute path leakage and noisy diffs. | Stop tracking in implementation phase. |
| Docker files exist despite no-Docker target. | `docker-compose*.yml`, `Makefile` | Operator confusion. | Mark local-only or remove/replace with no-Docker docs. |

## Positive Controls To Preserve

Status: verified fact.

| Control | Evidence |
| --- | --- |
| Password validators on register/reset | `accounts.serializers.RegisterSerializer`, `accounts.views.PasswordResetConfirmView` |
| Generic password reset response | `PasswordResetView` |
| Throttles for auth, reset, verify, resend, public request, contact, push subscription | `backend/apps/core/throttles.py` |
| Admin routes protected by `IsStaffOrAdmin` | Multiple admin views |
| Customer-owned request detail filters by customer profile | `CustomerRequestDetailView` |
| Anonymous tracking serializer excludes PII/prices/photos/internal notes | `PublicTransportRequestTrackingSerializer` |
| Status history events | `RequestStatusEvent` |
| Audit middleware and audit log | `backend/apps/audit/*` |
| Production HTTPS cookies and HSTS | `backend/config/settings/production.py` |
| Test settings avoid real Postgres/Redis and use in-memory SQLite/cache | `backend/config/settings/test.py` |

## Dependency and External Risk

Status: unknown.

No dependency audit (`npm audit`, `pip-audit`, Safety, Snyk) was run in this planning pass. Network/package operations were intentionally avoided. A future implementation phase should run dependency checks in a safe NCKL context, not against SAHA.

