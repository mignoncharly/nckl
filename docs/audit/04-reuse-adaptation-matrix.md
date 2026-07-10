# 04 - Reuse and Adaptation Matrix

## Reuse Unchanged

| File/module | Current responsibility | Problem/coupling | NCKL treatment | Risk | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- | --- |
| `backend/apps/core/pagination.py` | Shared DRF pagination | None found | Reuse unchanged | Low | DRF | API list tests |
| `backend/apps/core/exceptions.py` | Adds `status_code` to DRF errors | Generic | Reuse unchanged unless API format changes | Low | DRF | Error response tests |
| `backend/apps/core/permissions.py` | `IsStaffOrAdmin` role permission | Generic role names | Reuse unchanged if roles stay admin/staff/customer | Low | `accounts.User.role` | Permission tests |
| `backend/apps/customers/matching.py` | Conservative phone matching | Generic; lacks full E.164 region | Reuse initially | Medium | Customer model | Matching tests |
| `backend/apps/logistics/reference.py` retry algorithm | Race-safe unique reference creation | Prefix is client-specific | Reuse algorithm, not literal prefix | Medium | DB unique constraint | Collision tests |
| `backend/apps/logistics/views.py` ownership scoping | Public create/tracking, admin/customer views | Some status/copy coupling elsewhere | Reuse structure | Medium | serializers, models | Request/API tests |
| `backend/apps/audit/*` | Audit log infrastructure | May log sensitive metadata | Reuse with redaction review | Medium | signals/middleware | Audit tests |
| `frontend/src/lib/api.ts` | Fetch wrapper, language/auth headers | API base fallback local-only | Reuse with config review | Low | auth/i18n | API integration tests |
| `frontend/src/components/ui/*` | Shared UI primitives | Generic | Reuse | Low | Tailwind | Visual/regression checks |

## Reuse After Configuration

| File/module | Current responsibility | Problem/coupling | NCKL treatment | Risk | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- | --- |
| `backend/config/settings/base.py` | Core Django settings | Defaults use `stl_*`, STL email, `stl.log` | Replace defaults with neutral/NCKL placeholders; fail fast in production | High | env files, systemd | `manage.py check --deploy` later |
| `backend/config/settings/production.py` | Production security/email/CORS | Sender fallback is STL; env validation weak | Require NCKL env; no source defaults | High | NCKL `.env` | Startup check |
| `frontend/next.config.js` | Headers, CSP report-only, rewrites, image config | CSP has SAHA API origin | Make API origin configurable; NCKL domains | High | deployment domain | Header inspection |
| `frontend/src/lib/constants.ts` | Contact/city constants | SAHA phone and service areas | Centralize NCKL contact/areas or pull from API | High | NCKL requirements | Search + UI review |
| `frontend/src/lib/i18n-config.ts` | FR/DE translations | Many SAHA strings | Replace copy; keep utility | High | content catalogue | Bilingual review |
| `backend/apps/notifications/emails.py` | Branded transactional emails | SAHA brand/email/phone | Parameterize brand/contact; rewrite copy | High | settings/i18n | Rendered email snapshots |
| `frontend/src/app/manifest.webmanifest/route.ts` | PWA manifest | SAHA name/short name | NCKL app identity | Medium | icons/theme | Manifest check |
| `frontend/public/sw.js` | Service worker | Cache name `stl-v2` | Rename cache namespace | Low | PWA | Browser/PWA smoke test |

## Refactor Before Reuse

| File/module | Current responsibility | Problem/coupling | NCKL treatment | Risk | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- | --- |
| `backend/apps/logistics/models.py` | Request statuses include `arrived_cameroon` | Geography encoded in DB value | If NCKL route differs, add migration to generic status (`arrived_destination`) | High | frontend status maps, tests, data | Migration + status tests |
| `frontend/src/components/public/StatusTimeline.tsx` and `StatusBadge.tsx` | Status labels | Cameroon-specific status labels | Generalize labels via i18n/status config | Medium | status model | UI + API status tests |
| `backend/apps/destinations/models.py` | Destination city default country | Default `Cameroun` | Make country required/configured or seed-specific | Medium | migrations/seed | Model/admin tests |
| `backend/apps/schedules/models.py` | Pickup region default country | Default `Allemagne` | Make seed/config-driven | Medium | migrations/seed | Schedule tests |
| `scripts/backup_db.sh`, `scripts/restore_db.sh` | Docker backup/restore | Docker and STL DB names | Replace with no-Docker NCKL PostgreSQL scripts | High | DB naming | Restore test |
| `scripts/create_admin.py` | Ad hoc admin bootstrap | Hardcoded email/weak password | Replace with env-driven management command | High | accounts | Bootstrap dry run |
| `deploy/root_setup.sh` | SAHA provisioning | Touches SAHA names/resources | Rewrite from scratch for NCKL or split into reviewed steps | Critical | infra decisions | Manual review only |

## Replace For NCKL

| File/module | Current responsibility | Problem/coupling | NCKL treatment | Risk | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- | --- |
| `README.md`, existing `docs/*.md` | Project docs | SAHA docs | Create NCKL docs; mark legacy if retained | Medium | operational choices | Search for SAHA references |
| `frontend/src/app/layout.tsx` | Metadata and root layout | SAHA title/description | NCKL SEO metadata | Medium | content/legal | Browser metadata check |
| `frontend/src/components/layout/Footer.tsx` | Footer brand/contact | SAHA copy/email | NCKL contact/legal/footer | High | requirements | UI review |
| `frontend/src/components/layout/AppNavbar.tsx` | Brand/navigation | Displays STL | NCKL logo/name | Medium | assets | Responsive visual check |
| `frontend/src/app/contact/page.tsx` | Contact UI/form | SAHA email/phone/areas | NCKL contact channels | High | contact info | Form test |
| `frontend/src/app/privacy/page.tsx` | Privacy copy | SAHA email and policy claims | NCKL legal/privacy text | High | legal owner | Legal review |
| `frontend/src/components/public/HeroSection.tsx` | Homepage hero | SAHA route/copy/image alt | NCKL brand/services | High | images/content | Visual review |
| `backend/apps/*/seed_data.py` | Reference seed data | SAHA services/prices/destinations/schedules | Replace with NCKL seed records | High | requirements | Seed dry run in isolated DB |
| `frontend/src/app/icon.svg`, `frontend/public/icons/*` | PWA/favicon/logo assets | STL icon | NCKL assets | Medium | supplied logo | Asset check |

## Remove

| File/module | Current responsibility | Reason | Risk | Validation |
| --- | --- | --- | --- | --- |
| Ignored `backups/` | Copied SQL/secret backups | Not part of NCKL repo; possible data/secrets | Critical | Confirm untracked and remove only with approval |
| Ignored `.env`, `frontend/.env.production`, `deploy/.secrets.json`, `deploy/redis-saha.conf` | Local runtime config | Source/copy secrets | Critical | Confirm ignored, never staged |
| Ignored `backend/media/`, `backend/test_media/` | Uploaded/test files | Possible PII; not NCKL seed media | Critical | Confirm ignored, never staged |
| Tracked `frontend/tsconfig.tsbuildinfo` | Build artifact | Absolute SAHA paths | Medium | Stop tracking later; `git status` clean |
| Docker production path | Docker compose production | Target says do not use Docker | Medium | Docs and deployment scripts no longer instruct Docker |

